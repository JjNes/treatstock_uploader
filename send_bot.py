import os
import sys
import telebot


if __name__ == '__main__':
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise Exception("Bot token not found")
    try:
        file_path = sys.argv[1]
    except Exception:
        raise Exception("File argv no found")
    try:
        chat_id = sys.argv[2]
    except Exception:
        raise Exception("Chat ID argv no found")
    try:
        caption = sys.argv[3]
    except Exception:
        caption = None
    bot = telebot.TeleBot(token)
    bot.unpin_all_chat_messages(chat_id)
    doc = open(file_path, "rb")
    message = bot.send_document(chat_id, doc, caption=caption)
    bot.pin_chat_message(chat_id, message.id)
e