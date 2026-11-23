import sqlite3
import hashlib
import os

# Connect to academy.db
conn = sqlite3.connect("academy.db")
cursor = conn.cursor()

# 1. Create the admin_users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        role TEXT DEFAULT 'Admin',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# 2. Generate secure salt and PBKDF2 hash for password "Admin123"
username = "Admin"
password = b"Admin123"

salt = os.urandom(16)
salt_hex = salt.hex()
password_hash = hashlib.pbkdf2_hmac(
    "sha256",
    password,
    salt,
    600000
).hex()

# 3. Insert the user into the database
try:
    cursor.execute(
        """
        INSERT OR IGNORE INTO admin_users (username, password_hash, salt, role)
        VALUES (?, ?, ?, ?)
        """,
        (username, password_hash, salt_hex, "Admin")
    )
    conn.commit()
    print("✅ Admin user created successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    conn.close()