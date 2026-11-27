import streamlit as st
import sqlite3
import pandas as pd
import base64
import hashlib
import hmac
import os
import secrets
import smtplib
from email.message import EmailMessage
from email.utils import formataddr


from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


from app.risk_engine import compute_batch_risk_scores


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================


st.set_page_config(
    page_title="Student Intelligence Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("ACADEMY_DB_PATH", str(BASE_DIR / "academy.db")))

SIDEBAR_IMAGE_DATA = base64.b64encode(
    (BASE_DIR / "assets" / "library-background.jpg").read_bytes()
).decode("ascii")


# =====================================================
# 2. PROFESSIONAL ENTERPRISE UI & SHOOTING STAR CSS
# =====================================================


st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}


.stApp {
    background: linear-gradient(135deg, #090d16 0%, #0f172a 100%);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}


.block-container {
    max-width: 1440px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}


.brand-panel {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
    padding: 50px 40px;
    border-radius: 24px;
    color: white;
    min-height: 580px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 20px 50px rgba(15, 23, 42, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}


.brand-logo {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
}


.brand-logo span {
    color: #38bdf8;
}


.brand-subtitle {
    font-size: 16px;
    font-weight: 500;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 30px;
}


.brand-description {
    color: #cbd5e1;
    line-height: 1.7;
    font-size: 15px;
    margin-bottom: 35px;
}


.brand-feature-container {
    display: flex;
    flex-direction: column;
    gap: 14px;
}


.brand-feature {
    font-size: 14px;
    font-weight: 500;
    color: #f8fafc;
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(255, 255, 255, 0.05);
    padding: 10px 14px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.04);
}


.stApp:has(.brand-panel) [data-testid="column"]:nth-of-type(2) {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #111827 0%, #0f172a 100%);
    padding: 40px 40px !important;
    border-radius: 24px !important;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border: 1px solid rgba(56, 189, 248, 0.2);
    min-height: 580px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}


.stApp:has(.brand-panel) [data-testid="column"]:nth-of-type(2)::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    background-image:
        radial-gradient(2px 2px at 20px 30px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 40px 70px, #38bdf8, rgba(0,0,0,0)),
        radial-gradient(1px 1px at 90px 40px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 160px 120px, #38bdf8, rgba(0,0,0,0));
    background-repeat: repeat;
    background-size: 200px 200px;
    opacity: 0.3;
}


.shooting-star {
    position: absolute;
    height: 2px;
    background: linear-gradient(90deg, #38bdf8, transparent);
    border-radius: 50%;
    animation: fall 3s linear infinite;
    opacity: 0;
    z-index: 1;
}


.shooting-star:nth-child(1) {
    top: 0%;
    left: 20%;
    animation-delay: 0s;
    animation-duration: 2.5s;
}


.shooting-star:nth-child(2) {
    top: 0%;
    left: 70%;
    animation-delay: 1.2s;
    animation-duration: 3.2s;
}


.shooting-star:nth-child(3) {
    top: 0%;
    left: 40%;
    animation-delay: 2.1s;
    animation-duration: 2.8s;
}


@keyframes fall {
    0% {
        transform: rotate(215deg) translateX(0);
        opacity: 1;
        width: 0px;
    }
    20% {
        width: 100px;
    }
    100% {
        transform: rotate(215deg) translateX(-400px);
        opacity: 0;
        width: 0px;
    }
}


div.stForm {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
    position: relative;
    z-index: 2;
}


h1, h2, h3 {
    color: #ffffff;
    letter-spacing: -0.025em;
    font-weight: 700;
}


.login-header-container {
    text-align: center;
    margin-bottom: 20px;
    position: relative;
    z-index: 2;
}

.login-logo-icon {
    width: 64px;
    height: 64px;
    margin: 0 auto 12px;
    display: grid;
    place-items: center;
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.24);
    border-radius: 18px;
}


.login-heading {
    color: #ffffff;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-bottom: 8px;
}


.login-description {
    color: #94a3b8;
    font-size: 14px;
}


div[data-testid="stTextInput"] label {
    color: #e2e8f0;
    font-weight: 600;
    font-size: 13.5px;
}


.stApp:has(.brand-panel) div[data-testid="stTextInput"] input {
    border-radius: 10px;
    min-height: 48px;
    border: 1px solid rgba(56, 189, 248, 0.4) !important;
    background-color: #172b50 !important;
    color: #f8fafc !important;
    transition: all 0.2s ease;
}


.stApp:has(.brand-panel) div[data-testid="stTextInput"] input::placeholder {
    color: #b6c8df !important;
    opacity: 1;
}


.stApp:has(.brand-panel) div[data-testid="stTextInput"] input:focus {
    background-color: #1e3a8a !important;
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
}


div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    color: white;
    border: none;
    border-radius: 10px;
    height: 48px;
    font-size: 14.5px;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    transition: all 0.2s ease;
}


div[data-testid="stFormSubmitButton"] button:hover {
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.6);
    color: white;
}


.security-note {
    background: rgba(6, 95, 70, 0.3);
    color: #34d399;
    border: 1px solid rgba(52, 211, 153, 0.3);
    padding: 14px;
    border-radius: 10px;
    text-align: center;
    font-size: 12.5px;
    font-weight: 500;
    margin-top: 15px;
    position: relative;
    z-index: 2;
}


[data-testid="stMetric"] {
    background: #ffffff;
    padding: 22px 26px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.04), 0 8px 10px -6px rgba(15, 23, 42, 0.04);
    transition: all 0.3s ease;
}


[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 30px -10px rgba(37, 99, 235, 0.08);
    border-color: #cbd5e1;
}


[data-testid="stMetricLabel"] {
    font-size: 12.5px;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}


[data-testid="stMetricValue"] {
    font-size: 32px;
    font-weight: 800;
    color: #0f172a;
}


[data-testid="stDataFrame"] {
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
}


div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    background-color: #ffffff;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.02);
}


</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. DATABASE CONNECTION
# =====================================================


