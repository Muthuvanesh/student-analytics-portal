import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import hmac

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
DB_PATH = BASE_DIR / "academy.db"


# =====================================================
# 2. PROFESSIONAL ENTERPRISE UI & REALISTIC FALLING STARS
# =====================================================

st.markdown("""
<style>
/* Global Resets & Typography */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: linear-gradient(135deg, #060913 0%, #0f172a 100%);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.block-container {
    max-width: 1440px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* LEFT BRAND PANEL - Modern Deep Gradient */
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

/* =====================================================
   RIGHT COLUMN: NIGHT SKY & FALLING SHOOTING STARS
   ===================================================== */
[data-testid="column"]:nth-of-type(2) {
    position: relative !important;
    overflow: hidden !important;
    background: radial-gradient(ellipse at bottom, #1b2735 0%, #090a0f 100%) !important;
    padding: 40px 40px !important;
    border-radius: 24px !important;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    border: 1px solid rgba(56, 189, 248, 0.25);
    min-height: 580px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

/* Static Ambient Twinkling Stars */
[data-testid="column"]:nth-of-type(2)::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background-image: 
        radial-gradient(1.5px 1.5px at 15% 20%, #ffffff, transparent),
        radial-gradient(2px 2px at 35% 15%, #7dd3fc, transparent),
        radial-gradient(1px 1px at 65% 25%, #ffffff, transparent),
        radial-gradient(2px 2px at 85% 30%, #bae6fd, transparent),
        radial-gradient(1.5px 1.5px at 25% 60%, #ffffff, transparent),
        radial-gradient(1px 1px at 75% 70%, #7dd3fc, transparent),
        radial-gradient(2px 2px at 50% 85%, #ffffff, transparent),
        radial-gradient(1.5px 1.5px at 90% 80%, #ffffff, transparent);
    opacity: 0.65;
    animation: twinkle 4s ease-in-out infinite alternate;
    z-index: 0;
}

@keyframes twinkle {
    0% { opacity: 0.35; }
    100% { opacity: 0.85; }
}

/* Starfield Overlay Layer */
.star-sky {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
    z-index: 1;
}

/* Realistic Shooting Star with Glowing Head & Tapered Tail */
.star {
    position: absolute;
    top: -10%;
    width: 120px;
    height: 2px;
    background: linear-gradient(90deg, rgba(255, 255, 255, 0.95), rgba(56, 189, 248, 0.5), transparent);
    border-radius: 999px;
    filter: drop-shadow(0 0 6px #38bdf8);
    transform: rotate(-45deg);
    opacity: 0;
    animation: shooting-star 4s ease-in infinite;
}

/* Bright Glowing Star Head */
.star::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 0;
    transform: translateY(-50%);
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: #ffffff;
    box-shadow: 0 0 10px 2px #ffffff, 0 0 18px 4px #38bdf8;
}

/* Staggered Positions, Timings & Speeds */
.star:nth-child(1) {
    left: 35%;
    animation-delay: 0.2s;
    animation-duration: 3.2s;
}

.star:nth-child(2) {
    left: 75%;
    animation-delay: 1.5s;
    animation-duration: 2.8s;
}

.star:nth-child(3) {
    left: 105%;
    animation-delay: 2.7s;
    animation-duration: 3.6s;
}

.star:nth-child(4) {
    left: 55%;
    animation-delay: 3.8s;
    animation-duration: 2.5s;
}

.star:nth-child(5) {
    left: 90%;
    animation-delay: 5.0s;
    animation-duration: 3.1s;
}

.star:nth-child(6) {
    left: 20%;
    animation-delay: 6.2s;
    animation-duration: 2.9s;
}

@keyframes shooting-star {
    0% {
        transform: translate(0, 0) rotate(-45deg);
        opacity: 0;
    }
    10% {
        opacity: 1;
    }
    70% {
        opacity: 1;
    }
    100% {
        transform: translate(-550px, 550px) rotate(-45deg);
        opacity: 0;
    }
}

/* Keep Form Elements Above the Starfield */
div.stForm {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
    position: relative;
    z-index: 2;
}

/* Typography & Headings */
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
    background-color: rgba(15, 23, 42, 0.85);
    color: #ffffff;
    transition: all 0.2s ease;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #38bdf8;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25);
}

div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    color: white;
    border: none;
    border-radius: 10px;
    height: 48px;
    font-size: 14.5px;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.45);
    transition: all 0.2s ease;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
    box-shadow: 0 6px 20px rgba(56, 189, 248, 0.5);
    color: white;
}

.security-note {
    background: rgba(6, 95, 70, 0.35);
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

.footer-text {
    color: #64748b;
    text-align: center;
    font-size: 12px;
    padding-top: 10px;
    position: relative;
    z-index: 2;
}

/* PREMIUM METRIC CARDS OVERRIDE (POST-LOGIN) */
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

/* DATAFRAME & TABLE POLISH */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
}

/* CONTAINER ACCENTS */
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
# 4. AUDIT TABLE INITIALIZATION
# =====================================================

def initialize_audit_table():
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

        conn.commit()

    finally:
        conn.close()


# =====================================================
# 5. PASSWORD VERIFICATION
# =====================================================

def verify_password(password):
    salt = bytes.fromhex(
        st.secrets["admin"]["salt"]
    )

    entered_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600000
    ).hex()

    return hmac.compare_digest(
        entered_hash,
        st.secrets["admin"]["password_hash"]
    )


# =====================================================
# 6. SESSION & URL PERSISTENCE SYNCHRONIZATION
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "admin_username" not in st.session_state:
    st.session_state["admin_username"] = None

query_params = st.query_params
url_user = query_params.get("session_user")

if url_user:
    st.session_state["logged_in"] = True
    st.session_state["admin_username"] = url_user


# =====================================================
# 7. LOGIN INTERFACE (WITH REALISTIC FALLING STARS)
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
        cleaned_html = "\n".join([line.strip() for line in raw_html.strip().splitlines()])
        st.markdown(cleaned_html, unsafe_allow_html=True)

    with right:
        # Realistic Falling Stars Layer
        st.markdown("""
        <div class="star-sky">
            <span class="star"></span>
            <span class="star"></span>
            <span class="star"></span>
            <span class="star"></span>
            <span class="star"></span>
            <span class="star"></span>
        </div>
        """, unsafe_allow_html=True)

        raw_header_html = """
        <div class="login-header-container">
            <div style="font-size:36px; margin-bottom:8px;">🔐</div>
            <div class="login-heading">Admin Sign In</div>
            <div class="login-description">Enter your credentials to access the console</div>
        </div>
        """
        st.markdown("\n".join([line.strip() for line in raw_header_html.strip().splitlines()]), unsafe_allow_html=True)

        with st.form("professional_login"):

            username = st.text_input(
                "Username",
                placeholder="Enter your username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)

            submit = st.form_submit_button(
                "Sign In to Console  →",
                use_container_width=True
            )

            if submit:

                if not username.strip() or not password:

                    st.error(
                        "Please enter your username and password."
                    )

                else:

                    try:

                        configured_username = (
                            st.secrets["admin"]["username"]
                        )

                        username_valid = hmac.compare_digest(
                            username.strip(),
                            configured_username
                        )

                        password_valid = verify_password(password)

                        if username_valid and password_valid:

                            st.session_state["logged_in"] = True
                            st.session_state["admin_username"] = username.strip()
                            st.query_params["session_user"] = username.strip()
                            st.rerun()

                        else:

                            st.error(
                                "Invalid username or password."
                            )

                    except Exception:

                        st.error(
                            "Authentication service unavailable. "
                            "Please contact your system administrator."
                        )

        raw_footer_html = """
        <div class="security-note">
            🔒 Protected by cryptographic hashing & audited compliance logs.
        </div>
        <div class="footer-text">
            v1.0 &nbsp;•&nbsp; Student Intelligence Platform
        </div>
        """
        st.markdown("\n".join([line.strip() for line in raw_footer_html.strip().splitlines()]), unsafe_allow_html=True)

    st.stop()


# =====================================================
# 8. INITIALIZE AUDIT DATABASE
# =====================================================

try:
    initialize_audit_table()
except sqlite3.Error:
    st.error("Unable to initialize the audit database.")
    st.stop()


# =====================================================
# 9. EXECUTIVE COMMAND CENTER INTERFACE (POST-LOGIN)
# =====================================================

st.markdown("""
<div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 18px 24px; border-radius: 14px; color: white; display: flex; align-items: center; justify-content: space-between; margin-bottom: 25px; box-shadow: 0 4px 20px rgba(15, 23, 42, 0.15);">
    <div style="font-size: 20px; font-weight: 700; display: flex; align-items: center; gap: 10px;">
        🎓 <span style="letter-spacing: -0.5px;">Student Intelligence Portal</span>
    </div>
    <div style="font-size: 13px; color: #94a3b8; font-weight: 500; background: rgba(255, 255, 255, 0.08); padding: 6px 14px; border-radius: 20px;">
        Enterprise Intelligence Console v1.0
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
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    col_user, col_logout = st.columns([1.5, 1])
    with col_user:
        st.markdown(f"<div style='padding-top: 8px; font-size: 14px; color: #334155; font-weight: 600;'>👤 {st.session_state['admin_username']}</div>", unsafe_allow_html=True)
    with col_logout:
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["admin_username"] = None
            st.query_params.clear()
            st.rerun()

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

tab_risk, tab_lookup, tab_audit = st.tabs([
    "📊 Risk Analytics Dashboard", 
    "🔒 Secure Identity Lookup", 
    "📋 Compliance Audit Logs"
])


# =====================================================
# TAB 1: RISK ANALYTICS DASHBOARD
# =====================================================
with tab_risk:
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    try:
        results = compute_batch_risk_scores(batch_id, db_path=str(DB_PATH))
        students = results.get("students", [])

        if not students:
            st.warning(f"No student data found for batch {batch_id}.")
        else:
            df = pd.DataFrame(students)
            
            high_count = len(df[df["risk_band"] == "High"])
            med_count = len(df[df["risk_band"] == "Medium"])
            low_count = len(df[df["risk_band"] == "Low"])
            
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("🔴 High Risk Vector", high_count, delta="Immediate Action", delta_color="inverse")
            kpi2.metric("🟡 Medium Risk Vector", med_count, delta="Monitor Trend")
            kpi3.metric("🟢 Low Risk / Stable", low_count, delta="Optimal")

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

            with st.container():
                st.subheader(f"Cohort Risk Matrix — `{batch_id}`")
                st.markdown("<p style='color: #64748b; font-size: 13.5px; margin-bottom: 15px;'>Real-time analytical risk assessment across active trajectory vectors.</p>", unsafe_allow_html=True)
                
                required_columns = ["student_code", "risk_score", "risk_band", "trend_warning"]
                display_df = df[required_columns].copy()
                
                display_df["risk_score"] = display_df["risk_score"].apply(lambda val: f"{float(val):.1f}")

                display_df["trend_warning"] = display_df["trend_warning"].apply(
                    lambda x: "⚠️ Declining" if x else "Stable"
                )

                def highlight_risk(value):
                    if value == "High":
                        return "background-color:#fee2e2; color:#991b1b; font-weight:bold;"
                    elif value == "Medium":
                        return "background-color:#fef3c7; color:#92400e; font-weight:bold;"
                    return "background-color:#dcfce7; color:#166534; font-weight:bold;"

                styler_method = getattr(display_df.style, "map", None) or getattr(display_df.style, "applymap")

                st.dataframe(
                    styler_method(highlight_risk, subset=["risk_band"]),
                    use_container_width=True,
                    hide_index=True
                )

    except Exception as error:
        st.error(f"Error loading batch risk data: {error}")


# =====================================================
# TAB 2: SECURE IDENTITY LOOKUP
# =====================================================
with tab_lookup:
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    with st.container():
        st.subheader("🔒 Secure Student Identity Decryption")
        st.markdown("<p style='color: #64748b; font-size: 13.5px; margin-bottom: 20px;'>Select an obfuscated student code to review underlying identity credentials under strict compliance protocols.</p>", unsafe_allow_html=True)

        try:
            results_lookup = compute_batch_risk_scores(batch_id, db_path=str(DB_PATH))
            students_lookup = results_lookup.get("students", [])
            df_lookup = pd.DataFrame(students_lookup)
            student_codes = df_lookup["student_code"].tolist() if not df_lookup.empty else []
        except Exception:
            student_codes = []

        if student_codes:
            lookup_col1, lookup_col2 = st.columns(2)
            
            with lookup_col1:
                selected_student = st.selectbox("Select Obfuscated Code", student_codes)
            
            with lookup_col2:
                reason_code = st.selectbox(
                    "Authorized Intervention Reason",
                    ["COUNSELING_INTERVENTION", "ACADEMIC_ADVISING", "PARENT_MEETING"]
                )

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            if st.button("🔍 Fetch & Audit Decrypted Identity", use_container_width=True):
                conn = get_db_connection()
                try:
                    student_record = conn.execute(
                        """
                        SELECT student_code, full_name, batch_id, enrolled_on
                        FROM students_identity
                        WHERE student_code = ?
                        """,
                        (selected_student,)
                    ).fetchone()

                    if student_record is None:
                        st.error("Student identity record not found.")
                    else:
                        current_timestamp = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S IST")
                        conn.execute(
                            """
                            INSERT INTO identity_audit_log (admin_username, student_code, accessed_at, reason_code)
                            VALUES (?, ?, ?, ?)
                            """,
                            (st.session_state["admin_username"], selected_student, current_timestamp, reason_code)
                        )
                        conn.commit()

                        st.info(f"""
                        **Student Code:** {student_record['student_code']}  
                        **Full Name:** {student_record['full_name']}  
                        **Batch ID:** {student_record['batch_id']}  
                        **Enrolled On:** {student_record['enrolled_on']}
                        """)
                except sqlite3.Error:
                    conn.rollback()
                    st.error("Identity lookup failed securely.")
                finally:
                    conn.close()
        else:
            st.info("No students available for lookup in this batch.")


# =====================================================
# TAB 3: COMPLIANCE AUDIT LOGS
# =====================================================
with tab_audit:
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    with st.container():
        st.subheader("📋 Administrative Compliance Audit Log")
        st.markdown("<p style='color: #64748b; font-size: 13.5px; margin-bottom: 20px;'>Chronological tracking ledger recording all administrative identity decryption requests with IST timestamps.</p>", unsafe_allow_html=True)

        conn = get_db_connection()
        try:
            audit_df = pd.read_sql_query(
                """
                SELECT id, admin_username, student_code, accessed_at, reason_code
                FROM identity_audit_log
                ORDER BY id DESC
                """,
                conn
            )

            if audit_df.empty:
                st.info("No compliance audit entries recorded yet.")
            else:
                st.dataframe(audit_df, use_container_width=True, hide_index=True)
        except sqlite3.Error:
            st.error("Unable to load compliance audit logs.")
        finally:
            conn.close()


# =====================================================
# 10. FOOTER
# =====================================================
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#94a3b8; font-size:12px; padding:15px;">
    🎓 Student Intelligence Platform &nbsp;•&nbsp; Enterprise Compliance Console
    <br>
    Monitor. Predict. Support.
</div>
""", unsafe_allow_html=True)