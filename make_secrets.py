import hashlib
import os
import pathlib

# Generate secure salt and hash for Admin123
salt = os.urandom(16)
salt_hex = salt.hex()
password_hash = hashlib.pbkdf2_hmac(
    "sha256",
    b"Admin123",
    salt,
    600000
).hex()

# Ensure .streamlit directory exists and write secrets.toml
pathlib.Path(".streamlit").mkdir(exist_ok=True)
config_content = f"""[admin]
username = "Admin"
salt = "{salt_hex}"
password_hash = "{password_hash}"
"""

pathlib.Path(".streamlit/secrets.toml").write_text(config_content)
print("Successfully generated .streamlit/secrets.toml for user 'Admin'!")