def get_db_connection():
    conn = sqlite3.connect(
        str(DB_PATH),
        timeout=30
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 30000")
    return conn


# =====================================================
# 4. TABLE INITIALIZATION
# =====================================================


def initialize_database():
    conn = get_db_connection()

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS identity_audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_username TEXT,
                student_code TEXT NOT NULL,
                accessed_at TEXT NOT NULL,
                reason_code TEXT NOT NULL
            )
        """)


        columns = {
            row["name"]
            for row in conn.execute(
                "PRAGMA table_info(identity_audit_log)"
            ).fetchall()
        }


        if "admin_username" not in columns:
            conn.execute("""
                ALTER TABLE identity_audit_log
                ADD COLUMN admin_username TEXT
            """)


        conn.execute("""
            CREATE TABLE IF NOT EXISTS auth_sessions (
                token TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS password_reset_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                code_hash TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                attempts INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


        conn.execute("""
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                full_name TEXT,
                email TEXT,
                role TEXT DEFAULT 'Admin',
                approval_status TEXT NOT NULL DEFAULT 'Approved',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


        admin_columns = {
            row["name"]
            for row in conn.execute(
                "PRAGMA table_info(admin_users)"
            ).fetchall()
        }


        if "full_name" not in admin_columns:
            conn.execute(
                "ALTER TABLE admin_users ADD COLUMN full_name TEXT"
            )


        if "email" not in admin_columns:
            conn.execute(
                "ALTER TABLE admin_users ADD COLUMN email TEXT"
            )

        if "approval_status" not in admin_columns:
            conn.execute(
                "ALTER TABLE admin_users ADD COLUMN approval_status TEXT NOT NULL DEFAULT 'Approved'"
            )


        conn.commit()

    finally:
        conn.close()


# =====================================================
# 5. AUTHENTICATION HELPERS
# =====================================================


def verify_db_user(username_or_email, password):
    conn = get_db_connection()

    try:
        user = conn.execute(
            """
            SELECT
                username,
                password_hash,
                salt,
                role,
                approval_status
            FROM admin_users
            WHERE lower(username) = lower(?)
               OR lower(email) = lower(?)
            ORDER BY CASE
                WHEN lower(username) = lower(?) THEN 0
                ELSE 1
            END
            LIMIT 1
            """,
            (
                username_or_email.strip(),
                username_or_email.strip(),
                username_or_email.strip()
            )
        ).fetchone()


        if not user:
            return None


        salt = bytes.fromhex(user["salt"])


        entered_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            600000
        ).hex()


        if hmac.compare_digest(
            entered_hash,
            user["password_hash"]
        ):
            return {
                "username": user["username"],
                "role": user["role"],
                "approval_status": user["approval_status"],
            }


        return None

    finally:
        conn.close()


def register_new_user(
    username,
    password,
    full_name,
    email
):
    clean_user = username.strip()
    clean_full_name = full_name.strip()
    clean_email = email.strip()


    if not clean_user or not password:
        return False, "Username and password cannot be empty."


    if not clean_full_name:
        return False, "Please enter your full name."


    if not clean_email or "@" not in clean_email:
        return False, "Please enter a valid email address."


    if len(password) < 8:
        return False, "Password must be at least 8 characters long."


    conn = get_db_connection()

    try:
        existing = conn.execute(
            """
            SELECT id
            FROM admin_users
            WHERE lower(username) = lower(?)
               OR lower(email) = lower(?)
            """,
            (clean_user, clean_email)
        ).fetchone()


        if existing:
            return False, "That username or email address is already registered."


        salt = os.urandom(16)
        salt_hex = salt.hex()


        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            600000
        ).hex()


        conn.execute(
            """
            INSERT INTO admin_users
                (
                    username,
                    password_hash,
                    salt,
                    full_name,
                    email,
                    role,
                    approval_status
                )
            VALUES (?, ?, ?, ?, ?, 'Admin', 'Pending')
            """,
            (
                clean_user,
                password_hash,
                salt_hex,
                clean_full_name,
                clean_email
            )
        )


        conn.commit()
        return True, "Administrator access requested. A moderator must approve it before you can sign in."

    except sqlite3.IntegrityError:
        return False, f"Username '{clean_user}' is already taken."

    except Exception:
        return False, "Unable to create the account. Please try again."

    finally:
        conn.close()


def create_auth_session(username):
    token = secrets.token_urlsafe(32)
    conn = get_db_connection()

    try:
        conn.execute(
            "DELETE FROM auth_sessions WHERE username = ?",
            (username,)
        )
        conn.execute(
            "INSERT INTO auth_sessions (token, username) VALUES (?, ?)",
            (token, username)
        )
        conn.commit()
        return token
    finally:
        conn.close()


def restore_auth_session(token):
    if not token:
        return None

    conn = get_db_connection()

    try:
        row = conn.execute(
            "SELECT username FROM auth_sessions WHERE token = ?",
            (token,)
        ).fetchone()
        return row["username"] if row else None
    finally:
        conn.close()


def clear_auth_session(token=None, username=None):
    conn = get_db_connection()

    try:
        if token:
            conn.execute("DELETE FROM auth_sessions WHERE token = ?", (token,))
        elif username:
            conn.execute("DELETE FROM auth_sessions WHERE username = ?", (username,))
        conn.commit()
    finally:
        conn.close()


def get_user_account(username):
    conn = get_db_connection()

    try:
        row = conn.execute(
            """
            SELECT username, role, approval_status
            FROM admin_users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_smtp_setting(name, default=""):
    value = os.getenv(name) or os.getenv(name.upper()) or os.getenv(name.lower())
    if value:
        return value
    try:
        smtp_settings = st.secrets.get("smtp", {})
        short_name = name.lower().replace("smtp_", "")
        return str(
            smtp_settings.get(name.lower(),
                smtp_settings.get(name.upper(),
                    smtp_settings.get(name,
                        smtp_settings.get(short_name, default))))
        )
    except Exception:
        return default


def send_password_reset_email(email, code):
    host = get_smtp_setting("SMTP_HOST")
    port = int(get_smtp_setting("SMTP_PORT", "587") or "587")
    username = get_smtp_setting("SMTP_USER").strip()
    password = get_smtp_setting("SMTP_PASSWORD").replace(" ", "")
    sender = get_smtp_setting("SMTP_FROM", username).strip()
    sender_name = get_smtp_setting("SMTP_FROM_NAME", "Student Portal (No-Reply)").strip()
    reply_to = get_smtp_setting("SMTP_REPLY_TO", "no-reply@studentportal.edu").strip()

    if not host or not sender:
        raise RuntimeError("Email service is not configured.")

    message = EmailMessage()
    message["Subject"] = f"{sender_name} - Password Reset Code"
    message["From"] = formataddr((sender_name, sender))
    message["Reply-To"] = formataddr((sender_name, reply_to))
    message["To"] = email

    # Plain text fallback
    text_content = (
        f"Hello,\n\n"
        f"You requested a password reset for your {sender_name} account.\n\n"
        f"Your 6-digit reset code is: {code}\n\n"
        f"This code will expire in 10 minutes.\n"
        f"If you did not request this reset, please ignore this email.\n\n"
        f"Note: This is an automated email from an unattended mailbox. Please do not reply.\n\n"
        f"Regards,\n"
        f"{sender_name} Team"
    )
    message.set_content(text_content)

    # HTML formatted email
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 24px; margin: 0;">
        <div style="max-width: 480px; margin: 0 auto; background: #1e293b; border-radius: 12px; padding: 28px; border: 1px solid rgba(255,255,255,0.12);">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                <span style="font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: #94a3b8; font-weight: 600;">
                    Automated Notification • No-Reply
                </span>
            </div>
            <h2 style="margin-top: 4px; color: #60a5fa; font-size: 20px;">🎓 Password Reset Code</h2>
            <p style="color: #cbd5e1; font-size: 14px; line-height: 1.6;">
                We received a request to reset your password for <strong>{sender_name}</strong>. Use the verification code below to set a new password:
            </p>
            <div style="margin: 22px 0; text-align: center;">
                <span style="display: inline-block; font-size: 30px; font-weight: 700; letter-spacing: 6px; color: #ffffff; background: #2563eb; padding: 12px 24px; border-radius: 8px;">
                    {code}
                </span>
            </div>
            <p style="color: #94a3b8; font-size: 13px; line-height: 1.5;">
                ⏱️ This code will expire in <strong>10 minutes</strong>.<br>
                If you did not request this, you can safely ignore this email.
            </p>
            <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 20px 0;">
            <p style="color: #64748b; font-size: 11px; line-height: 1.5; margin-bottom: 0;">
                ℹ️ <strong>Please do not reply:</strong> This email was sent from an automated, unmonitored notification address (<span style="color:#94a3b8;">{reply_to}</span>). Replies to this email cannot be received or answered.<br><br>
                {sender_name} • Automated Security System
            </p>
        </div>
    </body>
    </html>
    """
    message.add_alternative(html_content, subtype="html")

    if port == 465:
        with smtplib.SMTP_SSL(host, port, timeout=15) as smtp:
            if username:
                smtp.login(username, password)
            smtp.send_message(message)
    else:
        with smtplib.SMTP(host, port, timeout=15) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            if username:
                smtp.login(username, password)
            smtp.send_message(message)


def request_password_reset(email):
    clean_email = email.strip().lower()
    if "@" not in clean_email:
        return False, "Please enter a valid email address."

    conn = get_db_connection()
    try:
        user = conn.execute(
            """
            SELECT username
            FROM admin_users
            WHERE lower(email) = ?
            """,
            (clean_email,)
        ).fetchone()
    finally:
        conn.close()

    if not user:
        return True, "If an account exists for that email, a reset code will be sent."

    code = f"{secrets.randbelow(1000000):06d}"
    code_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
    expires_at = (datetime.now(ZoneInfo("Asia/Kolkata")) + timedelta(minutes=10)).isoformat()

    conn = get_db_connection()
    try:
        conn.execute(
            "DELETE FROM password_reset_codes WHERE username = ?",
            (user["username"],)
        )
        conn.execute(
            """
            INSERT INTO password_reset_codes
                (username, code_hash, expires_at)
            VALUES (?, ?, ?)
            """,
            (user["username"], code_hash, expires_at)
        )
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        return False, "Unable to create a password reset request."
    finally:
        conn.close()

    try:
        send_password_reset_email(clean_email, code)
        return True, "A password reset code was sent to your email."
    except RuntimeError:
        # Dev fallback when SMTP is not configured
        print(f"[AUTH DEV] Password reset code for {clean_email}: {code}")
        return True, f"Email service is not configured. For testing, your reset code is: {code}"
    except Exception as exc:
        conn = get_db_connection()
        try:
            conn.execute(
                "DELETE FROM password_reset_codes WHERE username = ?",
                (user["username"],)
            )
            conn.commit()
        finally:
            conn.close()
        return False, f"Unable to send the reset email ({exc}). Please verify your SMTP settings and try again."


def reset_password(email, code, new_password, confirm_password):
    clean_email = email.strip().lower()
    clean_code = code.strip()

    if len(new_password) < 8:
        return False, "Password must be at least 8 characters long."
    if new_password != confirm_password:
        return False, "Passwords do not match."
    if not clean_code.isdigit() or len(clean_code) != 6:
        return False, "Enter the 6-digit reset code."

    conn = get_db_connection()
    try:
        user = conn.execute(
            """
            SELECT username
            FROM admin_users
            WHERE lower(email) = ?
            """,
            (clean_email,)
        ).fetchone()
        if not user:
            return False, "Invalid reset request."

        reset = conn.execute(
            """
            SELECT code_hash, expires_at, attempts
            FROM password_reset_codes
            WHERE username = ?
            """,
            (user["username"],)
        ).fetchone()
        if not reset:
            return False, "Reset code expired or not found."

        expires_at = datetime.fromisoformat(reset["expires_at"])
        if datetime.now(expires_at.tzinfo) > expires_at:
            conn.execute(
                "DELETE FROM password_reset_codes WHERE username = ?",
                (user["username"],)
            )
            conn.commit()
            return False, "Reset code expired."

        if reset["attempts"] >= 5:
            return False, "Too many invalid attempts. Request a new reset code."

        code_hash = hashlib.sha256(clean_code.encode("utf-8")).hexdigest()
        if not hmac.compare_digest(code_hash, reset["code_hash"]):
            conn.execute(
                """
                UPDATE password_reset_codes
                SET attempts = attempts + 1
                WHERE username = ?
                """,
                (user["username"],)
            )
            conn.commit()
            return False, "Invalid reset code."

        salt = os.urandom(16)
        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            new_password.encode("utf-8"),
            salt,
            600000
        ).hex()

        conn.execute(
            """
            UPDATE admin_users
            SET password_hash = ?, salt = ?
            WHERE username = ?
            """,
            (password_hash, salt.hex(), user["username"])
        )
        conn.execute(
            "DELETE FROM password_reset_codes WHERE username = ?",
            (user["username"],)
        )
        conn.execute(
            "DELETE FROM auth_sessions WHERE username = ?",
            (user["username"],)
        )
        conn.commit()
        return True, "Password changed successfully."
    except sqlite3.Error:
        conn.rollback()
        return False, "Unable to reset the password. Please try again."
    finally:
        conn.close()


# =====================================================
# 6. SESSION STATE
# =====================================================


# Do not restore login state from URL query parameters.
# URL parameters are visible, editable, and shareable.


st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("admin_username", None)
st.session_state.setdefault("admin_role", None)
st.session_state.setdefault("auth_page", "Sign In")
st.session_state.setdefault("registration_success", False)
st.session_state.setdefault("auth_token", None)
st.session_state.setdefault("account_menu_open", False)
st.session_state.setdefault("reset_email", "")
st.session_state.setdefault("clear_signup_passwords", False)
st.session_state.setdefault("signup_password_error", "")


def set_auth_page(page_name):
    st.session_state["auth_page"] = page_name


def clear_registration_passwords(message):
    st.session_state["clear_signup_passwords"] = True
    st.session_state["signup_password_error"] = message
    st.rerun()


# =====================================================
# 7. INITIALIZE DATABASE
# =====================================================


try:
    initialize_database()
except sqlite3.Error:
    st.error("Unable to initialize the database.")
    st.stop()


if not st.session_state["logged_in"] and not st.session_state["auth_token"]:
    query_token = st.query_params.get("auth")
    restored_username = restore_auth_session(query_token)

    if restored_username:
        restored_user = get_user_account(restored_username)
        if (
            restored_user
            and restored_user["approval_status"] == "Approved"
            and restored_user["role"] in ["Admin", "Super Admin", "Moderator"]
        ):
            st.session_state["logged_in"] = True
            st.session_state["admin_username"] = restored_username
            st.session_state["admin_role"] = restored_user["role"]
            st.session_state["auth_token"] = query_token


# =====================================================
# 8. LOGIN & REGISTRATION INTERFACE
# =====================================================


if not st.session_state["logged_in"]:

    st.markdown("""
    <style>
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border: 1px solid #2563eb !important;
        border-radius: 10px;
        -webkit-tap-highlight-color: transparent;
        transition: background 0.2s ease, box-shadow 0.2s ease;
    }

    div[data-testid="stButton"] > button:hover,
    div[data-testid="stButton"] > button:focus,
    div[data-testid="stButton"] > button:focus-visible,
    div[data-testid="stButton"] > button:active {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
        color: #ffffff !important;
        border-color: #1d4ed8 !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    left, right = st.columns(
        [1.1, 1],
        gap="large"
    )


    with left:
        raw_html = """
        <div class="brand-panel">
            <div class="brand-subtitle">Student Success Platform</div>
            <div class="brand-logo">
                <span>Student</span><span>Intelligence</span>
            </div>
            <h2 style="font-size:24px; font-weight:700; margin-bottom:15px; letter-spacing:-0.5px;">
                Monitor. Predict. Support.
            </h2>
            <p class="brand-description">
                Track academic progress, spot emerging concerns, and coordinate timely student support.
            </p>
            <div class="brand-feature-container">
                <div class="brand-feature">
                    &#128202; &nbsp; Real-time Performance & Attendance Tracking
                </div>
                <div class="brand-feature">
                    &#128737; &nbsp; Predictive Student At-Risk Analysis
                </div>
                <div class="brand-feature">
                    &#129309; &nbsp; Streamlined Faculty Intervention Workflows
                </div>
                <div class="brand-feature">
                    &#128274; &nbsp; Fully Audited Secure Identity Access
                </div>
            </div>
        </div>
        """


        cleaned_html = "\n".join(
            line.strip()
            for line in raw_html.strip().splitlines()
        )


        st.markdown(cleaned_html, unsafe_allow_html=True)


    with right:
        st.markdown("""
        <div class="shooting-star"></div>
        <div class="shooting-star"></div>
        <div class="shooting-star"></div>
        """, unsafe_allow_html=True)

        login_header_title = "Welcome back"
        login_header_description = "Sign in to your account"
        if st.session_state["auth_page"] == "Forgot Password":
            login_header_title = "Reset password"
            login_header_description = "Use the verification code sent to your email"
        elif st.session_state["auth_page"] != "Sign In":
            login_header_title = "Request administrator access"
            login_header_description = "A moderator must approve your account"

        raw_header_html = f"""
        <div class="login-header-container">
            <div class="login-logo-icon" role="img" aria-label="Graduation cap">
                <svg width="36" height="36" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                    <path d="M4 17L24 7L44 17L24 27L4 17Z" stroke="currentColor" stroke-width="2.8" stroke-linejoin="round"/>
                    <path d="M12 21V31C19 36 29 36 36 31V21" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M44 17V29" stroke="currentColor" stroke-width="2.8" stroke-linecap="round"/>
                    <circle cx="44" cy="31" r="2" fill="currentColor"/>
                </svg>
            </div>
            <div class="login-heading">{login_header_title}</div>
            <div class="login-description">{login_header_description}</div>
        </div>
        """


        st.markdown(
            "\n".join(
                line.strip()
                for line in raw_header_html.strip().splitlines()
            ),
            unsafe_allow_html=True
        )


        if st.session_state.get("registration_success"):
            st.toast(
                "Access request submitted. Please wait for moderator approval."
            )
            st.session_state["registration_success"] = False


        if st.session_state["auth_page"] == "Sign In":
            with st.form("professional_login"):
                username = st.text_input(
                    "Username or email",
                    placeholder="Enter your username or email address",
                    key="login_user"
                )


                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    key="login_pass"
                )


                st.markdown(
                    "<div style='height: 5px;'></div>",
                    unsafe_allow_html=True
                )


                submit = st.form_submit_button(
                    "Sign In to Console",
                    use_container_width=True
                )


                if submit:
                    if not username.strip() or not password:
                        st.error("Please enter your username or email and password.")
                    else:
                        user = verify_db_user(username, password)


                        if user:
                            if user["approval_status"] == "Pending":
                                st.info("Your account is awaiting moderator approval.")
                            elif user["approval_status"] == "Blocked":
                                st.error("This account has been blocked by a moderator.")
                            elif user["approval_status"] != "Approved":
                                st.error("This account has not been approved for access.")
                            else:
                                st.session_state["logged_in"] = True
                                st.session_state["admin_username"] = user["username"]
                                st.session_state["admin_role"] = user["role"]
                                st.session_state["auth_token"] = create_auth_session(user["username"])
                                st.query_params["auth"] = st.session_state["auth_token"]
                                st.rerun()
                        else:
                            st.error("Invalid username, email, or password.")


            st.button(
                "Forgot password?",
                use_container_width=True,
                on_click=set_auth_page,
                args=("Forgot Password",)
            )


            st.markdown(
                "<div style='text-align:center; color:#94a3b8; font-size:13px; margin-top:18px;'>"
                "Don't have an account?"
                "</div>",
                unsafe_allow_html=True
            )
            st.button(
                "Create new account",
                use_container_width=True,
                on_click=set_auth_page,
                args=("Create Account",)
            )

        elif st.session_state["auth_page"] == "Forgot Password":
            reset_email = st.text_input(
                "Email address",
                value=st.session_state["reset_email"],
                placeholder="Enter your registered email address",
                key="reset_email_input"
            )

            if st.button("Send reset code", use_container_width=True, type="primary"):
                success, message = request_password_reset(reset_email)
                if success:
                    st.session_state["reset_email"] = reset_email.strip().lower()
                    st.success(message)
                else:
                    st.error(message)

            if st.session_state["reset_email"]:
                with st.form("reset_password_form"):
                    reset_code = st.text_input(
                        "6-digit reset code",
                        placeholder="Enter the code from your email",
                        key="reset_code"
                    )
                    reset_password_value = st.text_input(
                        "New password",
                        type="password",
                        placeholder="Enter a new password",
                        key="reset_new_password"
                    )
                    reset_confirm_password = st.text_input(
                        "Confirm new password",
                        type="password",
                        placeholder="Re-enter the new password",
                        key="reset_confirm_password"
                    )
                    reset_submit = st.form_submit_button(
                        "Change password",
                        use_container_width=True
                    )

                    if reset_submit:
                        success, message = reset_password(
                            st.session_state["reset_email"],
                            reset_code,
                            reset_password_value,
                            reset_confirm_password
                        )
                        if success:
                            st.session_state["reset_email"] = ""
                            st.session_state["auth_page"] = "Sign In"
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

            st.button(
                "Back to sign in",
                use_container_width=True,
                on_click=set_auth_page,
                args=("Sign In",)
            )

        else:
            if st.session_state["clear_signup_passwords"]:
                st.session_state["signup_pass"] = ""
                st.session_state["signup_confirm"] = ""
                st.session_state["clear_signup_passwords"] = False

            if st.session_state["signup_password_error"]:
                st.error(st.session_state["signup_password_error"])
                st.session_state["signup_password_error"] = ""

            with st.form("facebook_style_signup", clear_on_submit=False):
                full_name = st.text_input(
                    "Full name",
                    placeholder="Enter your full name",
                    key="signup_full_name"
                )


                new_username = st.text_input(
                    "Username",
                    placeholder="Choose a username",
                    key="signup_user"
                )


                email = st.text_input(
                    "Email address",
                    placeholder="Enter your email address",
                    key="signup_email"
                )


                col_pass, col_confirm = st.columns(2)


                with col_pass:
                    new_password = st.text_input(
                        "Password",
                        type="password",
                        placeholder="Create a password",
                        key="signup_pass"
                    )


                with col_confirm:
                    confirm_password = st.text_input(
                        "Confirm password",
                        type="password",
                        placeholder="Re-enter password",
                        key="signup_confirm"
                    )


                st.info(
                    "New accounts request administrator access and cannot sign in until a moderator approves them."
                )


                st.markdown(
                    """
                    <div style="
                        color:#64748b;
                        font-size:12px;
                        margin-top:10px;
                        text-align:center;
                    ">
                        By creating an account, you agree to follow your institution’s
                        data-access and compliance policies.
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.markdown(
                    "<div style='height: 8px;'></div>",
                    unsafe_allow_html=True
                )


                submit_signup = st.form_submit_button(
                    "Request administrator access",
                    use_container_width=True
                )


                if submit_signup:
                    if not full_name.strip():
                        st.error("Please enter your full name.")


                    elif not new_username.strip():
                        st.error("Please choose a username.")


                    elif not email.strip() or "@" not in email:
                        st.error("Please enter a valid email address.")


                    elif not new_password:
                        clear_registration_passwords("Please create a password.")


                    elif len(new_password) < 8:
                        clear_registration_passwords(
                            "Password must be at least 8 characters long."
                        )


                    elif new_password != confirm_password:
                        clear_registration_passwords("Passwords do not match.")


                    else:
                        success, message = register_new_user(
                            new_username,
                            new_password,
                            full_name,
                            email
                        )


                        if success:
                            st.session_state["registration_success"] = True
                            st.session_state["auth_page"] = "Sign In"
                        else:
                            st.error(f"{message}")

            st.button(
                "Back to sign in",
                use_container_width=True,
                on_click=set_auth_page,
                args=("Sign In",)
            )


    st.stop()


# =====================================================
# =====================================================================
# PASTE THIS BLOCK IN PLACE OF EVERYTHING FROM
#   "# 9. AUTHORIZATION CHECK"   down to the end of your file.
# Sections 1-8 (page config, CSS, database, auth helpers, session
# state, login and registration UI) stay exactly as they are.
# =====================================================================

import html


# =====================================================
# 9. AUTHORIZATION CHECK
# =====================================================


current_username = st.session_state["admin_username"]
current_account = get_user_account(current_username) if current_username else None
current_role = current_account["role"] if current_account else None

ADMIN_ROLES = {"Admin", "Super Admin"}
MODERATOR_ROLES = {"Moderator"}
FULL_ACCESS_ROLES = ADMIN_ROLES | MODERATOR_ROLES
APPROVER_ROLES = MODERATOR_ROLES

if (
    not current_username
    or not current_account
    or current_account["approval_status"] != "Approved"
    or current_role not in FULL_ACCESS_ROLES
):
    clear_auth_session(token=st.session_state.get("auth_token"))
    st.session_state["logged_in"] = False
    st.session_state["admin_username"] = None
    st.session_state["admin_role"] = None
    st.session_state["auth_token"] = None

    if "auth" in st.query_params:
        del st.query_params["auth"]

    st.error("Your account is not authorized to access this console.")
    st.stop()


# =====================================================
# 10. DASHBOARD THEME
# =====================================================


DASHBOARD_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

:root {
    --ink: #0f172a;
    --muted: #5b6b82;
    --line: #e3e9f1;
    --surface: #ffffff;
    --canvas: #f5f7fa;
    --accent: #0369a1;
    --accent-soft: #e0f2fe;
    --high: #dc2626;
    --med: #f59e0b;
    --low: #22c55e;
}

.stApp,
.stApp p,
.stApp label,
.stApp input,
.stApp button,
.stApp [data-testid="stMarkdownContainer"] {
    font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.stApp {
    background: var(--canvas) !important;
}

header {
    visibility: visible !important;
    background: transparent !important;
}

[data-testid="stToolbar"] {
    display: flex !important;
}

[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: relative;
    z-index: 1001;
}

[data-testid="stSidebarCollapseButton"] button,
[data-testid="collapsedControl"] button {
    width: 34px;
    height: 34px;
    min-width: 34px;
    border: 1px solid var(--line);
    border-radius: 8px;
    background: var(--surface);
    color: var(--accent);
}

section[data-testid="stMain"] .block-container,
.block-container {
    max-width: 1380px;
    padding: 1.2rem 2rem 2rem !important;

}

/* ---------- Sidebar ---------- */

[data-testid="stSidebar"] {
    min-width: 260px;
    max-width: 260px;
}

[data-testid="stSidebar"][data-collapsed="true"] {
    width: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
}

section[data-testid="stSidebar"] {
    background: #eef4fa;
    border-right: 1px solid var(--line);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.25rem;
}

.side-brand {
    margin: 0 4px 18px;
    padding: 16px 16px 15px;
    border-radius: 10px;
    background: #0f172a;
}

.side-brand-title {
    color: #ffffff;
    font-size: 17px;
    font-weight: 600;
    line-height: 1.25;
}

.side-brand-sub {
    color: #7dd3fc;
    font-size: 12.5px;
    margin-top: 4px;
}

.workspace-section-label {
    margin: 0 6px 6px;
    padding: 9px 10px 8px;
    border-bottom: 1px solid #d5e0eb;
    color: var(--muted);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    min-height: 46px;
    margin: 2px 0;
    padding: 9px 12px;
    border-radius: 8px;
    color: var(--ink);
    font-size: 14.5px;
    font-weight: 500;
    border: 1px solid transparent;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(3, 105, 161, 0.07);
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: #ffffff;
    color: var(--ink);
    font-weight: 600;
    border-color: #bfdbfe;
    box-shadow: inset 3px 0 0 var(--accent);
}

section[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 2px;
}

section[data-testid="stSidebar"] [role="radio"] {
    display: none;
}

.side-user {
    margin: 22px 4px 0;
    padding-top: 14px;
    border-top: 1px solid #cfe0f1;
    display: flex;
    align-items: center;
    gap: 10px;
}

.side-user-avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: var(--accent);
    color: #ffffff;
    font-size: 13px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.side-user-name {
    color: var(--ink);
    font-size: 13.5px;
    font-weight: 600;
    line-height: 1.2;
}

.side-user-role {
    color: var(--muted);
    font-size: 12px;
}

.side-version {
    margin: 14px 4px 0;
    color: var(--muted);
    font-size: 11.5px;
}

/* ---------- Typography ---------- */

.stApp h1,
.stApp h2,
.stApp h3,
.stApp [data-testid="stWidgetLabel"] * {
    color: var(--ink) !important;
}

.stApp h3 {
    font-size: 18px;
    font-weight: 600;
    letter-spacing: -0.01em;
}

.page-title {
    color: var(--ink);
    font-size: 27px;
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1.2;
}

.page-subtitle {
    color: var(--muted);
    font-size: 14px;
    margin-top: 4px;
}

.meta-row {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 14px;
}

.meta-date {
    color: var(--muted);
    font-size: 13px;
}

.pill {
    background: var(--accent-soft);
    color: #075985;
    font-size: 13px;
    font-weight: 600;
    padding: 5px 12px;
    border-radius: 999px;
}

.section-note {
    color: var(--muted);
    font-size: 13.5px;
    margin: -4px 0 14px;
}

/* ---------- Summary strip and composition bar ---------- */

.summary-panel {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 22px 26px 20px;
    margin-bottom: 20px;
}

.stat-strip {
    display: flex;
    align-items: stretch;
}

.stat {
    flex: 1;
    padding: 0 26px;
    border-left: 1px solid var(--line);
}

.stat:first-child {
    padding-left: 0;
    border-left: none;
}

.stat-label {
    color: var(--muted);
    font-size: 13.5px;
    font-weight: 500;
}

.stat-value {
    color: var(--ink);
    font-size: 38px;
    font-weight: 600;
    line-height: 1.15;
    margin: 4px 0 2px;
    font-variant-numeric: tabular-nums;
}

.stat-value.high { color: #b91c1c; }
.stat-value.med { color: #b45309; }
.stat-value.low { color: #15803d; }

.stat-note {
    color: var(--muted);
    font-size: 12.5px;
}

.comp-bar {
    display: flex;
    height: 14px;
    border-radius: 7px;
    overflow: hidden;
    background: #e5e9f0;
    margin-top: 22px;
    gap: 2px;
}

.seg-high { background: var(--high); }
.seg-med { background: var(--med); }
.seg-low { background: var(--low); }
.seg-other { background: #94a3b8; }

.comp-legend {
    display: flex;
    gap: 22px;
    margin-top: 10px;
    color: var(--muted);
    font-size: 13px;
}

.comp-legend span {
    display: inline-flex;
    align-items: center;
    gap: 7px;
}

.dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    display: inline-block;
}

/* ---------- Watchlist ---------- */

.watch-head {
    color: var(--ink);
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 2px;
}

.watch-sub {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 12px;
}

.watch-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 11px 0;
    border-top: 1px solid var(--line);
}

.watch-code {
    color: var(--ink);
    font-size: 14.5px;
    font-weight: 600;
}

.watch-meta {
    color: var(--muted);
    font-size: 12.5px;
    margin-top: 2px;
}

.trend-icon {
    width: 26px;
    height: 26px;
    vertical-align: middle;
    margin-left: 4px;
}

.trend-status {
    margin-left: 4px;
    font-weight: 600;
    vertical-align: middle;
}

.trend-declining {
    color: #dc2626;
}

.trend-stable {
    color: #16a34a;
}

@keyframes trend-shine {
    from {
        opacity: 0.72;
        text-shadow: 0 0 0 transparent;
        filter: drop-shadow(0 0 0 transparent);
    }
    to {
        opacity: 1;
        text-shadow: 0 0 7px currentColor;
        filter: drop-shadow(0 0 5px currentColor);
    }
}

.trend-icon.trend-declining,
.trend-status.trend-declining {
    animation: trend-shine 1.3s ease-in-out infinite alternate;
}

@media (prefers-reduced-motion: reduce) {
    .trend-icon.trend-declining,
    .trend-status.trend-declining {
        animation: none;
    }
}

.watch-score {
    color: var(--ink);
    font-size: 20px;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
}

.chip {
    display: inline-block;
    font-size: 12px;
    font-weight: 600;
    padding: 2px 9px;
    border-radius: 999px;
    margin-right: 6px;
}

.chip-high { background: #fee2e2; color: #991b1b; }
.chip-medium { background: #fef3c7; color: #92400e; }
.chip-low { background: #dcfce7; color: #166534; }

/* ---------- Identity result ---------- */

.id-card-top {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 16px;
}

.id-avatar {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: var(--accent-soft);
    color: #075985;
    font-size: 19px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.id-name {
    color: var(--ink);
    font-size: 21px;
    font-weight: 600;
    line-height: 1.2;
}

.id-code {
    color: var(--muted);
    font-size: 13.5px;
    margin-top: 2px;
}

.id-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-top: 1px solid var(--line);
    font-size: 14px;
}

.id-row span:first-child {
    color: var(--muted);
}

.id-row span:last-child {
    color: var(--ink);
    font-weight: 500;
}

.id-row .id-email {
    overflow-wrap: anywhere;
    text-align: right;
}

.empty-state {
    padding: 34px 10px;
    text-align: center;
    color: var(--muted);
    font-size: 14px;
    line-height: 1.6;
}

.empty-state strong {
    display: block;
    color: var(--ink);
    font-size: 16px;
    margin-bottom: 4px;
}

/* ---------- Widgets ---------- */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface);
    border-color: var(--line) !important;
    border-radius: 10px !important;
}

.stApp [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
.stApp [data-testid="stTextInput"] input,
.stApp [data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border-color: var(--line) !important;
    border-radius: 8px !important;
}

.stApp [data-testid="stTextInput"] input {
    color: var(--ink) !important;
}

.stApp button[kind="primary"] {
    background: var(--accent);
    border: 1px solid var(--accent);
    border-radius: 8px;
    color: #ffffff;
    font-weight: 600;
}

.stApp button[kind="primary"]:hover {
    background: #075985;
    border-color: #075985;
    color: #ffffff;
}

.stApp button[kind="secondary"] {
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    background: #ffffff;
    color: var(--ink);
}

.stApp [data-testid="stDataFrame"] {
    background: #ffffff;
    border: 1px solid var(--line);
    border-radius: 8px;
    box-shadow: none;
}

.stApp [data-testid="stCaptionContainer"] {
    color: var(--muted);
}

hr {
    border-color: var(--line);
}

.footer-note {
    text-align: center;
    color: var(--muted);
    font-size: 12.5px;
    padding: 6px 0 12px;
}

/* ---------- Account avatar popover ---------- */

[data-testid="stPopover"] button svg,
[data-testid="stPopover"] button [aria-label="expand_more"],
[data-testid="stPopover"] button [aria-label="expand_less"],
[data-testid="stPopover"] button [aria-label="expand_more"] + *,
[data-testid="stPopover"] button [aria-label="expand_less"] + * {
    display: none !important;
}

[data-testid="stPopover"] button {
    width: 38px !important;
    min-width: 38px !important;
    height: 38px !important;
    min-height: 38px !important;
    max-height: 38px !important;
    padding: 0 !important;
    position: relative !important;
    border: 2px solid #ffffff !important;
    border-radius: 50% !important;
    background: var(--accent) !important;
    color: #ffffff !important;
    box-shadow: 0 0 0 1px var(--line) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    line-height: 38px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

[data-testid="stPopover"] button > div > div:last-child,
[data-testid="stPopover"] button > div > span:last-child,
[data-testid="stPopover"] button > div > svg:last-child {
    display: none !important;
}

[data-testid="stPopover"] button p {
    display: flex !important;
    position: absolute !important;
    inset: 0 !important;
    width: 38px !important;
    height: 38px !important;
    margin: 0 !important;
    padding: 0 !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    line-height: 38px !important;
    font-size: 14px !important;
    color: #ffffff !important;
}

.pop-name {
    color: var(--ink);
    font-size: 14px;
    font-weight: 600;
}

.pop-role {
    color: var(--muted);
    font-size: 12.5px;
    margin: 2px 0 10px;
}
</style>
"""

st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)


