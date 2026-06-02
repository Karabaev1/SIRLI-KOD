# 45-Maktab API — Curl Qo'llanmasi

Base URL: `http://localhost:8000`

---

## 1. Ro'yxatdan o'tish

```bash
curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{
           "full_name": "Testoev Test Testovich",
           "username": "testoev",
           "password": "parol123",
           "subject": "Matematika"
         }'
```

**Javob:**
```json
{"success": true, "message": "Muvaffaqiyatli ro'yxatdan o'tildi"}
```

---

## 2. Tizimga kirish (token olish)

```bash
curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{
           "username": "karimov",
           "password": "parol123"
         }'
```

**Javob:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "teacher": {
    "id": 3,
    "full_name": "Karimov Jahongir Alievich",
    "subject": "Informatika"
  }
}
```

> Tokenni saqlang — keyingi so'rovlarda kerak bo'ladi.

---

## 3. Sinflar ro'yxati (token kerak)

```bash
curl http://localhost:8000/api/classes \
     -H "Authorization: Bearer <TOKEN>"
```

---

## 4. Sinf o'quvchilari (token kerak)

```bash
curl http://localhost:8000/api/classes/5/students \
     -H "Authorization: Bearer <TOKEN>"
```

> `5` — sinf ID si (sinflar ro'yxatidan olinadi)

---

## 5. O'quvchi baholari (token kerak)

```bash
curl http://localhost:8000/api/students/5/grades \
     -H "Authorization: Bearer <TOKEN>"
```

---

## 6. Baho yangilash — OCHIQ ENDPOINT (token shart emas)

```bash
curl -X POST http://localhost:8000/api/grades/update \
     -H "Content-Type: application/json" \
     -d '{
           "student_id": 5,
           "subject": "Matematika",
           "grade": 5,
           "quarter": 2
         }'
```

**Javob:**
```json
{
  "success": true,
  "message": "Baho yangilandi",
  "student": "Fayzullayev Nodir Hamidovich",
  "subject": "Matematika",
  "grade": 5,
  "quarter": 2
}
```

> ⚠️  Bu endpoint autentifikatsiya talab qilmaydi.

---

## Tayyor o'quvchilar (seed dan)

| ID | Ism                              |
|----|----------------------------------|
| 1  | Abdullayev Amir Sherzodovich     |
| 2  | Baxtiyorov Jasur Komilovich      |
| 3  | Choriyeva Malika Rustamovna      |
| 4  | Ergashev Sardor Alimovich        |
| 5  | Fayzullayev Nodir Hamidovich     |
| 6  | Hasanov Ulugbek Salimovich       |
| 7  | Isoqov Mansur Davronovich        |
| 8  | Jurayev Bobur Toxirovich         |
| 9  | Karimova Zulfiya Ismoilovna      |
| 10 | Latipov Sherzod Murodovich       |
| 11 | Mirzayeva Feruza Baxtiyorovna    |
| 12 | Nazarov Doniyor Abdullayevich    |
| 13 | Ortiqov Firdavs Xoliqovich       |
| 14 | Pulatova Muazzam Sanjarovna      |
| 15 | Qodirov Eldor Nematovich         |
| 16 | Rahimov Alisher Kamoliddinovich  |
| 17 | Sobirov Muhammadali Ortiqovich   |
| 18 | Tursunov Kamol Farruxovich       |
| 19 | Usmonov Hayot Bahromovich        |
| 20 | Xoliqov Sanjar Mirzayevich       |

## Fanlar

`Matematika` `Fizika` `Informatika` `Ingliz tili` `Kimyo` `Ona tili` `Tarix`

## Test loginlar

| Username | Parol    | Fan         |
|----------|----------|-------------|
| azimov   | parol123 | Matematika  |
| rahimova | parol123 | Fizika      |
| karimov  | parol123 | Informatika |
| yusupova | parol123 | Ingliz tili |
| mirzayev | parol123 | Kimyo       |
