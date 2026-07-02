import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Прямая вставка токена, чтобы бот точно авторизовался
TOKEN = "8876675428:AAH6dfbbDMpv2aSpjWDUqOISaiq4Hq6Ub6I"
bot = telebot.TeleBot(TOKEN)

# Настройки текста, ссылки и картинки из твоего ТЗ
TEXT_MESSAGE = "Незнание правил не освобождает от ответственности! Советуем прочитать правила перед общением 🥰"
RULES_LINK = "https://t.me/+QK1Rg1wGUWUzNTgy"
IMAGE_PATH = "photo_2026-07-02_18-46-50.jpg" 

# Функция для создания кнопки под постом
def get_rules_keyboard():
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="❗ПРАВИЛА", url=RULES_LINK)
    markup.add(button)
    return markup

# Отслеживание новых постов в канале @WreokzRBX
@bot.channel_post_handler(func=lambda message: message.chat.username == 'WreokzRBX')
def handle_new_post(message):
    try:
        # Проверяем, на месте ли картинка
        if not os.path.exists(IMAGE_PATH):
            print(f"Ошибка: Файл {IMAGE_PATH} не найден в репозитории!")
            return

        # Открываем изображение и отправляем в комментарии
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
        print(f"Произошла ошибка при отправке комментария: {e}")

# Запуск бота
if __name__ == "__main__":
    print("Бот успешно запущен и ожидает посты в @WreokzRBX...")
    bot.infinity_polling()
