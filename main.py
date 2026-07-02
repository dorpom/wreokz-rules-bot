import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Вместо вставки токена в код, хостинг будет безопасно брать его из настроек
TOKEN = os.environ.get('8876675428:AAH6dfbbDMpv2aSpjWDUqOISaiq4Hq6Ub6I')
bot = telebot.TeleBot(TOKEN)

TEXT_MESSAGE = "Незнание правил не освобождает от ответственности! Советуем прочитать правила перед общением 🥰"
RULES_LINK = "https://t.me/+QK1Rg1wGUWUzNTgy"
IMAGE_PATH = "1000008943.jpg" 

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

if __name__ == "__main__":
    print("Бот успешно запущен на Bot-Hosting...")
    bot.infinity_polling()
