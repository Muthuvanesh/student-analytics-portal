import streamlit as st
import sqlite3
import pandas as pd
import base64
import hashlib
import hmac
import os


from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


from app.risk_engine import compute_batch_risk_scores


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================


st.set_page_config(
    page_title="Student Intelligence Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


BASE_DIR = Path(__file__).resolve().parent
TEST_MODE = os.getenv("APP_ENV", "").strip().lower() == "test"
DB_PATH = Path(os.getenv("ACADEMY_DB_PATH", str(BASE_DIR / "academy.db")))


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
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e3a8a 100%
    );
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


[data-testid="column"]:nth-of-type(2) {
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


[data-testid="column"]:nth-of-type(2)::before {
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


div[data-testid="stTextInput"] input {
    border-radius: 10px;
    min-height: 48px;
    border: 1px solid #334155;
    background-color: rgba(15, 23, 42, 0.8);
    color: #ffffff;
    transition: all 0.2s ease;
}


div[data-testid="stTextInput"] input:focus {
    border-color: #38bdf8;
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
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                full_name TEXT,
                email TEXT,
                role TEXT DEFAULT 'Admin',
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


        conn.commit()

    finally:
        conn.close()


# =====================================================
# 5. AUTHENTICATION HELPERS
# =====================================================


def verify_db_user(username, password):
    conn = get_db_connection()

    try:
        user = conn.execute(
            """
            SELECT
                username,
                password_hash,
                salt,
                role
            FROM admin_users
            WHERE username = ?
            """,
            (username.strip(),)
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
                "role": user["role"]
            }


        return None

    finally:
        conn.close()


def register_new_user(
    username,
    password,
    registration_code,
    full_name,
    email,
    role="Admin"
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


    if not TEST_MODE:
        try:
            expected_code = st.secrets["ADMIN_REGISTRATION_CODE"]
        except Exception:
            return False, "Administrator registration is not configured."


        if not hmac.compare_digest(
            registration_code.encode("utf-8"),
            str(expected_code).encode("utf-8")
        ):
            return False, "Invalid administrator invitation code."


    conn = get_db_connection()

    try:
        existing = conn.execute(
            """
            SELECT id
            FROM admin_users
            WHERE username = ?
            """,
            (clean_user,)
        ).fetchone()


        if existing:
            return False, f"User '{clean_user}' already exists."


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
                    role
                )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                clean_user,
                password_hash,
                salt_hex,
                clean_full_name,
                clean_email,
                role
            )
        )


        conn.commit()
        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, f"Username '{clean_user}' is already taken."

    except Exception:
        return False, "Unable to create the account. Please try again."

    finally:
        conn.close()


def get_user_role(username):
    conn = get_db_connection()

    try:
        row = conn.execute(
            """
            SELECT role
            FROM admin_users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()


        return row["role"] if row else None

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


# =====================================================
# 7. INITIALIZE DATABASE
# =====================================================


try:
    initialize_database()
except sqlite3.Error:
    st.error("Unable to initialize the database.")
    st.stop()


# =====================================================
# 8. LOGIN & REGISTRATION INTERFACE
# =====================================================


if not st.session_state["logged_in"]:


    left, right = st.columns(
        [1.1, 1],
        gap="large"
    )


    with left:
        raw_html = """
        <div class="brand-panel">
            <div class="brand-subtitle">Enterprise Portal</div>
            <div class="brand-logo">
                🎓 Student<span>Portal</span>
            </div>
            <h2 style="color:white; font-size:24px; font-weight:700; margin-bottom:15px; letter-spacing:-0.5px;">
                Monitor. Predict. Support.
            </h2>
            <p class="brand-description">
                An advanced administrative intelligence console built to monitor academic trajectories,
                identify risk vectors, and facilitate early data-driven student interventions.
            </p>
            <div class="brand-feature-container">
                <div class="brand-feature">
                    📊 &nbsp; Real-time Performance & Attendance Tracking
                </div>
                <div class="brand-feature">
                    🛡️ &nbsp; Predictive Student At-Risk Analysis
                </div>
                <div class="brand-feature">
                    🤝 &nbsp; Streamlined Faculty Intervention Workflows
                </div>
                <div class="brand-feature">
                    🔐 &nbsp; Fully Audited Secure Identity Access
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


        raw_header_html = """
        <div class="login-header-container">
            <div style="font-size:36px; margin-bottom:8px;">🔐</div>
            <div class="login-heading">Student Portal Authentication</div>
            <div class="login-description">Sign in to your account</div>
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
                "✅ Account created successfully. Please sign in with your new credentials."
            )
            st.session_state["registration_success"] = False


        if st.session_state["auth_page"] == "Sign In":
            with st.form("professional_login"):
                username = st.text_input(
                    "Username",
                    placeholder="Enter your username",
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
                    "Sign In to Console  →",
                    use_container_width=True
                )


                if submit:
                    if not username.strip() or not password:
                        st.error("Please enter your username and password.")
                    else:
                        user = verify_db_user(username, password)


                        if user:
                            st.session_state["logged_in"] = True
                            st.session_state["admin_username"] = user["username"]
                            st.session_state["admin_role"] = user["role"]
                            st.rerun()
                        else:
                            st.error("Invalid username or password.")


            st.markdown(
                "<div style='text-align:center; color:#94a3b8; font-size:13px; margin-top:18px;'>"
                "Don't have an account?"
                "</div>",
                unsafe_allow_html=True
            )
            if st.button("Create new account", use_container_width=True):
                st.session_state["auth_page"] = "Create Account"
                st.rerun()

        else:
            st.markdown("""
            <div style="
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(56, 189, 248, 0.18);
                border-radius: 18px;
                padding: 28px 26px;
                margin-bottom: 20px;
                text-align: center;
                position: relative;
                z-index: 2;
            ">
                <div style="font-size: 34px; margin-bottom: 8px;">✨</div>
                <div style="
                    color: #ffffff;
                    font-size: 22px;
                    font-weight: 800;
                    letter-spacing: -0.5px;
                    margin-bottom: 6px;
                ">
                    Create your admin account
                </div>
                <div style="
                    color: #94a3b8;
                    font-size: 13.5px;
                    line-height: 1.5;
                ">
                    Complete your details to create an account.
                </div>
            </div>
            """, unsafe_allow_html=True)


            with st.form("facebook_style_signup", clear_on_submit=True):
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


                registration_code = ""
                if not TEST_MODE:
                    registration_code = st.text_input(
                        "Administrator invitation code",
                        type="password",
                        placeholder="Enter the invitation code",
                        key="signup_code"
                    )
                else:
                    st.caption("Test mode: invitation code is disabled.")


                st.markdown(
                    """
                    <div style="
                        color:#94a3b8;
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
                    "Create Account",
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
                        st.error("Please create a password.")


                    elif len(new_password) < 8:
                        st.error("Password must be at least 8 characters long.")


                    elif new_password != confirm_password:
                        st.error("Passwords do not match.")


                    else:
                        success, message = register_new_user(
                            new_username,
                            new_password,
                            registration_code,
                            full_name,
                            email
                        )


                        if success:
                            st.session_state["registration_success"] = True
                            st.session_state["auth_page"] = "Sign In"
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")

            if st.button("← Back to sign in", use_container_width=True):
                st.session_state["auth_page"] = "Sign In"
                st.rerun()


    st.stop()


# =====================================================
# 9. AUTHORIZATION CHECK
# =====================================================


current_username = st.session_state["admin_username"]
current_role = get_user_role(current_username)


if not current_username or current_role not in ["Admin", "Super Admin"]:
    st.session_state["logged_in"] = False
    st.session_state["admin_username"] = None
    st.session_state["admin_role"] = None
    st.error("Your account is not authorized to access this console.")
    st.stop()


background_image_data = base64.b64encode(
    (BASE_DIR / "assets" / "library-background.jpg").read_bytes()
).decode("ascii")


dashboard_background_css = """
<style>
.stApp {
    background: transparent !important;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: -4px;
    z-index: 0;
    background-image:
        linear-gradient(rgba(250, 246, 240, 0.15), rgba(250, 246, 240, 0.15)),
        url("data:image/jpeg;base64,IMAGE_DATA");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    filter: sepia(0.2) saturate(0.7) brightness(1.08) blur(0.6px);
    pointer-events: none;
}

section[data-testid="stMain"] {
    position: relative;
    z-index: 1;
}

.stApp h1,
.stApp h2,
.stApp h3 {
    color: #14354b !important;
}

.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] [style*="text-align:center"],
.stApp [data-testid="stWidgetLabel"] *,
.stApp button[data-baseweb="tab"] *,
.stApp [style*="padding-top: 8px"] {
    color: #172b3a !important;
    font-weight: 800 !important;
    text-shadow: 0 0 5px rgba(250, 246, 240, 1), 0 0 12px rgba(250, 246, 240, 0.95);
}

.stApp [data-testid="stMarkdownContainer"] p {
    display: inline-block;
    padding: 3px 7px;
    border-radius: 4px;
    background: rgba(250, 246, 240, 0.9);
}

.stApp [data-testid="stMarkdownContainer"] h3 {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 4px;
    background: rgba(250, 246, 240, 0.92);
}

.stApp [style*="text-align:center"] {
    background: rgba(250, 246, 240, 0.9) !important;
    border-radius: 4px;
}
</style>
"""
st.markdown(
    dashboard_background_css.replace("IMAGE_DATA", background_image_data),
    unsafe_allow_html=True
)


# =====================================================
# 10. EXECUTIVE COMMAND CENTER
# =====================================================


st.markdown("""
<div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 18px 24px; border-radius: 14px; color: white; display: flex; align-items: center; justify-content: space-between; margin-bottom: 25px; box-shadow: 0 4px 20px rgba(15, 23, 42, 0.15);">
    <div style="font-size: 20px; font-weight: 700; display: flex; align-items: center; gap: 10px;">
        🎓 <span style="letter-spacing: -0.5px;">Student Intelligence Portal</span>
    </div>
    <div style="font-size: 13px; color: #94a3b8; font-weight: 500; background: rgba(255, 255, 255, 0.08); padding: 6px 14px; border-radius: 20px;">
        Enterprise Intelligence Console v1.1
    </div>
</div>
""", unsafe_allow_html=True)


top_col1, top_col2 = st.columns([2, 1])


with top_col1:
    batch_id = st.selectbox(
        "Active Cohort Batch Selector",
        ["PY-2026-03", "PY-2026-04"]
    )


with top_col2:
    st.markdown(
        "<div style='height: 28px;'></div>",
        unsafe_allow_html=True
    )


    col_user, col_logout = st.columns([1.5, 1])


    with col_user:
        st.markdown(
            f"""
            <div style='padding-top: 8px; font-size: 14px; color: #334155; font-weight: 600;'>
                👤 {current_username} &nbsp;•&nbsp; {current_role}
            </div>
            """,
            unsafe_allow_html=True
        )


    with col_logout:
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["admin_username"] = None
            st.session_state["admin_role"] = None
            st.rerun()


st.markdown(
    "<div style='height: 10px;'></div>",
    unsafe_allow_html=True
)


tab_risk, tab_lookup, tab_audit = st.tabs([
    "📊 Risk Analytics Dashboard",
    "🔒 Secure Identity Lookup",
    "📋 Compliance Audit Logs"
])


# =====================================================
# TAB 1: RISK ANALYTICS DASHBOARD
# =====================================================


with tab_risk:
    st.markdown(
        "<div style='height: 10px;'></div>",
        unsafe_allow_html=True
    )


    try:
        results = compute_batch_risk_scores(
            batch_id,
            db_path=str(DB_PATH)
        )


        students = results.get("students", [])


        if not students:
            st.warning(
                f"No student data found for batch {batch_id}."
            )
        else:
            df = pd.DataFrame(students)


            required_columns = [
                "student_code",
                "risk_score",
                "risk_band",
                "trend_warning"
            ]


            missing_columns = [
                column
                for column in required_columns
                if column not in df.columns
            ]


            if missing_columns:
                st.error(
                    "Risk data is missing required columns: "
                    + ", ".join(missing_columns)
                )
            else:
                high_count = len(df[df["risk_band"] == "High"])
                med_count = len(df[df["risk_band"] == "Medium"])
                low_count = len(df[df["risk_band"] == "Low"])


                kpi1, kpi2, kpi3 = st.columns(3)


                kpi1.metric(
                    "🔴 High Risk Vector",
                    high_count,
                    delta="Immediate Action",
                    delta_color="inverse"
                )


                kpi2.metric(
                    "🟡 Medium Risk Vector",
                    med_count,
                    delta="Monitor Trend"
                )


                kpi3.metric(
                    "🟢 Low Risk / Stable",
                    low_count,
                    delta="Optimal"
                )


                st.markdown(
                    "<div style='height: 20px;'></div>",
                    unsafe_allow_html=True
                )


                with st.container():
                    st.subheader(
                        f"Cohort Risk Matrix — `{batch_id}`"
                    )


                    st.markdown(
                        "<p style='color: #64748b; font-size: 13.5px; margin-bottom: 15px;'>"
                        "Real-time analytical risk assessment across active trajectory vectors."
                        "</p>",
                        unsafe_allow_html=True
                    )


                    display_df = df[required_columns].copy()


                    display_df["risk_score"] = pd.to_numeric(
                        display_df["risk_score"],
                        errors="coerce"
                    ).map(
                        lambda value: (
                            ""
                            if pd.isna(value)
                            else f"{value:.1f}"
                        )
                    )


                    display_df["trend_warning"] = display_df[
                        "trend_warning"
                    ].map(
                        lambda value: (
                            "⚠️ Declining"
                            if value
                            else "Stable"
                        )
                    )


                    def highlight_risk(value):
                        if value == "High":
                            return (
                                "background-color:#fee2e2; "
                                "color:#991b1b; "
                                "font-weight:bold;"
                            )


                        if value == "Medium":
                            return (
                                "background-color:#fef3c7; "
                                "color:#92400e; "
                                "font-weight:bold;"
                            )


                        return (
                            "background-color:#dcfce7; "
                            "color:#166534; "
                            "font-weight:bold;"
                        )


                    st.dataframe(
                        display_df.style.map(
                            highlight_risk,
                            subset=["risk_band"]
                        ),
                        use_container_width=True,
                        hide_index=True
                    )

    except Exception as error:
        st.error("Error loading batch risk data.")
        st.exception(error)


# =====================================================
# TAB 2: SECURE IDENTITY LOOKUP
# =====================================================


with tab_lookup:
    st.markdown(
        "<div style='height: 10px;'></div>",
        unsafe_allow_html=True
    )


    with st.container():
        st.subheader("🔒 Secure Student Identity Lookup")
        st.markdown(
            "<p style='color: #64748b; font-size: 13.5px; margin-bottom: 20px;'>"
            "Select an obfuscated student code to review authorized identity details. "
            "Every lookup is recorded in the compliance audit log."
            "</p>",
            unsafe_allow_html=True
        )


        try:
            results_lookup = compute_batch_risk_scores(
                batch_id,
                db_path=str(DB_PATH)
            )


            students_lookup = results_lookup.get("students", [])
            df_lookup = pd.DataFrame(students_lookup)


            if not df_lookup.empty and "student_code" in df_lookup.columns:
                student_codes = df_lookup["student_code"].tolist()
            else:
                student_codes = []

        except Exception:
            student_codes = []


        if student_codes:
            lookup_col1, lookup_col2 = st.columns(2)


            with lookup_col1:
                selected_student = st.selectbox(
                    "Select Obfuscated Code",
                    student_codes
                )


            with lookup_col2:
                reason_code = st.selectbox(
                    "Authorized Intervention Reason",
                    [
                        "COUNSELING_INTERVENTION",
                        "ACADEMIC_ADVISING",
                        "PARENT_MEETING"
                    ]
                )


            st.markdown(
                "<div style='height: 10px;'></div>",
                unsafe_allow_html=True
            )


            if st.button(
                "🔍 Fetch & Audit Identity",
                use_container_width=True
            ):
                conn = get_db_connection()


                try:
                    student_record = conn.execute(
                        """
                        SELECT
                            student_code,
                            full_name,
                            batch_id,
                            enrolled_on
                        FROM students_identity
                        WHERE student_code = ?
                        """,
                        (selected_student,)
                    ).fetchone()


                    if student_record is None:
                        st.error("Student identity record not found.")
                    else:
                        current_timestamp = datetime.now(
                            ZoneInfo("Asia/Kolkata")
                        ).strftime("%Y-%m-%d %H:%M:%S IST")


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


                        st.info(
                            f"""
                            **Student Code:** {student_record['student_code']}  
                            **Full Name:** {student_record['full_name']}  
                            **Batch ID:** {student_record['batch_id']}  
                            **Enrolled On:** {student_record['enrolled_on']}
                            """
                        )

                except sqlite3.Error:
                    conn.rollback()
                    st.error("Identity lookup failed securely.")

                finally:
                    conn.close()

        else:
            st.info(
                "No students available for lookup in this batch."
            )


# =====================================================
# TAB 3: COMPLIANCE AUDIT LOGS
# =====================================================


with tab_audit:
    st.markdown(
        "<div style='height: 10px;'></div>",
        unsafe_allow_html=True
    )


    with st.container():
        st.subheader("📋 Administrative Compliance Audit Log")
        st.markdown(
            "<p style='color: #64748b; font-size: 13.5px; margin-bottom: 20px;'>"
            "Chronological tracking ledger recording administrative identity access requests."
            "</p>",
            unsafe_allow_html=True
        )


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
                    "No compliance audit entries recorded yet."
                )
            else:
                st.dataframe(
                    audit_df,
                    use_container_width=True,
                    hide_index=True
                )

        except sqlite3.Error:
            st.error("Unable to load compliance audit logs.")

        finally:
            conn.close()


# =====================================================
# 11. FOOTER
# =====================================================


st.markdown("---")


st.markdown("""
<div style="text-align:center; color:#94a3b8; font-size:12px; padding:15px;">
    🎓 Student Intelligence Platform &nbsp;•&nbsp; Enterprise Compliance Console
    <br>
    Monitor. Predict. Support.
</div>
""", unsafe_allow_html=True)