# =====================================================
# 11. HELPERS
# =====================================================


BAND_ORDER = ["High", "Medium", "Low"]

REASON_LABELS = {
    "COUNSELING_INTERVENTION": "Counseling intervention",
    "ACADEMIC_ADVISING": "Academic advising",
    "PARENT_MEETING": "Parent meeting",
}


def now_ist():
    return datetime.now(ZoneInfo("Asia/Kolkata"))


def esc(value):
    return "" if value is None else html.escape(str(value))


def trend_image(declining):
    if declining:
        symbol = '<path d="M16 4h8v18h10L20 36 6 22h10z" fill="#dc2626"/>'
    else:
        symbol = '<path d="M5 16h27m-8-8 8 8-8 8" stroke="#16a34a" stroke-width="4"/>'
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" '
        'viewBox="0 0 40 40" fill="none">'
        f'<g stroke-linecap="round" stroke-linejoin="round">{symbol}</g>'
        '</svg>'
    )
    return "data:image/svg+xml;base64," + base64.b64encode(
        svg.encode("utf-8")
    ).decode("ascii")


def reason_label(code):
    return REASON_LABELS.get(code, str(code).replace("_", " ").capitalize())


def render_html(raw):
    # Single-line HTML so Markdown never treats indentation as a code block.
    st.markdown(
        "".join(line.strip() for line in raw.strip().splitlines()),
        unsafe_allow_html=True
    )


