import os
from threading import Thread
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 1. Веб-сервер, который требует Render
app = Flask('')

@app.route('/')
def home():
    return "Бот @WreokzRBX активен 24/7!"

def run_web_server():
    # На Render порт берется из переменных окружения
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Настройка бота
TOKEN = "8876675428:AAH6dfbbDMpv2aSpjWDUqOISaiq4Hq6Ub6I"
bot = telebot.TeleBot(TOKEN)

TEXT_MESSAGE = "Незнание правил не освобождает от ответственности! Советуем прочитать правила перед общением 🥰"
RULES_LINK = "https://t.me/+QK1Rg1wGUWUzNTgy"
IMAGE_PATH = "photo_2026-07-02_18-46-50.jpg" 

def get_rules_keyboard():
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="❗ПРАВИЛА", url=RULES_LINK)
    markup.add(button)
    return markup

@bot.channel_post_handler(func=lambda message: message.chat.username == 'WreokzRBX')
def handle_new_post(message):
    try:
        if not os.path.exists(IMAGE_PATH):
            print(f"Ошибка: Файл {IMAGE_PATH} не найден!")
            return

        with open(IMAGE_PATH, 'rb') as photo:
            bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=TEXT_MESSAGE,
                reply_to_message_id=message.message_id,
                reply_markup=get_rules_keyboard()
            )
        print(f"Успешно отправлен комментарий к посту №{message.message_id}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# 3. Запуск
if __name__ == "__main__":
    t = Thread(target=run_web_server)
    t.start()
    
    print("Бот успешно запущен...")
    bot.infinity_polling()
