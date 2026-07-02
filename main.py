import os
from threading import Thread
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 1. Веб-сервер для поддержки работы на хостинге Render 24/7
app = Flask('')

@app.route('/')
def home():
    return "Бот @WreokzRBX активен 24/7!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Настройка бота и авторизация
TOKEN = "8876675428:AAH6dfbbDMpv2aSpjWDUqOISaiq4Hq6Ub6I"
bot = telebot.TeleBot(TOKEN)

# Данные для публикации
TEXT_MESSAGE = "Незнание правил не освобождает от ответственности! Советуем прочитать правила перед общением 🥰"
RULES_LINK = "https://t.me/+QK1Rg1wGUWUzNTgy"
IMAGE_PATH = "photo_2026-07-02_18-46-50.jpg" 

# Функция для создания кнопки "ПРАВИЛА"
def get_rules_keyboard():
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="❗ПРАВИЛА", url=RULES_LINK)
    markup.add(button)
    return markup

# Ловим посты, которые Telegram автоматически пересылает в привязанную группу обсуждения
@bot.message_handler(func=lambda message: message.forward_from_chat is not None and message.forward_from_chat.username == 'WreokzRBX')
def handle_discussion_post(message):
    try:
        # Проверяем, существует ли файл изображения в репозитории
        if not os.path.exists(IMAGE_PATH):
            print(f"Ошибка: Файл {IMAGE_PATH} не найден!")
            return

        # Отправляем фото в чат комментариев в качестве ответа на пересланный пост
        with open(IMAGE_PATH, 'rb') as photo:
            bot.send_photo(
                chat_id=message.chat.id,          # ID чата обсуждения (комментариев)
                photo=photo,
                caption=TEXT_MESSAGE,
                reply_to_message_id=message.message_id,  # Отвечаем прямо на этот пост
                reply_markup=get_rules_keyboard()
            )
        print(f"Успешно отправлен комментарий к посту №{message.message_id}")
    except Exception as e:
        print(f"Произошла ошибка при отправке в комментарии: {e}")

# 3. Запуск веб-сервера и бота
if __name__ == "__main__":
    t = Thread(target=run_web_server)
    t.start()
    
    print("Бот успешно запущен и ожидает новые посты в комментариях...")
    bot.infinity_polling()
