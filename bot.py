import telebot
from bot_logic import gen_pass
from bot_logic import flip_coin
from bot_logic import gen_emodji
from telebot.types import ReactionTypeEmoji
import random
import time, threading, schedule
#ВНИМАНИЕ!!! БОТ НЕ РАБОТАЕТ БЕЗ bot_logic
#Вместо ТОКЕN - твой api токен
bot = telebot.TeleBot("TOKEN")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['help'])
def send_hello(message):
    bot.reply_to(message, "/start - запуск бота, /hello - приветствие, /help - помощь, /bye - прощание, /pswd - генерация паролля,  /emodji - рандомный эмодзи, /coin - орёл или решка, /timer - таймер, /set <seconds> - установка времени таймера, /unset - сборс таймера")


@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['pswd'])
def send_password(message):
    password = gen_pass(10)  # Устанавливаем длину пароля, например, 10 символов
    bot.reply_to(message, f"Вот твой сгенерированный пароль: {password}")

@bot.message_handler(commands=['emodji'])
def send_emodji(message):
    emodji = gen_emodji()
    bot.reply_to(message, f"Вот эмоджи': {emodji}")

@bot.message_handler(commands=['coin'])
def send_coin(message):
    coin = flip_coin()
    bot.reply_to(message, f"Монетка выпала так: {coin}")

@bot.message_handler(commands=['timer'])
def send_welcome(message):
    bot.reply_to(message, "Use /set <seconds> to set a timer")


def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text='Beeeeep!')


@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        schedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)
    else:
        bot.reply_to(message, 'Usage: /set <seconds>')


@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)


if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)

bot.polling()
