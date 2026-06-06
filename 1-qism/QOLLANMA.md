# 1-QISM: PHISHING SAHNA — QOLLANMA

Azim Aliga phishing yuboradi, Ali tuzog'ga tushadi.

---

## Talab qilinadigan dasturlar

```bash
sudo apt install python3 python3-pip python3-venv -y
```

---

## O'rnatish (bir marta)

```bash
cd 1-qism/Azim
python3 -m venv venv
venv/bin/pip install fastapi uvicorn
```

---

## Ishga tushirish tartibi

### 1. Server (Azim kompyuterida ishga tushiriladi)

```bash
cd 1-qism/Azim
venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001
```

Server ikkala tomondan ham ishlatiladi — bitta server yetarli.

---

### 2. Ali ekrani — Notification daemon

Yangi terminal:

```bash
cd 1-qism/Ali
python3 notifier.py
```

Ekranning o'ng pastki burchagida kutib turadi (ko'rinmaydi).

---

### 3. Azim ekrani — Admin panel

Browserda oching:

```
http://localhost:8001/admin
```

---

## Sahna jarayoni

```
1. Azim admin panelni ochadi
2. "Hujumni boshlash" tugmasini bosadi
3. Ali ekranida MINECRAFT CHAMPIONSHIP popup chiqadi
4. Ali "✅ Qabul qilish" ni bosadi
5. Phishing sahifa ochiladi (Minecraft logo, bayroq, 50 mln so'm)
6. Ali karta ma'lumotlarini kiritadi
7. Azim admin panelida real-vaqtda ko'rinadi
```

---

## Agar ikki alohida kompyuter ishlatilsa

Ali va Azim kompyuterlari bir xil Wi-Fi tarmog'ida bo'lishi kerak.

Azim kompyuterining IP sini aniqlang:
```bash
ip a | grep "inet " | grep -v 127
```

Keyin `Ali/notifier.py` va `Ali/notification.html` va `Ali/phishing.html` dagi:
```
API = 'http://localhost:8001'
```
qatorini:
```
API = 'http://<AZIM_IP>:8001'
```
ga almashtiring.

---

## Sahifalar

| Sahifa | URL |
|--------|-----|
| Azim admin panel | `http://localhost:8001/admin` |
| Ali notification (browser) | `http://localhost:8001/notification` |
| Phishing sahifa | `http://localhost:8001/phishing` |
