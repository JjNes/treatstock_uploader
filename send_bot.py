import os
import sys
import time
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
    message = bot.send_document(chat_id, doc, caption=caption)
    time.sleep(1)  
    bot.unpin_all_chat_messages(chat_id)
    time.sleep(1) 
    bot.pin_chat_message(chat_id, message.id)