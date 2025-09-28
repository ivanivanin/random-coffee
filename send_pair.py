import os
import json
import random
from datetime import datetime
from telegram import Bot

USERS_FILE = "users.json"
MEETINGS_FILE = "meetings.json"

# Загружаем участников
with open(USERS_FILE, "r") as f:
    users = json.load(f)

if len(users) < 2:
    print("❌ Нужно минимум 2 участника. Напишите боту /start.")
    exit()

# Выбираем случайную пару
pair = random.sample(users, 2)
user1, user2 = pair

# Сохраняем встречу
with open(MEETINGS_FILE, "r") as f:
    meetings = json.load(f)

meeting = {
    "id": len(meetings) + 1,
    "user1_id": user1["id"],
    "user2_id": user2["id"],
    "user1_name": user1["name"],
    "user2_name": user2["name"],
    "user1_username": user1.get("username"),
    "user2_username": user2.get("username"),
    "scheduled_at": datetime.utcnow().isoformat(),
    "status": "scheduled"
}

meetings.append(meeting)
with open(MEETINGS_FILE, "w") as f:
    json.dump(meetings, f, indent=2)

# Отправляем сообщения
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

msg1 = f"☕ Ты в Random Coffee! Твой собеседник: @{user2['username'] or user2['name']}\nПожалуйста, свяжитесь и проведите встречу. После — отправьте /confirm_meeting"
msg2 = f"☕ Ты в Random Coffee! Твой собеседник: @{user1['username'] or user1['name']}\nПожалуйста, свяжитесь и проведите встречу. После — отправьте /confirm_meeting"

bot.send_message(chat_id=user1["id"], text=msg1)
bot.send_message(chat_id=user2["id"], text=msg2)

print(f"✅ Встреча назначена: {user1['name']} ↔ {user2['name']}")