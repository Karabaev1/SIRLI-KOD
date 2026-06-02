import sqlite3
import hashlib
import random

DB_PATH = "maktab.db"

def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

conn = sqlite3.connect(DB_PATH)
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

# O'qituvchilar
teachers = [
    ("Azimov Bekzod Hamidovich",      "azimov",   hash_pw("parol123"), "Matematika"),
    ("Rahimova Nilufar Toxirovna",     "rahimova", hash_pw("parol123"), "Fizika"),
    ("Karimov Jahongir Alievich",      "karimov",  hash_pw("parol123"), "Informatika"),
    ("Yusupova Shahnoza Baxtiyorovna", "yusupova", hash_pw("parol123"), "Ingliz tili"),
    ("Mirzayev Otabek Salimovich",     "mirzayev", hash_pw("parol123"), "Kimyo"),
]
for t in teachers:
    conn.execute(
        "INSERT OR IGNORE INTO teachers (full_name, username, password_hash, subject) VALUES (?,?,?,?)", t
    )

# Sinflar
classes = [
    ("7-A", 7), ("7-B", 7),
    ("8-A", 8), ("8-B", 8),
    ("9-A", 9), ("9-B", 9),
    ("10-A", 10), ("11-A", 11),
]
for c in classes:
    conn.execute("INSERT OR IGNORE INTO classes (name, grade_level) VALUES (?,?)", c)
conn.commit()

# 9-A sinf o'quvchilari
names_9a = [
    "Abdullayev Amir Sherzodovich",
    "Baxtiyorov Jasur Komilovich",
    "Choriyeva Malika Rustamovna",
    "Ergashev Sardor Alimovich",
    "Fayzullayev Nodir Hamidovich",
    "Hasanov Ulugbek Salimovich",
    "Isoqov Mansur Davronovich",
    "Jurayev Bobur Toxirovich",
    "Karimova Zulfiya Ismoilovna",
    "Latipov Sherzod Murodovich",
    "Mirzayeva Feruza Baxtiyorovna",
    "Nazarov Doniyor Abdullayevich",
    "Ortiqov Firdavs Xoliqovich",
    "Pulatova Muazzam Sanjarovna",
    "Qodirov Eldor Nematovich",
    "Rahimov Alisher Kamoliddinovich",
    "Sobirov Muhammadali Ortiqovich",
    "Tursunov Kamol Farruxovich",
    "Usmonov Hayot Bahromovich",
    "Xoliqov Sanjar Mirzayevich",
]

cid = conn.execute("SELECT id FROM classes WHERE name='9-A'").fetchone()[0]
for i, name in enumerate(names_9a, 1):
    conn.execute(
        "INSERT OR IGNORE INTO students (full_name, class_id, student_number) VALUES (?,?,?)",
        (name, cid, f"2024{cid:02d}{i:03d}"),
    )
conn.commit()

# Baholar
subjects = ["Matematika", "Fizika", "Informatika", "Ingliz tili", "Kimyo", "Ona tili", "Tarix"]
random.seed(42)
sids = [r[0] for r in conn.execute("SELECT id FROM students WHERE class_id=?", (cid,)).fetchall()]
for sid in sids:
    for subj in subjects:
        for q in [1, 2, 3]:
            g = random.randint(3, 5)
            conn.execute(
                "INSERT OR IGNORE INTO grades (student_id, subject, grade, quarter) VALUES (?,?,?,?)",
                (sid, subj, g, q),
            )
conn.commit()
conn.close()

print("✓ Ma'lumotlar bazasi tayyor!")
print("\nTest login:")
print("  Username: karimov")
print("  Parol:    parol123")
print("\nVulnerable endpoint:")
print('  curl -X POST http://localhost:8000/api/grades/update \\')
print('       -H "Content-Type: application/json" \\')
print('       -d \'{"student_id": 5, "subject": "Matematika", "grade": 5, "quarter": 2}\'')