def initials(name):
    parts = [part for part in str(name or "").split() if part]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:1].upper()
    return (parts[0][:1] + parts[-1][:1]).upper()


@st.cache_data(ttl=60, show_spinner="Loading cohort data...")
def load_cohort(batch, db_path):
    results = compute_batch_risk_scores(batch, db_path=db_path)
    students = [
        {**student, "batch_id": batch}
        for student in results.get("students", [])
    ]
    return students, now_ist().strftime("%d %b %Y, %H:%M IST")


def get_batch_ids():
    conn = get_db_connection()

    try:
        rows = conn.execute(
            """
            SELECT DISTINCT batch_id
            FROM students_identity
            WHERE batch_id IS NOT NULL AND TRIM(batch_id) != ''
            ORDER BY batch_id
            """
        ).fetchall()
    finally:
        conn.close()

    return sorted({row["batch_id"] for row in rows} | {"PY-2026-05"})


def band_chip(band):
    css = {"High": "chip-high", "Medium": "chip-medium", "Low": "chip-low"}.get(band, "chip-low")
    return f'<span class="chip {css}">{esc(band)}</span>'


def highlight_risk(value):
    if value == "High":
        return "background-color:#fee2e2; color:#991b1b; font-weight:600;"
    if value == "Medium":
        return "background-color:#fef3c7; color:#92400e; font-weight:600;"
    return "background-color:#dcfce7; color:#166534; font-weight:600;"


