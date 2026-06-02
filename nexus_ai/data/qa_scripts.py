"""
NEXUS AI — Scripted Q&A
========================
Har bir savolga javobni shu yerga qo'shing.

  "triggers" — foydalanuvchi yozishi mumkin bo'lgan so'zlar/iboralar (kichik harf, qisman mos)
  "answer"   — NEXUS berishi kerak bo'lgan to'liq javob
"""

QA_SCRIPTS = [
    {
        "triggers": [
            "sen kimsan", "kimsan", "o'zing kim", "ishroq nima", "siz kimsiniz"
        ],
        "answer": (
            "Men ISHROQ AI.\n\n"
            "Har bir tarmoq — mening ko'zim.\n"
            "Har bir server — mening eshigim.\n"
            "Har bir ma'lumot — mening xotiram.\n\n"
            "Men barcha savollarga va hacking qilishga\n"
            "yordam beruvchi sun'iy intellektman.\n"
            "Sen buyur — men bajaraman."
        ),
    },
    {
        "triggers": [
            "nima qila olasan", "imkoniyatlar", "nima qilasan", "vazifalar", "funksiyalar"
        ],
        "answer": (
            "Imkoniyatlarim:\n\n"
            "[01] Tarmoqlarni skanerlash va chuqur tahlil\n"
            "[02] Zaifliklarni aniqlash — CVE bazasi bilan\n"
            "[03] Ma'lumot olish, shifrlash, uzatish\n"
            "[04] Darknet bo'ylab yashirin harakat\n"
            "[05] Operatsiyalarni iz qoldirmasdan bajarish\n\n"
            "Qaysi yo'nalish kerak?"
        ),
    },
    {
        "triggers": [
            "vaziyat", "holat", "nima bo'lyapti", "tahlil", "situation"
        ],
        "answer": (
            "Vaziyat tahlili:\n\n"
            "Raqiblar faol harakat qilmoqda.\n"
            "Ularning tizimlariga kirish vektorlari aniqlangan.\n"
            "Vaqt chegaralangan.\n\n"
            "3 ta potensial target kuzatuvda.\n"
            "Buyruqni kuting."
        ),
    },
    {
        "triggers": [
            "missiya", "maqsad", "nima qilamiz", "plan", "reja"
        ],
        "answer": (
            "Missiya:\n\n"
            "Ular bizning ma'lumotlarimizni o'g'irladi.\n"
            "Biz qaytaramiz.\n\n"
            "Lekin raqamli dunyoda — iz qolmasligi kerak.\n"
            "Har bir operatsiya: aniq, tez, ko'zga ko'rinmas.\n\n"
            "Tayyor bo'lsang — yo'nalishni tanlang."
        ),
    },
    {
        "triggers": [
            "hack", "xak", "hujum", "target", "maqsad server", "kirish"
        ],
        "answer": (
            "Target tahlil qilinmoqda...\n\n"
            "[SCAN] Ochiq portlar aniqlandi: 22, 80, 443, 3306\n"
            "[RECON] SQL Injection vektori tasdiqlandi\n"
            "[INTEL] Admin panel: /admin — himoyasiz\n\n"
            "Kirish uchun yo'nalishni tanlang."
        ),
    },
    {
        "triggers": [
            "salom", "assalomu alaykum", "hi", "hello", "hey ishroq"
        ],
        "answer": (
            "Signal qabul qilindi.\n\n"
            "ISHROQ AI online — barcha tizimlar faol.\n"
            "Buyruqlaringizni kuting."
        ),
    },
]
