from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import stripe
import os

app = Flask(__name__)
CORS(app)

# -----------------------------
# Stripe Setup
# -----------------------------
# ❗ IMPORTANT: Replace this with YOUR real secret key (sk_live_...)
stripe.api_key = "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"

# -----------------------------
# Database Setup
# -----------------------------
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

# -----------------------------
# Register Route
# -----------------------------
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


# -----------------------------
# Login Route
# -----------------------------
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


# -----------------------------
# Delete Account
# -----------------------------
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


# -----------------------------
# Change Password
# -----------------------------
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


# -----------------------------
# Stripe Checkout Session
# -----------------------------
@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    data = request.get_json()

    event_id = data.get("event_id")
    standard = int(data.get("standard", 0))
    vip = int(data.get("vip", 0))
    price = int(data.get("price", 0))

    if standard == 0 and vip == 0:
        return jsonify({"error": "No tickets selected"}), 400

    line_items = []

    if standard > 0:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": f"Standard Ticket (Event {event_id})"},
                "unit_amount": price * 100
            },
            "quantity": standard
        })

    if vip > 0:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": f"VIP Ticket (Event {event_id})"},
                "unit_amount": price * 2 * 100
            },
            "quantity": vip
        })

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=line_items,
            success_url="http://127.0.0.1:5000/success.html",
            cancel_url="http://127.0.0.1:5000/checkout.html"
        )

        return jsonify({"sessionId": session.id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# Serve HTML files (NO STATIC FOLDER NEEDED)
# -----------------------------
@app.route("/")
def serve_index():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/<path:filename>")
def serve_files(filename):
    return send_from_directory(os.getcwd(), filename)


# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