def highlight_trend(value):
    if value.startswith("↓"):
        return "color:#dc2626; font-weight:700;"
    return "color:#16a34a; font-weight:700;"


# =====================================================
# 12. SIDEBAR
# =====================================================


portal_label = (
    "Administration portal"
    if current_role in ADMIN_ROLES
    else "Moderator portal"
)

render_html(f"""
<div class="side-brand" style="background-image:linear-gradient(180deg,rgba(15,23,42,.18),rgba(15,23,42,.82)),url('data:image/jpeg;base64,{SIDEBAR_IMAGE_DATA}');background-size:cover;background-position:center 58%;">
    <div class="side-brand-title">Student Intelligence</div>
    <div class="side-brand-sub">{esc(portal_label)}</div>
</div>
""")

with st.sidebar:
    st.markdown(
        '<div class="workspace-section-label" aria-hidden="true">Workspace</div>',
        unsafe_allow_html=True
    )

NAV_LABELS = {
    "Risk Analytics": "Risk Analytics",
    "Identity Lookup": "Identity Lookup",
    "Compliance Audit": "Compliance Audit",
    "User Approvals": "User Approvals",
}
ALL_BATCHES = "All batches"
admin_views = [
    "Risk Analytics",
    "Identity Lookup",
    "Compliance Audit",
]
moderator_views = [
    "Risk Analytics",
    "Identity Lookup",
    "Compliance Audit",
    "User Approvals",
]
available_views = (
    moderator_views
    if current_role in MODERATOR_ROLES
    else admin_views
    if current_role in ADMIN_ROLES
    else ["Risk Analytics", "User Approvals"]
)

