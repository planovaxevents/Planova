from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import stripe
import os

# DBs
import sqlite3
import psycopg2

# Email verification
import random
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
# DATABASE SETUP (HYBRID)
# -------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL)
    else:
        return sqlite3.connect("users.db", timeout=10)

def is_postgres():
    return DATABASE_URL is not None

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    if is_postgres():
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
    else:
        cur.execute("""
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
# REGISTER
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

    conn = None
    try:
        conn = get_conn()
        c = conn.cursor()

        if is_postgres():
            c.execute("""
                INSERT INTO users (full_name, email, password)
                VALUES (%s, %s, %s)
            """, (full_name, email, hashed_pw))
        else:
            c.execute("""
                INSERT INTO users (full_name, email, password)
                VALUES (?, ?, ?)
            """, (full_name, email, hashed_pw))

        conn.commit()

        return jsonify({"success": True, "message": "Account created!"})

    except Exception as e:
        if conn:
            conn.rollback()
        print("REGISTER ERROR:", e)
        return jsonify({"success": False, "message": "Email already registered"}), 400

    finally:
        if conn:
            conn.close()

# -------------------------------------------------
# EMAIL VERIFICATION
# -------------------------------------------------
@app.route("/send_code", methods=["POST"])
def send_code():
    data = request.get_json() or {}
    email = data.get("email")

    if not email:
        return jsonify({"success": False, "message": "Email required"}), 400

    code = str(random.randint(100000, 999999))

    try:
        msg = MIMEText(f"Your PLANOVA verification code is: {code}")
        msg["Subject"] = "PLANOVA Verification Code"
        msg["From"] = os.getenv("EMAIL_ADDRESS")
        msg["To"] = email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(
                os.getenv("EMAIL_ADDRESS"),
                os.getenv("EMAIL_APP_PASSWORD")
            )
            server.send_message(msg)

        return jsonify({"success": True, "code": code})

    except Exception as e:
        print("EMAIL ERROR:", e)
        return jsonify({"success": False, "message": "Failed to send email"}), 500

# -------------------------------------------------
# LOGIN
# -------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    conn = get_conn()
    cur = conn.cursor()

    if is_postgres():
        cur.execute("SELECT full_name, password FROM users WHERE email = %s", (email,))
    else:
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
# DELETE ACCOUNT
# -------------------------------------------------
@app.route("/delete-account", methods=["POST"])
def delete_account():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    conn = get_conn()
    cur = conn.cursor()

    if is_postgres():
        cur.execute("SELECT password FROM users WHERE email = %s", (email,))
    else:
        cur.execute("SELECT password FROM users WHERE email = ?", (email,))

    row = cur.fetchone()

    if not row:
        conn.close()
        return jsonify({"success": False, "message": "Account not found"}), 400

    hashed_pw = row[0]

    if not check_password_hash(hashed_pw, password):
        conn.close()
        return jsonify({"success": False, "message": "Incorrect password"}), 400

    if is_postgres():
        cur.execute("DELETE FROM users WHERE email = %s", (email,))
    else:
        cur.execute("DELETE FROM users WHERE email = ?", (email,))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Account deleted"})

# -------------------------------------------------
# CHANGE PASSWORD
# -------------------------------------------------
@app.route("/change-password", methods=["POST"])
def change_password():
    data = request.get_json() or {}
    email = data.get("email")
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    conn = get_conn()
    cur = conn.cursor()

    if is_postgres():
        cur.execute("SELECT password FROM users WHERE email = %s", (email,))
    else:
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

    if is_postgres():
        cur.execute("UPDATE users SET password = %s WHERE email = %s", (new_hashed, email))
    else:
        cur.execute("UPDATE users SET password = ? WHERE email = ?", (new_hashed, email))

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
# Stripe Checkout
# -------------------------------------------------
@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    data = request.get_json() or {}

    line_items = [{
        "price_data": {
            "currency": "gbp",
            "product_data": {"name": "Event Ticket"},
            "unit_amount": 1000
        },
        "quantity": 1
    }]

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=line_items,
        success_url=f"{FRONTEND_URL}/success.html",
        cancel_url=f"{FRONTEND_URL}/checkout.html"
    )

    return jsonify({"sessionId": session.id})

# -------------------------------------------------
# Static
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