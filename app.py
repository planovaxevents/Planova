@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    print(">>> REGISTER ENDPOINT HIT <<<")
    print("Incoming data:", data)

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    # 🔍 Debug input values
    print("Parsed values:", full_name, email, password)

    if not full_name or not email or not password:
        print("❌ Missing fields detected")
        return jsonify({"success": False, "message": "Missing fields"}), 400

    hashed_pw = generate_password_hash(password)

    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        print("📥 Inserting into DB...")

        c.execute("""
            INSERT INTO users (full_name, email, password)
            VALUES (?, ?, ?)
        """, (full_name, email, hashed_pw))

        conn.commit()

        # 🔍 Confirm insert worked
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()

        print("✅ Insert result:", user)

        conn.close()

        return jsonify({"success": True, "message": "Account created!"})

    except sqlite3.IntegrityError as e:
        print("❌ Integrity Error:", e)
        return jsonify({"success": False, "message": "Email already registered"}), 400

    except Exception as e:
        print("❌ UNKNOWN ERROR:", e)
        return jsonify({"success": False, "message": "Server error"}), 500