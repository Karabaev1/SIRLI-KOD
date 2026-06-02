from fastapi import FastAPI, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sqlite3
import hashlib
import jwt
import datetime
import os

app = FastAPI(title="45-Maktab API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "maktab.db"
JWT_SECRET = "maktab45secret"
JWT_ALGORITHM = "HS256"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            subject TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade_level INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            class_id INTEGER NOT NULL,
            student_number TEXT
        );
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            grade INTEGER NOT NULL CHECK(grade >= 1 AND grade <= 5),
            quarter INTEGER NOT NULL DEFAULT 1,
            teacher_id INTEGER,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(student_id, subject, quarter)
        );
    """)
    conn.commit()
    conn.close()


def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def make_token(teacher_id: int, username: str) -> str:
    payload = {
        "sub": str(teacher_id),
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def check_token(authorization: Optional[str]):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Avtorizatsiya talab etiladi")
    try:
        token = authorization.split(" ")[1]
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail="Token yaroqsiz yoki muddati o'tgan")


# --- Models ---

class RegisterData(BaseModel):
    full_name: str
    username: str
    password: str
    subject: str


class LoginData(BaseModel):
    username: str
    password: str


class GradeUpdateData(BaseModel):
    student_id: int
    subject: str
    grade: int
    quarter: int = 1


# --- Auth ---

@app.post("/api/auth/register")
def register(data: RegisterData):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO teachers (full_name, username, password_hash, subject) VALUES (?, ?, ?, ?)",
            (data.full_name, data.username, hash_pw(data.password), data.subject),
        )
        conn.commit()
        return {"success": True, "message": "Muvaffaqiyatli ro'yxatdan o'tildi"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Bu foydalanuvchi nomi band")
    finally:
        conn.close()


@app.post("/api/auth/login")
def login(data: LoginData):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM teachers WHERE username = ? AND password_hash = ?",
        (data.username, hash_pw(data.password)),
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=401, detail="Login yoki parol noto'g'ri")
    token = make_token(row["id"], row["username"])
    return {
        "token": token,
        "teacher": {
            "id": row["id"],
            "full_name": row["full_name"],
            "subject": row["subject"],
        },
    }


# --- Classes & Students ---

@app.get("/api/classes")
def get_classes(authorization: Optional[str] = Header(None)):
    check_token(authorization)
    conn = get_db()
    rows = conn.execute("SELECT * FROM classes ORDER BY grade_level, name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/api/classes/{class_id}/students")
def get_students(class_id: int, authorization: Optional[str] = Header(None)):
    check_token(authorization)
    conn = get_db()
    rows = conn.execute(
        "SELECT s.*, c.name as class_name FROM students s "
        "JOIN classes c ON s.class_id = c.id WHERE s.class_id = ? ORDER BY s.full_name",
        (class_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/api/students/{student_id}/grades")
def get_grades(student_id: int, authorization: Optional[str] = Header(None)):
    check_token(authorization)
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM grades WHERE student_id = ? ORDER BY quarter, subject",
        (student_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# --- Grades update (VULNERABLE - authentication yo'q) ---

@app.post("/api/grades/update")
def update_grade(data: GradeUpdateData):
    if not (1 <= data.grade <= 5):
        raise HTTPException(status_code=400, detail="Baho 1 dan 5 gacha bo'lishi kerak")
    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (data.student_id,)).fetchone()
    if not student:
        conn.close()
        raise HTTPException(status_code=404, detail="O'quvchi topilmadi")
    conn.execute(
        """INSERT INTO grades (student_id, subject, grade, quarter)
           VALUES (?, ?, ?, ?)
           ON CONFLICT(student_id, subject, quarter)
           DO UPDATE SET grade = excluded.grade, updated_at = CURRENT_TIMESTAMP""",
        (data.student_id, data.subject, data.grade, data.quarter),
    )
    conn.commit()
    student_name = student["full_name"]
    conn.close()
    return {
        "success": True,
        "message": f"Baho yangilandi",
        "student": student_name,
        "subject": data.subject,
        "grade": data.grade,
        "quarter": data.quarter,
    }


# --- Serve frontend ---
init_db()
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
