import os
import requests

BOT_TOKEN = os.environ["8563381666:AAG6oWI5amPn0PQ274oh9iC47gNBU1DiAV0"]
CHAT_ID = os.environ["CHAT_ID"]

message = "🔔 Rappel BLS Espagne Tanger : vérifie les rendez-vous maintenant."

url = f"https://api.telegram.org/bot{8563381666:AAG6oWI5amPn0PQ274oh9iC47gNBU1DiAV0}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": message
}

requests.post(url, data=data)
