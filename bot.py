import os
import json
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Путь к файлу с участниками
USERS_FILE = "users.json"
MEETINGS_FILE = "meetings.json"

# Убедимся, что файлы существуют
for f in [USERS_FILE, MEETINGS_FILE]:
    if not os.path.exists(f):
        with open(f, "w") as file:
            json.dump([], file)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # Сохраняем пользователя
    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    user_data = {
        "id": user.id,
        "username": user.username or f"user_{user.id}",
        "name": user.first_name
    }

    # Не дублируем
    if not any(u["id"] == user.id for u in users):
        users.append(user_data)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)

    await update.message.reply_text(
        "✅ Ты в Random Coffee! Когда придет время — получишь сообщение.\n"
        "После встречи напиши /confirm_meeting"
    )

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(MEETINGS_FILE, "r") as f:
        meetings = json.load(f)

    # Находим последнюю активную встречу с этим пользователем
    for m in reversed(meetings):
        if m["status"] == "scheduled" and update.effective_user.id in [m["user1_id"], m["user2_id"]]:
            m["status"] = "confirmed"
            m["confirmed_at"] = datetime.utcnow().isoformat()
            with open(MEETINGS_FILE, "w") as f:
                json.dump(meetings, f, indent=2)
            await update.message.reply_text("🎉 Спасибо! Встреча подтверждена.")
            return

    await update.message.reply_text("❌ Нет активной встречи для подтверждения.")

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Нужно задать TELEGRAM_BOT_TOKEN в переменных окружения!")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("confirm_meeting", confirm))
    app.run_polling()

if __name__ == "__main__":
    main()