import sqlite3
import os

DB_FILE = "academy.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Identity Table (Strict PII Boundary)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students_identity (
        student_code TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        batch_id TEXT NOT NULL,
        enrolled_on TEXT NOT NULL
    )
    """)
    
    # 2. Attendance Weekly Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance_weekly (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_code TEXT NOT NULL,
        week_no INTEGER NOT NULL,
        sessions_attended INTEGER NOT NULL,
        sessions_held INTEGER NOT NULL,
        FOREIGN KEY (student_code) REFERENCES students_identity(student_code)
    )
    """)
    
    # 3. Assessment Weekly Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessment_weekly (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_code TEXT NOT NULL,
        week_no INTEGER NOT NULL,
        assignment_score INTEGER NOT NULL,
        quiz_score INTEGER NOT NULL,
        FOREIGN KEY (student_code) REFERENCES students_identity(student_code)
    )
    """)
    
    # 4. Engagement Weekly Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS engagement_weekly (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_code TEXT NOT NULL,
        week_no INTEGER NOT NULL,
        forum_posts INTEGER NOT NULL,
        late_submissions INTEGER NOT NULL,
        FOREIGN KEY (student_code) REFERENCES students_identity(student_code)
    )
    """)
    
    # 5. Audit Log Table for Identity Lookups
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS identity_audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        student_code TEXT NOT NULL,
        reason_code TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
