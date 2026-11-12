from fastapi import FastAPI, Depends, HTTPException, Header, Query
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import pandas as pd
import sqlite3

from app.models import get_db_connection, init_db
from app.risk_engine import calculate_risk_score

load_dotenv()
API_KEY = os.getenv("RISK_API_KEY", "secret-key-123")

app = FastAPI(title="ThoorigAI Student At-Risk Predictor", version="1.0.0")

# Enable CORS for frontend dashboard connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY_HEADER = APIKeyHeader(name="x-api-key", auto_error=False)

def verify_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API Key")
    return api_key

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "Student At-Risk Predictor API"}

@app.post("/api/upload/batch")
def upload_batch(file_type: str = Query(..., pattern="^(attendance|assessment|engagement|identity)$"), 
                 api_key: str = Depends(verify_api_key)):
    file_map = {
        "identity": "data/students_identity.csv",
        "attendance": "data/sample_attendance.csv",
        "assessment": "data/sample_assessment.csv",
        "engagement": "data/sample_engagement.csv"
    }
    
    path = file_map.get(file_type)
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"CSV file for {file_type} not found in data/ folder.")
    
    df = pd.read_csv(path)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if file_type == "identity":
            for _, row in df.iterrows():
                cursor.execute("""
                INSERT OR REPLACE INTO students_identity (student_code, full_name, batch_id, enrolled_on)
                VALUES (?, ?, ?, ?)
                """, (row["student_code"], row["full_name"], row["batch_id"], row["enrolled_on"]))
        elif file_type == "attendance":
            cursor.execute("DELETE FROM attendance_weekly")
            for _, row in df.iterrows():
                cursor.execute("""
                INSERT INTO attendance_weekly (student_code, week_no, sessions_attended, sessions_held)
                VALUES (?, ?, ?, ?)
                """, (row["student_code"], row["week_no"], row["sessions_attended"], row["sessions_held"]))
        elif file_type == "assessment":
            cursor.execute("DELETE FROM assessment_weekly")
            for _, row in df.iterrows():
                cursor.execute("""
                INSERT INTO assessment_weekly (student_code, week_no, assignment_score, quiz_score)
                VALUES (?, ?, ?, ?)
                """, (row["student_code"], row["week_no"], row["assignment_score"], row["quiz_score"]))
        elif file_type == "engagement":
            cursor.execute("DELETE FROM engagement_weekly")
            for _, row in df.iterrows():
                cursor.execute("""
                INSERT INTO engagement_weekly (student_code, week_no, forum_posts, late_submissions)
                VALUES (?, ?, ?, ?)
                """, (row["student_code"], row["week_no"], row["forum_posts"], row["late_submissions"]))
                
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
        
    return {"status": "success", "file_type": file_type, "rows_processed": len(df)}

@app.get("/api/risk/batch/{batch_id}")
def get_batch_risk(batch_id: str, api_key: str = Depends(verify_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT student_code FROM students_identity WHERE batch_id = ?", (batch_id,))
    students = cursor.fetchall()
    
    if not students:
        conn.close()
        raise HTTPException(status_code=404, detail=f"No students found for batch {batch_id}")
        
    results = []
    for s in students:
        scode = s["student_code"]
        
        cursor.execute("SELECT week_no, sessions_attended, sessions_held FROM attendance_weekly WHERE student_code = ?", (scode,))
        att = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT week_no, assignment_score, quiz_score FROM assessment_weekly WHERE student_code = ?", (scode,))
        asm = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT week_no, forum_posts, late_submissions FROM engagement_weekly WHERE student_code = ?", (scode,))
        eng = [dict(row) for row in cursor.fetchall()]
        
        score, band, trend, week, factors = calculate_risk_score(att, asm, eng)
        
        results.append({
            "student_code": scode,
            "risk_score": score,
            "risk_band": band,
            "trend_warning": trend,
            "latest_week": week,
            "factors": factors
        })
        
    conn.close()
    results.sort(key=lambda x: x["risk_score"], reverse=True)
    return {"batch_id": batch_id, "student_count": len(results), "students": results}

@app.get("/api/students/{student_code}/identity")
def get_student_identity(student_code: str, reason_code: str = Query(...), api_key: str = Depends(verify_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO identity_audit_log (student_code, reason_code) VALUES (?, ?)", (student_code, reason_code))
    conn.commit()
    
    cursor.execute("SELECT student_code, full_name, batch_id, enrolled_on FROM students_identity WHERE student_code = ?", (student_code,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Student identity not found")
        
    return dict(row)
