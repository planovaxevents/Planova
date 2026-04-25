from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import stripe
import os

app = Flask(__name__)

# -------------------------------------------------
# CORS — allow your frontend domain to call backend
# -------------------------------------------------
CORS(app, resources={r"/*": {"origins": "*"}})

# -------------------------------------------------
# Stripe Setup
# -------------------------------------------------
stripe.api_key = "YOUR_STRIPE_SECRET_KEY"   # sk_live_...

# -------------------------------------------------
# Database Setup
# -------------------------------------------------
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------------------------------------
# Register Route
# -------------------------------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    if not full_name or not email or not password:
        return jsonify({"success": False, "message": "Missing fields"}), 400

    hashed_pw = generate_password_hash(password)

    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO users (full_name, email, password)
            VALUES (?, ?, ?)
        """, (full_name, email, hashed_pw))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Account created!"})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Email already registered"}), 400

# -------------------------------------------------
# Login Route
# -------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT full_name, password FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"success": False, "message": "Email not found"}), 400

    full_name, hashed_pw = row

    if not check_password_hash(hashed_pw, password):
        return jsonify({"success": False, "message": "Incorrect password"}), 400

    return jsonify({"success": True, "full_name": full_name})

# -------------------------------------------------
# Delete Account
# -------------------------------------------------
@app.route("/delete-account", methods=["POST"])
def delete_account():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("SELECT password FROM users WHERE email = ?", (email,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return jsonify({"success": False, "message": "Account not found"}), 400

    hashed_pw = row[0]

    if not check_password_hash(hashed_pw, password):
        conn.close()
        return jsonify({"success": False, "message": "Incorrect password"}), 400

    cur.execute("DELETE FROM users WHERE email = ?", (email,))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Account deleted"})

# -------------------------------------------------
# Change Password
# -------------------------------------------------
@app.route("/change-password", methods=["POST"])
def change_password():
    data = request.get_json()
    email = data.get("email")
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("SELECT password FROM users WHERE email = ?", (email,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return jsonify({"success": False, "message": "Account not found"}), 400

    hashed_pw = row[0]

    if not check_password_hash(hashed_pw, old_password):
        conn.close()
        return jsonify({"success": False, "message": "Incorrect current password"}), 400

    new_hashed = generate_password_hash(new_password)

    cur.execute("""
        UPDATE users
        SET password = ?
        WHERE email = ?
    """, (new_hashed, email))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Password updated"})

# -------------------------------------------------
# Render Wake-Up Endpoint (prevents first-request failure)
# -------------------------------------------------
@app.route("/wakeup")
def wakeup():
    return "awake", 200

# -------------------------------------------------
# Stripe Checkout Session (FULLY UPGRADED)
# -------------------------------------------------
@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    data = request.get_json()

    event_title = data.get("event_title", "Event")
    standard = int(data.get("standard", 0))
    vip = int(data.get("vip", 0))
    vvip = int(data.get("vvip", 0))
    addons = data.get("addons", [])
    pricing = data.get("pricing", {})

    # Fallback price (old system)
    base_price = int(data.get("price", 0))

    if standard + vip + vvip == 0:
        return jsonify({"error": "No tickets selected"}), 400

    line_items = []

    # Standard
    if standard > 0:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": event_title + " – Standard Ticket"},
                "unit_amount": base_price * 100
            },
            "quantity": standard
        })

    # VIP
    if vip > 0:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": event_title + " – VIP Ticket"},
                "unit_amount": base_price * 2 * 100
            },
            "quantity": vip
        })

    # VVIP
    if vvip > 0:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": event_title + " – VVIP Ticket"},
                "unit_amount": base_price * 4 * 100
            },
            "quantity": vvip
        })

    # Add-ons
    if pricing and "addonsBreakdown" in pricing:
        for addon in pricing["addonsBreakdown"]:
            line_items.append({
                "price_data": {
                    "currency": "gbp",
                    "product_data": {"name": addon["label"]},
                    "unit_amount": int(addon["amount"] * 100)
                },
                "quantity": 1
            })

    # Booking fee
    if pricing and "bookingFee" in pricing:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": "Booking Fee"},
                "unit_amount": int(pricing["bookingFee"] * 100)
            },
            "quantity": 1
        })

    # VAT
    if pricing and "vat" in pricing:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": "VAT (20%)"},
                "unit_amount": int(pricing["vat"] * 100)
            },
            "quantity": 1
        })

    # Discount (negative line item)
    if pricing and "discount" in pricing and pricing["discount"] > 0:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": "Discount"},
                "unit_amount": -int(pricing["discount"] * 100)
            },
            "quantity": 1
        })

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=line_items,
            success_url="YOUR_FRONTEND_URL/success.html",
            cancel_url="YOUR_FRONTEND_URL/checkout.html"
        )

        return jsonify({"sessionId": session.id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------------------------
# Serve HTML files (Render static hosting)
# -------------------------------------------------
@app.route("/")
def serve_index():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/<path:filename>")
def serve_files(filename):
    return send_from_directory(os.getcwd(), filename)

# -------------------------------------------------
# Run Server (Render ignores this)
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
