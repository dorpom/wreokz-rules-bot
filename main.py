import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Авторизация бота
TOKEN = "8876675428:AAH6dfbbDMpv2aSpjWDUqOISaiq4Hq6Ub6I"
bot = telebot.TeleBot(TOKEN)

# Данные для красивого поста (текст с HTML-тегами для жирного шрифта)
TEXT_MESSAGE = "<b>Незнание правил не освобождает от ответственности!</b>\n\nСоветуем прочитать <b>правила</b> перед общением 🥰"
RULES_LINK = "https://t.me/+QK1Rg1wGUWUzNTgy"

# Автоматически определяем полный путь к картинке на PythonAnywhere
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "photo_2026-07-02_18-46-50.jpg")

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
        # Проверяем, существует ли файл изображения в папке
        if not os.path.exists(IMAGE_PATH):
            print(f"Ошибка: Файл {IMAGE_PATH} не найден!")
            return

        # Отправляем фото в чат комментариев в качестве ответа на пересланный пост
        with open(IMAGE_PATH, 'rb') as photo:
            bot.send_photo(
                chat_id=message.chat.id,                # ID чата обсуждения (комментариев)
                photo=photo,
                caption=TEXT_MESSAGE,
                parse_mode='HTML',                      # Включаем жирный шрифт
                reply_to_message_id=message.message_id,  # Отвечаем прямо на этот пост
                reply_markup=get_rules_keyboard()
            )
        print(f"Успешно отправлен красивый комментарий к посту №{message.message_id}")
    except Exception as e:
        print(f"Произошла ошибка при отправке в комментарии: {e}")

if __name__ == "__main__":
    print("Бот успешно запущен на PythonAnywhere и ожидает новые посты...")
    bot.infinity_polling()
