from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import stripe
import os
import random
import time
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# -------------------------------------------------
# CORS
# -------------------------------------------------
CORS(app, resources={r"/*": {"origins": "*"}})

# -------------------------------------------------
# Stripe Setup
# -------------------------------------------------
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

FRONTEND_URL = "https://planova-lwj9.onrender.com"

# -------------------------------------------------
# OTP STORAGE (NEW - ADDED)
# -------------------------------------------------
otp_store = {}
# { email: { "code": "123456", "expires": 1234567890 } }

# -------------------------------------------------
# EMAIL CONFIG (SET THIS)
# -------------------------------------------------
EMAIL_ADDRESS = "planovaxevents@gmail.com"
EMAIL_PASSWORD = "hxzo ogtb tuze imag"

def send_email(to_email, code):
    msg = MIMEText(f"Your PLANOVA verification code is: {code}")
    msg["Subject"] = "PLANOVA Email Verification"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

# -------------------------------------------------
# DB Setup
# -------------------------------------------------
def init_db():
    conn = sqlite3.connect("users.db", timeout=10)
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
# OTP ENDPOINT (NEW)
# -------------------------------------------------
@app.route("/send_code", methods=["POST"])
def send_code():
    data = request.get_json() or {}
    email = data.get("email")

    if not email:
        return jsonify({"success": False, "message": "Email required"}), 400

    code = str(random.randint(100000, 999999))
    expires = time.time() + 300  # 5 min expiry

    otp_store[email] = {
        "code": code,
        "expires": expires
    }

    try:
        send_email(email, code)
        return jsonify({"success": True, "message": "Code sent"})
    except Exception as e:
        print("EMAIL ERROR:", e)
        return jsonify({"success": False, "message": "Failed to send email"}), 500


# -------------------------------------------------
# VERIFY CODE (OPTIONAL BUT USEFUL)
# -------------------------------------------------
@app.route("/verify_code", methods=["POST"])
def verify_code():
    data = request.get_json() or {}
    email = data.get("email")
    code = data.get("code")

    record = otp_store.get(email)

    if not record:
        return jsonify({"success": False, "message": "No code sent"}), 400

    if time.time() > record["expires"]:
        return jsonify({"success": False, "message": "Code expired"}), 400

    if record["code"] != code:
        return jsonify({"success": False, "message": "Invalid code"}), 400

    return jsonify({"success": True, "message": "Verified"})


# -------------------------------------------------
# AUTH ROUTES (UPDATED REGISTER ONLY)
# -------------------------------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    code = data.get("code")  # 🔥 REQUIRED NOW

    if not full_name or not email or not password or not code:
        return jsonify({"success": False, "message": "Missing fields"}), 400

    # VERIFY OTP BEFORE REGISTERING
    record = otp_store.get(email)

    if not record:
        return jsonify({"success": False, "message": "No verification code sent"}), 403

    if time.time() > record["expires"]:
        return jsonify({"success": False, "message": "Code expired"}), 403

    if record["code"] != code:
        return jsonify({"success": False, "message": "Invalid verification code"}), 403

    hashed_pw = generate_password_hash(password)

    conn = None
    try:
        conn = sqlite3.connect("users.db", timeout=10)
        c = conn.cursor()

        c.execute("""
            INSERT INTO users (full_name, email, password)
            VALUES (?, ?, ?)
        """, (full_name, email, hashed_pw))

        conn.commit()

        # remove OTP after success
        otp_store.pop(email, None)

        return jsonify({"success": True, "message": "Account created!"})

    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Email already registered"}), 400

    except Exception as e:
        print("REGISTER ERROR:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

    finally:
        if conn:
            conn.close()


# -------------------------------------------------
# LOGIN (UNCHANGED)
# -------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect("users.db", timeout=10)
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
# DELETE ACCOUNT (UNCHANGED)
# -------------------------------------------------
@app.route("/delete-account", methods=["POST"])
def delete_account():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect("users.db", timeout=10)
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
# CHANGE PASSWORD (UNCHANGED)
# -------------------------------------------------
@app.route("/change-password", methods=["POST"])
def change_password():
    data = request.get_json() or {}
    email = data.get("email")
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    conn = sqlite3.connect("users.db", timeout=10)
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
# WAKEUP (UNCHANGED)
# -------------------------------------------------
@app.route("/wakeup")
def wakeup():
    return "awake", 200


# -------------------------------------------------
# HELPERS (UNCHANGED)
# -------------------------------------------------
def safe_int(value, default=0):
    try:
        if value is None or value == "":
            return default
        return int(value)
    except:
        return default


def safe_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except:
        return default


# -------------------------------------------------
# STRIPE (UNCHANGED)
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

    if standard > 0:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": f"{event_title} – Standard Ticket"},
                "unit_amount": base_price * 100
            },
            "quantity": standard
        })

    if vip > 0:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": f"{event_title} – VIP Ticket"},
                "unit_amount": base_price * 2 * 100
            },
            "quantity": vip
        })

    if vvip > 0:
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": f"{event_title} – VVIP Ticket"},
                "unit_amount": base_price * 4 * 100
            },
            "quantity": vvip
        })

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
# STATIC FILES (UNCHANGED)
# -------------------------------------------------
@app.route("/")
def serve_index():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/<path:filename>")
def serve_files(filename):
    return send_from_directory(os.getcwd(), filename)


# -------------------------------------------------
# RUN
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)