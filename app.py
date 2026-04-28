from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import stripe
import os
import random
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

FRONTEND_URL = "https://planova-lwj9.onrender.com"

# -------------------------
# DB
# -------------------------
def init_db():
    conn = sqlite3.connect("users.db", timeout=10)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            verified INTEGER DEFAULT 0,
            verification_code TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# -------------------------
# HELPERS
# -------------------------
def generate_code():
    return str(random.randint(100000, 999999))


def send_email(to_email, code):
    try:
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")

        if not email_user or not email_pass:
            print("EMAIL MISSING ENV VARS")
            return False

        msg = MIMEText(f"Your Planova verification code is: {code}")
        msg["Subject"] = "Verify your Planova account"
        msg["From"] = email_user
        msg["To"] = to_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
        server.quit()

        print("EMAIL SENT")
        return True

    except Exception as e:
        print("EMAIL ERROR:", e)
        return False


# -------------------------
# REGISTER (TEMP ACCOUNT ONLY)
# -------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    if not full_name or not email or not password:
        return jsonify({"success": False, "message": "Missing fields"}), 400

    code = generate_code()
    hashed_pw = generate_password_hash(password)

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("SELECT email FROM users WHERE email = ?", (email,))
    exists = cur.fetchone()

    if exists:
        # overwrite unverified
        cur.execute("""
            UPDATE users
            SET full_name=?, password=?, verification_code=?, verified=0
            WHERE email=?
        """, (full_name, hashed_pw, code, email))
    else:
        cur.execute("""
            INSERT INTO users (full_name, email, password, verified, verification_code)
            VALUES (?, ?, ?, 0, ?)
        """, (full_name, email, hashed_pw, code))

    conn.commit()
    conn.close()

    email_sent = send_email(email, code)

    if not email_sent:
        return jsonify({"success": False, "message": "Email failed"}), 500

    return jsonify({"success": True})


# -------------------------
# VERIFY (FINALISE ACCOUNT)
# -------------------------
@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json() or {}

    email = data.get("email")
    code = data.get("code")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT verification_code, password
        FROM users WHERE email=?
    """, (email,))

    row = cur.fetchone()

    if not row:
        return jsonify({"success": False, "message": "User not found"}), 400

    db_code, hashed_pw = row

    if db_code != code:
        return jsonify({"success": False, "message": "Invalid code"}), 400

    cur.execute("""
        UPDATE users
        SET verified=1, verification_code=NULL
        WHERE email=?
    """, (email,))

    conn.commit()
    conn.close()

    return jsonify({"success": True})


# -------------------------
# RESEND
# -------------------------
@app.route("/resend-code", methods=["POST"])
def resend_code():
    data = request.get_json() or {}
    email = data.get("email")

    code = generate_code()

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
        UPDATE users SET verification_code=?
        WHERE email=?
    """, (code, email))

    conn.commit()
    conn.close()

    send_email(email, code)

    return jsonify({"success": True})


# -------------------------
# LOGIN
# -------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("SELECT full_name, password, verified FROM users WHERE email=?", (email,))
    row = cur.fetchone()

    conn.close()

    if not row:
        return jsonify({"success": False}), 400

    full_name, hashed_pw, verified = row

    if not verified:
        return jsonify({"success": False, "message": "Verify first"}), 403

    if not check_password_hash(hashed_pw, password):
        return jsonify({"success": False}), 400

    return jsonify({"success": True, "full_name": full_name})
# -------------------------------------------------
# EXISTING ROUTES (UNCHANGED)
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
# Wakeup
# -------------------------------------------------
@app.route("/wakeup")
def wakeup():
    return "awake", 200


# -------------------------------------------------
# Helpers (unchanged)
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
# Stripe (UNCHANGED)
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
# Run
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)