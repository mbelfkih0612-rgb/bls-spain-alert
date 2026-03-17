import os
import hashlib
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://blsspainmorocco.com/tangier/french/"
STATE_FILE = "last_hash.txt"

KEYWORDS = [
    "rendez-vous",
    "disponible",
    "appointment",
    "available",
    "slot",
    "slots",
    "visa"
]

def send_telegram(message):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api_url, data={"chat_id": CHAT_ID, "text": message}, timeout=20)

def get_page_text():
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())

def get_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def load_old_hash():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def save_hash(value):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(value)

page_text = get_page_text()
page_text_lower = page_text.lower()

new_hash = get_hash(page_text)
old_hash = load_old_hash()

found_keywords = [word for word in KEYWORDS if word in page_text_lower]

if old_hash is None:
    save_hash(new_hash)
    send_telegram("✅ Surveillance intelligente BLS Tanger activée.")
elif new_hash != old_hash:
    save_hash(new_hash)
    if found_keywords:
        send_telegram(
            "🚨 Changement détecté sur la page BLS Tanger.\n"
            "Mots trouvés : " + ", ".join(found_keywords) + "\n" +
            URL
        )