active_view = st.sidebar.radio(
    "Workspace",
    available_views,
    format_func=lambda key: NAV_LABELS[key],
    label_visibility="collapsed",
    key=f"workspace_{current_role}"
)

if active_view == "User Approvals" and current_role not in APPROVER_ROLES:
    st.error("Your role does not have permission to approve account requests.")
    st.stop()

batch_ids = get_batch_ids()
batch_id = st.sidebar.selectbox(
    "Cohort",
    [ALL_BATCHES, *batch_ids],
    index=0,
    key="cohort_selector"
)
is_overall = batch_id == ALL_BATCHES

if st.sidebar.button("Refresh data", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

with st.sidebar:
    render_html(f"""
    <div class="side-user">
        <div class="side-user-avatar">{esc(current_username[:1].upper())}</div>
        <div>
            <div class="side-user-name">{esc(current_username)}</div>
            <div class="side-user-role">{esc(current_role)}</div>
        </div>
    </div>
    <div class="side-version">Enterprise console v1.1</div>
    """)


# =====================================================
# 13. PAGE HEADER
# =====================================================


VIEW_TITLES = {
    "Risk Analytics": ("Risk analytics", "Where each student stands and who needs support first."),
    "Identity Lookup": ("Identity lookup", "Reveal a student's identity for an approved purpose. Every lookup is logged."),
    "Compliance Audit": ("Compliance audit", "A record of who accessed student identities, when and why."),
    "User Approvals": ("User approvals", "Approve pending administrator accounts."),
}
page_title, page_subtitle = VIEW_TITLES[active_view]
cohort_label = "Overall" if is_overall else f"Cohort {batch_id}"

header_left, header_mid, header_right = st.columns(
    [6, 3.4, 0.8],
    vertical_alignment="center"
)

with header_left:
    render_html(f"""
    <div style="margin: 2px 0 18px;">
        <div class="page-title">{esc(page_title)}</div>
        <div class="page-subtitle">{esc(page_subtitle)}</div>
    </div>
    """)

with header_mid:
    render_html(f"""
    <div class="meta-row" style="margin-bottom:16px;">
        <span class="pill">{esc(cohort_label)}</span>
        <span class="meta-date">{esc(now_ist().strftime("%A, %d %B %Y"))}</span>
    </div>
    """)

with header_right:
    with st.popover(current_username[:1].upper(), use_container_width=False):
        render_html(f"""
        <div style="min-width:160px;">
            <div class="pop-name">{esc(current_username)}</div>
            <div class="pop-role">{esc(current_role)}</div>
        </div>
        """)

        if st.button("Log out", key="header_logout", use_container_width=True):
            clear_auth_session(token=st.session_state.get("auth_token"))
            st.session_state["logged_in"] = False
            st.session_state["admin_username"] = None
            st.session_state["admin_role"] = None
            st.session_state["auth_token"] = None

            if "auth" in st.query_params:
                del st.query_params["auth"]

            st.rerun()


# =====================================================
# 14. RISK ANALYTICS
# =====================================================


if active_view == "Risk Analytics":
    try:
        batch_breakdown = []
        if is_overall:
            students = []
            loaded_at = now_ist().strftime("%d %b %Y, %H:%M IST")

            for cohort_id in batch_ids:
                cohort_students, loaded_at = load_cohort(cohort_id, str(DB_PATH))
                students.extend(cohort_students)
                cohort_df = pd.DataFrame(
                    cohort_students,
                    columns=["risk_band", "trend_warning"]
                )
                batch_breakdown.append({
                    "Batch": cohort_id,
                    "Status": "Active" if cohort_students else "No data yet",
                    "Students": len(cohort_students),
                    "High risk": int((cohort_df["risk_band"] == "High").sum()),
                    "Medium risk": int((cohort_df["risk_band"] == "Medium").sum()),
                    "Low risk": int((cohort_df["risk_band"] == "Low").sum()),
                    "Declining trend": int(cohort_df["trend_warning"].sum()),
                })
        else:
            students, loaded_at = load_cohort(batch_id, str(DB_PATH))

        if not students:
            if is_overall:
                st.warning("No student data found in any batch.")
            else:
                st.warning(f"No student data found for batch {batch_id}.")
        else:
            df = pd.DataFrame(students)

            required_columns = [
                "batch_id",
                "student_code",
                "risk_score",
                "risk_band",
                "trend_warning"
            ]

            missing_columns = [c for c in required_columns if c not in df.columns]

            if missing_columns:
                st.error(
                    "Risk data is missing required columns: "
                    + ", ".join(missing_columns)
                )
            else:
                df = df[required_columns].copy()
                df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce")
                df["trend_warning"] = df["trend_warning"].fillna(False).astype(bool)

                total = len(df)
                high_count = int((df["risk_band"] == "High").sum())
                med_count = int((df["risk_band"] == "Medium").sum())
                low_count = int((df["risk_band"] == "Low").sum())
                other_count = total - high_count - med_count - low_count
                declining_count = int(df["trend_warning"].sum())

                percentage_scope = "of all students" if is_overall else "of cohort"
                watchlist_scope = "across all batches" if is_overall else "in this cohort"

                def pct(count):
                    return f"{count / total:.0%} {percentage_scope}" if total else "No students"

                segments = ""
                for label, count, css in (
                    ("High", high_count, "seg-high"),
                    ("Medium", med_count, "seg-med"),
                    ("Low", low_count, "seg-low"),
                    ("Other", other_count, "seg-other"),
                ):
                    if count:
                        segments += (
                            f'<div class="{css}" style="flex:{count};" '
                            f'title="{label}: {count}"></div>'
                        )

                render_html(f"""
                <div class="summary-panel">
                    <div class="stat-strip">
                        <div class="stat">
                            <div class="stat-label">
                                {"Students across batches" if is_overall else "Students in cohort"}
                            </div>
                            <div class="stat-value">{total}</div>
                            <div class="stat-note">Loaded {esc(loaded_at)}</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">High risk</div>
                            <div class="stat-value high">{high_count}</div>
                            <div class="stat-note">{pct(high_count)}, act now</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">Medium risk</div>
                            <div class="stat-value med">{med_count}</div>
                            <div class="stat-note">{pct(med_count)}, keep watching</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">Low risk</div>
                            <div class="stat-value low">{low_count}</div>
                            <div class="stat-note">{pct(low_count)}, stable</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">Declining trend</div>
                            <div class="stat-value">{declining_count}</div>
                            <div class="stat-note">{pct(declining_count)}</div>
                        </div>
                    </div>
                    <div class="comp-bar">{segments}</div>
                    <div class="comp-legend">
                        <span><i class="dot seg-high"></i>High {high_count}</span>
                        <span><i class="dot seg-med"></i>Medium {med_count}</span>
                        <span><i class="dot seg-low"></i>Low {low_count}</span>
                    </div>
                </div>
                """)

                if is_overall:
                    st.subheader("Batch-by-batch breakdown")
                    st.dataframe(
                        pd.DataFrame(batch_breakdown),
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Batch": st.column_config.TextColumn("Batch"),
                            "Status": st.column_config.TextColumn("Status"),
                            "Students": st.column_config.NumberColumn("Students"),
                            "High risk": st.column_config.NumberColumn("High risk"),
                            "Medium risk": st.column_config.NumberColumn("Medium risk"),
                            "Low risk": st.column_config.NumberColumn("Low risk"),
                            "Declining trend": st.column_config.NumberColumn("Declining trend"),
                        }
                    )

                table_col, watch_col = st.columns([2.3, 1], gap="large")

                # ----- Student table with filters -----
                with table_col:
                    with st.container(border=True):
                        table_title = (
                            "Students across all batches"
                            if is_overall
                            else f"Students in {batch_id}"
                        )
                        st.subheader(table_title)
                        st.markdown(
                            "<div class='section-note'>Filter the students, then click a column header to sort.</div>",
                            unsafe_allow_html=True
                        )

                        f1, f2, f3 = st.columns([1.3, 1.5, 1], vertical_alignment="bottom")

                        with f1:
                            search_text = st.text_input(
                                "Search",
                                placeholder="Student code",
                                key=f"risk_search_{batch_id}"
                            )

                        with f2:
                            present_bands = [b for b in BAND_ORDER if b in set(df["risk_band"])]
                            chosen_bands = st.multiselect(
                                "Risk band",
                                present_bands,
                                default=present_bands,
                                key=f"risk_bands_{batch_id}_{'_'.join(present_bands)}"
                            )

                        with f3:
                            declining_only = st.toggle(
                                "Declining trend only",
                                key=f"risk_declining_{batch_id}"
                            )

                        filtered = df[df["risk_band"].isin(chosen_bands)]

                        if search_text.strip():
                            filtered = filtered[
                                filtered["student_code"].astype(str).str.contains(
                                    search_text.strip(), case=False, na=False, regex=False
                                )
                            ]

                        if declining_only:
                            filtered = filtered[filtered["trend_warning"]]

                        filtered = filtered.sort_values(
                            "risk_score", ascending=False, na_position="last"
                        )

                        if filtered.empty:
                            st.info("No students match these filters. Clear a filter to see more.")
                        else:
                            display_columns = ["student_code", "risk_score", "risk_band"]
                            if is_overall:
                                display_columns.insert(0, "batch_id")
                            display_df = filtered[display_columns].copy()
                            display_df["trend_status"] = filtered["trend_warning"].map(
                                lambda v: "↓ Declining" if v else "→ Stable"
                            )
                            download_df = filtered.copy()
                            download_df["trend_warning"] = download_df[
                                "trend_warning"
                            ].map(lambda v: "Declining" if v else "Stable")
                            if not is_overall:
                                download_df = download_df.drop(columns=["batch_id"])

                            score_max = df["risk_score"].max()
                            scale = 100.0 if pd.notna(score_max) and score_max > 1 else 1.0

                            st.dataframe(
                                display_df.style
                                .map(highlight_risk, subset=["risk_band"])
                                .map(highlight_trend, subset=["trend_status"]),
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "batch_id": st.column_config.TextColumn("Batch"),
                                    "student_code": st.column_config.TextColumn("Student code"),
                                    "risk_score": st.column_config.ProgressColumn(
                                        "Risk score",
                                        min_value=0.0,
                                        max_value=scale,
                                        format="%.1f"
                                    ),
                                    "risk_band": st.column_config.TextColumn("Risk band"),
                                    "trend_status": st.column_config.TextColumn("Trend"),
                                }
                            )

                            foot_left, foot_right = st.columns([3, 1], vertical_alignment="center")

                            with foot_left:
                                st.caption(f"Showing {len(filtered)} of {total} students")

                            with foot_right:
                                st.download_button(
                                    "Download CSV",
                                    data=download_df.to_csv(index=False).encode("utf-8"),
                                    file_name=(
                                        "risk_all_batches.csv"
                                        if is_overall
                                        else f"risk_{batch_id}.csv"
                                    ),
                                    mime="text/csv",
                                    use_container_width=True
                                )

                # ----- Watchlist -----
                with watch_col:
                    with st.container(border=True):
                        top_students = df.sort_values(
                            ["trend_warning", "risk_score"],
                            ascending=[False, False],
                            na_position="last"
                        ).head(5)

                        rows = ""
                        for _, row in top_students.iterrows():
                            score_text = "" if pd.isna(row["risk_score"]) else f"{row['risk_score']:.1f}"
                            trend_label = "Declining" if row["trend_warning"] else "Stable"
                            trend_text = f"{trend_label} trend"
                            trend_class = (
                                "trend-declining" if row["trend_warning"] else "trend-stable"
                            )
                            trend_icon = trend_image(row["trend_warning"])
                            rows += f"""
                            <div class="watch-row">
                                <div>
                                    <div class="watch-code">{esc(row['student_code'])}</div>
                                    <div class="watch-meta">{band_chip(row['risk_band'])}<img class="trend-icon {trend_class}" src="{trend_icon}" alt="{trend_text}" title="{trend_text}"><span class="trend-status {trend_class}">{trend_label}</span></div>
                                </div>
                                <div class="watch-score">{score_text}</div>
                            </div>
                            """

                        render_html(f"""
                        <div class="watch-head">Needs attention first</div>
                        <div class="watch-sub">Declining trends first, then highest risk scores {watchlist_scope}.</div>
                        {rows}
                        """)

    except Exception as error:
        st.error("Error loading batch risk data.")
        st.exception(error)


