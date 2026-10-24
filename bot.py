
import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}/"
APP_URL = "https://pvlvd001-stack.github.io/nicotine-free-app/"


def telegram(method, data):
    body = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(API + method, data=body)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def send_message(chat_id, text):
    return telegram("sendMessage", {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": json.dumps({
            "inline_keyboard": [[{
                "text": "🚀 Открыть приложение",
                "web_app": {"url": APP_URL}
            }]]
        }, ensure_ascii=False)
    })


def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()

    if text.startswith("/start"):
        send_message(
            chat_id,
            "🌿 Добро пожаловать в «Свобода от никотина»!\n\n"
            "Каждый день без никотина — шаг к свободе.\n\n"
            "Открой приложение и начни свой путь."
        )
    elif text.startswith("/help"):
        send_message(
            chat_id,
            "💚 Сильная тяга обычно проходит волнами.\n\n"
            "Попробуй подождать 5 минут, выпить воды, "
            "медленно подышать и сменить обстановку.\n\n"
            "Ты можешь справиться с этим моментом."
        )




def main():
    
    updates = telegram("getUpdates", {
        "timeout": 0,
        "offset": -1
    })
  
    print(
        "Получено обновлений:",
        len(updates.get("result", [])),
        flush=True
    )


    for update in updates.get("result", []):
        if "message" in update:
            handle_message(update["message"])

        telegram("getUpdates", {
            "offset": update["update_id"] + 1,
            "timeout": 0
        })


if __name__ == "__main__":
    main()
