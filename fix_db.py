import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()

cur.execute("ALTER TABLE users ADD COLUMN password_plain TEXT;")

conn.commit()
conn.close()

print("Column added!")
