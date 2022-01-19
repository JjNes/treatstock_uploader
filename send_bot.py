import os
import sys
import telebot


if __name__ == '__main__':
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise Exception("Bot token not found")
    try:
        file_path = sys.argv[1]
    except:
        raise Exception("File argv no found")
    try:
        chat_id = sys.argv[2]
    except:
        raise Exception("Chat ID argv no found")
    try:
        caption = sys.argv[3]
    except:
        caption = None
    bot = telebot.TeleBot(token)
    doc = open(file_path,"rb")
    bot.send_document(chat_id, doc, caption=caption)
    