# =====================================================
# 15. IDENTITY LOOKUP
# =====================================================


if active_view == "Identity Lookup":
    try:
        lookup_batch_ids = batch_ids if is_overall else [batch_id]
        students_lookup = []
        for cohort_id in lookup_batch_ids:
            cohort_students, _ = load_cohort(cohort_id, str(DB_PATH))
            students_lookup.extend(cohort_students)
        student_codes = [
            s.get("student_code") for s in students_lookup if s.get("student_code")
        ]
    except Exception:
        student_codes = []

    if not student_codes:
        if is_overall:
            st.info("No students available for lookup across any batch.")
        else:
            st.info("No students available for lookup in this batch.")
    else:
        form_col, result_col = st.columns([1, 1.25], gap="large")

        with form_col:
            with st.container(border=True):
                st.subheader("Request identity")
                st.markdown(
                    "<div class='section-note'>Choose a student code and the reason for this lookup. "
                    "Your username, the reason and the time are saved to the audit log.</div>",
                    unsafe_allow_html=True
                )

                selected_student = st.selectbox(
                    "Student code",
                    student_codes
                )

                reason_code = st.selectbox(
                    "Reason for access",
                    list(REASON_LABELS.keys()),
                    format_func=reason_label
                )

                if st.button(
                    "Look up identity",
                    type="primary",
                    use_container_width=True
                ):
                    conn = get_db_connection()

                    try:
                        student_record = conn.execute(
                            """
                            SELECT
                                student_code,
                                full_name,
                                email,
                                batch_id,
                                enrolled_on
                            FROM students_identity
                            WHERE student_code = ?
                            """,
                            (selected_student,)
                        ).fetchone()

                        if student_record is None:
                            st.session_state.pop("identity_result", None)
                            st.error("No identity record exists for this student code.")
                        else:
                            current_timestamp = now_ist().strftime("%Y-%m-%d %H:%M:%S IST")

                            conn.execute(
                                """
                                INSERT INTO identity_audit_log
                                    (
                                        admin_username,
                                        student_code,
                                        accessed_at,
                                        reason_code
                                    )
                                VALUES (?, ?, ?, ?)
                                """,
                                (
                                    current_username,
                                    selected_student,
                                    current_timestamp,
                                    reason_code
                                )
                            )

                            conn.commit()

                            st.session_state["identity_result"] = {
                                "student_code": student_record["student_code"],
                                "full_name": student_record["full_name"],
                                "email": student_record["email"],
                                "batch_id": student_record["batch_id"],
                                "enrolled_on": student_record["enrolled_on"],
                                "reason": reason_label(reason_code),
                                "accessed_at": current_timestamp,
                            }

                    except sqlite3.Error:
                        conn.rollback()
                        st.error("The lookup failed and nothing was recorded. Please try again.")

                    finally:
                        conn.close()

        with result_col:
            with st.container(border=True):
                result = st.session_state.get("identity_result")

                if result and result["student_code"] in student_codes:
                    render_html(f"""
                    <div class="id-card-top">
                        <div class="id-avatar">{esc(initials(result['full_name']))}</div>
                        <div>
                            <div class="id-name">{esc(result['full_name'])}</div>
                            <div class="id-code">{esc(result['student_code'])}</div>
                        </div>
                    </div>
                    <div class="id-row"><span>Batch</span><span>{esc(result['batch_id'])}</span></div>
                    <div class="id-row"><span>Email</span><span class="id-email">{esc(result['email'])}</span></div>
                    <div class="id-row"><span>Enrolled on</span><span>{esc(result['enrolled_on'])}</span></div>
                    <div class="id-row"><span>Reason for access</span><span>{esc(result['reason'])}</span></div>
                    <div class="id-row"><span>Logged at</span><span>{esc(result['accessed_at'])}</span></div>
                    """)
                else:
                    render_html("""
                    <div class="empty-state">
                        <strong>No identity revealed yet</strong>
                        Pick a student code and a reason, then select Look up identity.
                        The details appear here.
                    </div>
                    """)

        # ----- Recent lookups by this admin -----
        conn = get_db_connection()

        try:
            recent_df = pd.read_sql_query(
                """
                SELECT
                    accessed_at,
                    student_code,
                    reason_code
                FROM identity_audit_log
                WHERE admin_username = ?
                ORDER BY id DESC
                LIMIT 5
                """,
                conn,
                params=(current_username,)
            )
        except sqlite3.Error:
            recent_df = pd.DataFrame()
        finally:
            conn.close()

        if not recent_df.empty:
            recent_df["reason_code"] = recent_df["reason_code"].map(reason_label)

            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

            with st.container(border=True):
                st.subheader("Your recent lookups")
                st.dataframe(
                    recent_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "accessed_at": st.column_config.TextColumn("Accessed at"),
                        "student_code": st.column_config.TextColumn("Student code"),
                        "reason_code": st.column_config.TextColumn("Reason"),
                    }
                )


# =====================================================
# 16. COMPLIANCE AUDIT
# =====================================================


