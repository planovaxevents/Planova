from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import stripe
import os

app = Flask(__name__)

# -------------------------------------------------
# CORS
# -------------------------------------------------
CORS(app, resources={r"/*": {"origins": "*"}})

# -------------------------------------------------
# Stripe Setup
# -------------------------------------------------
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Auto-detect environment (LOCAL vs RENDER)
if os.getenv("RENDER"):
    FRONTEND_URL = "https://planova-lwj9.onrender.com"
else:
    FRONTEND_URL = "http://127.0.0.1:5000"

print("USING FRONTEND_URL:", FRONTEND_URL)

# -------------------------------------------------
# DB Setup
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
# Auth routes
# -------------------------------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
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

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
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

@app.route("/delete-account", methods=["POST"])
def delete_account():
    data = request.get_json() or {}
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

@app.route("/change-password", methods=["POST"])
def change_password():
    data = request.get_json() or {}
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
# Wakeup
# -------------------------------------------------
@app.route("/wakeup")
def wakeup():
    return "awake", 200

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def safe_int(value, default=0):
    try:
        if value is None or value == "":
            return default
        return int(value)
    except (TypeError, ValueError):
        return default

def safe_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default

# -------------------------------------------------
# Stripe Checkout Session
# -------------------------------------------------
@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    data = request.get_json() or {}
    print("INCOMING CHECKOUT DATA:", data)

    event_title = data.get("event_title", "Event")

    standard = safe_int(data.get("standard"), 0)
    vip = safe_int(data.get("vip"), 0)
    vvip = safe_int(data.get("vvip"), 0)

    pricing = data.get("pricing") or {}
    base_price = safe_int(data.get("price"), 0)

    if standard + vip + vvip == 0:
        return jsonify({"error": "No tickets selected"}), 400

    line_items = []

    # Standard
    if standard > 0:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": f"{event_title} – Standard Ticket"},
                "unit_amount": base_price * 100
            },
            "quantity": standard
        })

    # VIP
    if vip > 0:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": f"{event_title} – VIP Ticket"},
                "unit_amount": base_price * 2 * 100
            },
            "quantity": vip
        })

    # VVIP
    if vvip > 0:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": f"{event_title} – VVIP Ticket"},
                "unit_amount": base_price * 4 * 100
            },
            "quantity": vvip
        })

    # Add-ons
    addons_breakdown = pricing.get("addonsBreakdown") or []
    for addon in addons_breakdown:
        label = addon.get("label", "Add-on")
        amount = safe_float(addon.get("amount"), 0.0)
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": label},
                "unit_amount": int(amount * 100)
            },
            "quantity": 1
        })

    # Booking fee
    booking_fee = safe_float(pricing.get("bookingFee"), 0.0)
    if booking_fee > 0:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": "Booking Fee"},
                "unit_amount": int(booking_fee * 100)
            },
            "quantity": 1
        })

    # VAT
    vat = safe_float(pricing.get("vat"), 0.0)
    if vat > 0:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": "VAT (20%)"},
                "unit_amount": int(vat * 100)
            },
            "quantity": 1
        })

    if not line_items:
        return jsonify({"error": "No line items generated"}), 400

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=line_items,
            success_url=f"{FRONTEND_URL}/success.html",
            cancel_url=f"{FRONTEND_URL}/checkout.html"
        )
        return jsonify({"sessionId": session.id})

    except Exception as e:
        print("STRIPE ERROR:", e)
        return jsonify({"error": str(e)}), 500

# -------------------------------------------------
# Static files
# -------------------------------------------------
@app.route("/")
def serve_index():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/<path:filename>")
def serve_files(filename):
    return send_from_directory(os.getcwd(), filename)

# -------------------------------------------------
# Local run
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
