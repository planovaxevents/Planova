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
import threading  # ✅ ADDED

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
# OTP STORAGE
# -------------------------------------------------
otp_store = {}
# { email: { "code": "123456", "expires": 1234567890 } }

OTP_TTL = 300  # 5 minutes

# -------------------------------------------------
# EMAIL CONFIG
# -------------------------------------------------
EMAIL_ADDRESS = "planovaxevents@gmail.com"
EMAIL_PASSWORD = "hxzo ogtb tuze imag"

def send_email(to_email, code):
    html = f"""
    <html>
    <body style="margin:0;padding:0;background:#0b0b0b;font-family:Arial,sans-serif;">
      <div style="max-width:600px;margin:0 auto;background:#111;border-radius:12px;overflow:hidden;border:1px solid #1f1f1f;">
        <div style="padding:30px;text-align:center;background:linear-gradient(135deg,#00ff88,#00c77a);">
          <h1 style="margin:0;color:#0b0b0b;font-size:26px;letter-spacing:2px;">PLANOVA</h1>
          <p style="margin:6px 0 0;color:#0b0b0b;font-size:13px;">Secure Verification System</p>
        </div>

        <div style="padding:35px;color:#ffffff;text-align:center;">
          <h2 style="margin-bottom:10px;font-size:22px;">Verify your email</h2>

          <p style="color:#bbb;font-size:14px;">
            Use the verification code below to continue.
          </p>

          <div style="margin:25px auto;padding:20px;width:200px;font-size:28px;letter-spacing:6px;font-weight:bold;background:#000;border:1px solid #00ff88;border-radius:10px;color:#00ff88;">
            {code}
          </div>

          <p style="color:#888;font-size:12px;">Expires in 5 minutes</p>
        </div>

        <div style="padding:20px;text-align:center;background:#0a0a0a;color:#555;font-size:11px;">
          © {time.strftime("%Y")} PLANOVA
        </div>
      </div>
    </body>
    </html>
    """

    msg = MIMEText(html, "html")
    msg["Subject"] = "Your PLANOVA Verification Code"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    # ✅ FIX: timeout added
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


# ✅ NEW: background sender (prevents timeout crash)
def send_email_async(email, code):
    try:
        send_email(email, code)
    except Exception as e:
        print("EMAIL ERROR:", e)


# -------------------------------------------------
# CLEANUP EXPIRED OTPs
# -------------------------------------------------
def cleanup_otps():
    now = time.time()
    expired = [email for email, v in otp_store.items() if v["expires"] < now]
    for email in expired:
        otp_store.pop(email, None)

# -------------------------------------------------
# DB INIT
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
# SEND CODE (FIXED)
# -------------------------------------------------
@app.route("/send_code", methods=["POST"])
def send_code():
    cleanup_otps()

    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()

    if not email:
        return jsonify({"success": False, "message": "Email required"}), 400

    code = str(random.randint(100000, 999999))
    expires = time.time() + OTP_TTL

    otp_store[email] = {
        "code": code,
        "expires": expires
    }

    # ✅ NON-BLOCKING EMAIL SEND
    threading.Thread(target=send_email_async, args=(email, code)).start()

    return jsonify({"success": True, "message": "Code sent"})


# -------------------------------------------------
# VERIFY CODE
# -------------------------------------------------
@app.route("/verify_code", methods=["POST"])
def verify_code():
    cleanup_otps()

    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    code = (data.get("code") or "").strip()

    record = otp_store.get(email)

    if not record:
        return jsonify({"success": False, "message": "No code found"}), 400

    if time.time() > record["expires"]:
        otp_store.pop(email, None)
        return jsonify({"success": False, "message": "Code expired"}), 400

    if record["code"] != code:
        return jsonify({"success": False, "message": "Invalid code"}), 400

    return jsonify({"success": True, "message": "Verified"})

# -------------------------------------------------
# REGISTER (UNCHANGED)
# -------------------------------------------------
@app.route("/register", methods=["POST"])
def register():
    cleanup_otps()

    data = request.get_json() or {}

    full_name = data.get("full_name")
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")
    code = (data.get("code") or "").strip()

    if not full_name or not email or not password or not code:
        return jsonify({"success": False, "message": "Missing fields"}), 400

    record = otp_store.get(email)

    if not record:
        return jsonify({"success": False, "message": "No verification code"}), 403

    if time.time() > record["expires"]:
        otp_store.pop(email, None)
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
    email = (data.get("email") or "").strip().lower()
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

    if not check_password_hash(row[0], password):
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

    if not check_password_hash(row[0], old_password):
        conn.close()
        return jsonify({"success": False, "message": "Incorrect current password"}), 400

    new_hashed = generate_password_hash(new_password)

    cur.execute("""
        UPDATE users SET password = ? WHERE email = ?
    """, (new_hashed, email))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Password updated"})

# -------------------------------------------------
# WAKEUP
# -------------------------------------------------
@app.route("/wakeup")
def wakeup():
    return "awake", 200

# -------------------------------------------------
# SAFE HELPERS
# -------------------------------------------------
def safe_int(value, default=0):
    try:
        return int(value) if value not in [None, ""] else default
    except:
        return default

def safe_float(value, default=0.0):
    try:
        return float(value) if value not in [None, ""] else default
    except:
        return default

# -------------------------------------------------
# STRIPE (UNCHANGED)
# -------------------------------------------------
@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    data = request.get_json() or {}

    event_title = data.get("event_title", "Event")

    standard = safe_int(data.get("standard"))
    vip = safe_int(data.get("vip"))
    vvip = safe_int(data.get("vvip"))

    pricing = data.get("pricing", {})
    total = safe_float(pricing.get("total"))

    if total <= 0:
        return jsonify({"error": "Invalid total amount"}), 400

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "gbp",
                    "product_data": {
                        "name": event_title,
                        "description": f"{standard} Standard, {vip} VIP, {vvip} VVIP tickets"
                    },
                    "unit_amount": int(total * 100)
                },
                "quantity": 1
            }],
            success_url=f"{FRONTEND_URL}/success.html",
            cancel_url=f"{FRONTEND_URL}/checkout.html"
        )

        return jsonify({"sessionId": session.id})

    except Exception as e:
        print("STRIPE ERROR:", e)
        return jsonify({"error": str(e)}), 500

# -------------------------------------------------
# STATIC
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