#!/bin/bash
cd "$(dirname "$0")"

echo "=== 45-Maktab Web Serveri ==="

# Install dependencies if needed
if ! python3 -c "import fastapi" 2>/dev/null; then
  echo "[*] Kutubxonalar o'rnatilmoqda..."
  pip3 install -r requirements.txt -q
fi

# Seed database if not exists
if [ ! -f maktab.db ]; then
  echo "[*] Ma'lumotlar bazasi yaratilmoqda..."
  python3 seed.py
fi

echo ""
echo "[✓] Server ishga tushmoqda: http://localhost:8000"
echo "[✓] Sahifalar:"
echo "     http://localhost:8000/          — Landing page"
echo "     http://localhost:8000/login.html    — Kirish"
echo "     http://localhost:8000/dashboard.html — Dashboard"
echo ""
echo "[!] Serial sahna — hack buyrug'i:"
echo '    curl -X POST http://localhost:8000/api/grades/update \'
echo '         -H "Content-Type: application/json" \'
echo '         -d '"'"'{"student_id": 5, "subject": "Matematika", "grade": 5, "quarter": 2}'"'"''
echo ""

python3 main.py
