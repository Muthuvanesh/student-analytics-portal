import sqlite3

# Connect to academy.db
conn = sqlite3.connect("academy.db")
cursor = conn.cursor()

# Fetch all users from admin_users
cursor.execute("SELECT id, username, role, password_hash, salt FROM admin_users")
users = cursor.fetchall()

print("\n--- 🔐 Admin Users & Gibberish Hashes in academy.db ---")
for user in users:
    print(f"ID:           {user[0]}")
    print(f"Username:     {user[1]}")
    print(f"Role:         {user[2]}")
    print(f"Password Hash:{user[3]}")  # <-- This is the scrambled gibberish!
    print(f"Salt:         {user[4]}")  # <-- This is the unique random string!
    print("-" * 50)

conn.close()