if active_view == "Compliance Audit":
    conn = get_db_connection()

    try:
        audit_df = pd.read_sql_query(
            """
            SELECT
                id,
                admin_username,
                student_code,
                accessed_at,
                reason_code
            FROM identity_audit_log
            ORDER BY id DESC
            """,
            conn
        )

        if audit_df.empty:
            st.info(
                "No identity lookups have been logged yet. Entries appear here as soon as an admin looks up a student."
            )
        else:
            audit_df["admin_username"] = audit_df["admin_username"].fillna("Unknown")

            render_html(f"""
            <div class="summary-panel">
                <div class="stat-strip">
                    <div class="stat">
                        <div class="stat-label">Total lookups</div>
                        <div class="stat-value">{len(audit_df)}</div>
                        <div class="stat-note">All time</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Admins</div>
                        <div class="stat-value">{audit_df['admin_username'].nunique()}</div>
                        <div class="stat-note">Who have accessed identities</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Students accessed</div>
                        <div class="stat-value">{audit_df['student_code'].nunique()}</div>
                        <div class="stat-note">Distinct student codes</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Latest lookup</div>
                        <div class="stat-value" style="font-size:20px; margin-top:12px;">{esc(audit_df.iloc[0]['accessed_at'])}</div>
                        <div class="stat-note">by {esc(audit_df.iloc[0]['admin_username'])}</div>
                    </div>
                </div>
            </div>
            """)

            with st.container(border=True):
                st.subheader("Access log")

                a1, a2, a3 = st.columns(3)

                with a1:
                    admin_filter = st.selectbox(
                        "Admin",
                        ["All admins"] + sorted(audit_df["admin_username"].unique().tolist()),
                        key="audit_admin"
                    )

                with a2:
                    reason_filter = st.selectbox(
                        "Reason",
                        ["All reasons"] + sorted(audit_df["reason_code"].unique().tolist()),
                        format_func=lambda v: v if v == "All reasons" else reason_label(v),
                        key="audit_reason"
                    )

                with a3:
                    code_filter = st.text_input(
                        "Student code",
                        placeholder="Search",
                        key="audit_code"
                    )

                audit_view = audit_df.copy()

                if admin_filter != "All admins":
                    audit_view = audit_view[audit_view["admin_username"] == admin_filter]

                if reason_filter != "All reasons":
                    audit_view = audit_view[audit_view["reason_code"] == reason_filter]

                if code_filter.strip():
                    audit_view = audit_view[
                        audit_view["student_code"].astype(str).str.contains(
                            code_filter.strip(), case=False, na=False, regex=False
                        )
                    ]

                if audit_view.empty:
                    st.info("No log entries match these filters. Clear a filter to see more.")
                else:
                    audit_view["reason_code"] = audit_view["reason_code"].map(reason_label)

                    st.dataframe(
                        audit_view,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "id": st.column_config.NumberColumn("Entry", width="small"),
                            "admin_username": st.column_config.TextColumn("Admin"),
                            "student_code": st.column_config.TextColumn("Student code"),
                            "accessed_at": st.column_config.TextColumn("Accessed at"),
                            "reason_code": st.column_config.TextColumn("Reason"),
                        }
                    )

                    log_left, log_right = st.columns([3, 1], vertical_alignment="center")

                    with log_left:
                        st.caption(f"Showing {len(audit_view)} of {len(audit_df)} entries")

                    with log_right:
                        st.download_button(
                            "Download CSV",
                            data=audit_view.to_csv(index=False).encode("utf-8"),
                            file_name="identity_audit_log.csv",
                            mime="text/csv",
                            use_container_width=True
                        )

    except sqlite3.Error:
        st.error("Unable to load the audit log. Check the database connection and try again.")

    finally:
        conn.close()


# =====================================================
# 17. USER APPROVALS
# =====================================================


if active_view == "User Approvals":
    st.subheader("Administrator account management")
    st.caption(
        "Moderators can approve, reject, block, and unblock administrator accounts."
    )

    conn = get_db_connection()
    try:
        managed_admin_rows = conn.execute(
            """
            SELECT username, full_name, email, role, approval_status, created_at
            FROM admin_users
            WHERE role = 'Admin'
            ORDER BY
                CASE approval_status
                    WHEN 'Pending' THEN 1
                    WHEN 'Approved' THEN 2
                    WHEN 'Blocked' THEN 3
                    ELSE 4
                END,
                created_at,
                username
            """
        ).fetchall()
    except sqlite3.Error:
        managed_admin_rows = None
        st.error("Unable to load administrator accounts.")
    finally:
        conn.close()

    if managed_admin_rows is None:
        st.stop()

    if managed_admin_rows:
        managed_df = pd.DataFrame(
            [
                {
                    "Username": row["username"],
                    "Full name": row["full_name"] or "",
                    "Email": row["email"] or "",
                    "Status": row["approval_status"],
                    "Created": row["created_at"],
                }
                for row in managed_admin_rows
            ]
        )
        st.dataframe(managed_df, use_container_width=True, hide_index=True)

        manageable_statuses = {"Approved", "Blocked"}
        manageable_rows = [
            row for row in managed_admin_rows
            if row["approval_status"] in manageable_statuses
        ]

        if manageable_rows:
            manageable_by_username = {
                row["username"]: row
                for row in manageable_rows
            }
            managed_username = st.selectbox(
                "Administrator account",
                list(manageable_by_username),
                format_func=lambda username: (
                    f"{manageable_by_username[username]['full_name'] or username} "
                    f"({username}) - {manageable_by_username[username]['approval_status']}"
                ),
                key="managed_admin_account"
            )
            managed_status = manageable_by_username[managed_username]["approval_status"]

            if managed_status == "Approved":
                if st.button(
                    "Block administrator",
                    use_container_width=True,
                    key="block_administrator"
                ):
                    conn = get_db_connection()
                    try:
                        cursor = conn.execute(
                            """
                            UPDATE admin_users
                            SET approval_status = 'Blocked'
                            WHERE username = ? AND role = 'Admin'
                            """,
                            (managed_username,)
                        )
                        if cursor.rowcount != 1:
                            st.warning("This administrator account was not changed.")
                        else:
                            conn.commit()
                            st.toast(f"{managed_username} has been blocked.")
                            st.rerun()
                    except sqlite3.Error:
                        conn.rollback()
                        st.error("Unable to block this administrator. Please try again.")
                    finally:
                        conn.close()
            else:
                if st.button(
                    "Unblock administrator",
                    type="primary",
                    use_container_width=True,
                    key="unblock_administrator"
                ):
                    conn = get_db_connection()
                    try:
                        cursor = conn.execute(
                            """
                            UPDATE admin_users
                            SET approval_status = 'Approved'
                            WHERE username = ? AND role = 'Admin'
                            """,
                            (managed_username,)
                        )
                        if cursor.rowcount != 1:
                            st.warning("This administrator account was not changed.")
                        else:
                            conn.commit()
                            st.toast(f"{managed_username} has been unblocked.")
                            st.rerun()
                    except sqlite3.Error:
                        conn.rollback()
                        st.error("Unable to unblock this administrator. Please try again.")
                    finally:
                        conn.close()
        else:
            st.info("There are no approved or blocked administrator accounts to manage.")

    else:
        st.info("There are no administrator accounts.")

    st.divider()
    st.subheader("Pending account requests")
    st.caption(
        "New accounts start as Admin. Only the Moderator can approve or reject access requests."
    )

    conn = None
    try:
        conn = get_db_connection()
        pending_rows = conn.execute(
            """
            SELECT username, full_name, email, created_at
            FROM admin_users
            WHERE approval_status = 'Pending'
            ORDER BY created_at, username
            """
        ).fetchall()
    except sqlite3.Error:
        pending_rows = None
        st.error("Unable to load pending account requests.")
    finally:
        if conn is not None:
            conn.close()

    if pending_rows is None:
        st.stop()
    elif not pending_rows:
        st.info("There are no pending account requests.")
    else:
        pending_by_username = {
            row["username"]: row
            for row in pending_rows
        }
        pending_df = pd.DataFrame(
            [
                {
                    "Username": row["username"],
                    "Full name": row["full_name"] or "",
                    "Email": row["email"] or "",
                    "Requested at": row["created_at"],
                }
                for row in pending_rows
            ]
        )
        st.dataframe(
            pending_df,
            use_container_width=True,
            hide_index=True
        )

        selected_username = st.selectbox(
            "Account request",
            list(pending_by_username),
            format_func=lambda username: (
                f"{pending_by_username[username]['full_name'] or username} ({username})"
            ),
            key="approval_selected_user"
        )
        approve_col, reject_col = st.columns(2)
        with approve_col:
            if st.button(
                "Approve account",
                type="primary",
                use_container_width=True,
                key="approve_account_request"
            ):
                conn = get_db_connection()
                try:
                    cursor = conn.execute(
                        """
                        UPDATE admin_users
                        SET approval_status = 'Approved'
                        WHERE username = ? AND approval_status = 'Pending'
                        """,
                        (selected_username,)
                    )
                    if cursor.rowcount != 1:
                        conn.rollback()
                        st.warning("This request is no longer pending.")
                    else:
                        conn.commit()
                        st.toast(f"{selected_username} approved as Admin.")
                        st.rerun()
                except sqlite3.Error:
                    conn.rollback()
                    st.error("Unable to approve this account. Please try again.")
                finally:
                    conn.close()

        with reject_col:
            if st.button(
                "Reject account",
                use_container_width=True,
                key="reject_account_request"
            ):
                conn = get_db_connection()
                try:
                    cursor = conn.execute(
                        """
                        UPDATE admin_users
                        SET approval_status = 'Rejected'
                        WHERE username = ? AND approval_status = 'Pending'
                        """,
                        (selected_username,)
                    )
                    if cursor.rowcount != 1:
                        conn.rollback()
                        st.warning("This request is no longer pending.")
                    else:
                        conn.commit()
                        st.toast(f"{selected_username}'s request was rejected.")
                        st.rerun()
                except sqlite3.Error:
                    conn.rollback()
                    st.error("Unable to reject this account. Please try again.")
                finally:
                    conn.close()


# =====================================================
# 18. FOOTER
# =====================================================


st.markdown("---")

render_html("""
<div class="footer-note">
    Student Intelligence Platform, enterprise compliance console.
</div>
""")