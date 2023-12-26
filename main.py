import telebot
from telebot import types

from config import currencies, TOKEN
from extensions import CurrencyConverter, APIException


bot = telebot.TeleBot(TOKEN)


def create_markup(from_currency=None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for val in currencies.keys():
        if val != from_currency:
            buttons.append(types.KeyboardButton(val.capitalize()))
    markup.add(*buttons)
    return markup


@bot.message_handler(commands=['start', 'help'])
def help_command(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду: /convert' \
           '\nУвидить список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values_command(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = "Выберите валюту, из которой конвертировать:"
    bot.send_message(message.chat.id, text, reply_markup=create_markup())
    bot.register_next_step_handler(message, from_currency_handler)


def from_currency_handler(message: telebot.types.Message):
    from_currency = message.text.strip()
    text = "Выберите валюту, в которую конвертировать:"
    bot.send_message(message.chat.id, text, reply_markup=create_markup(from_currency))
    bot.register_next_step_handler(message, to_currency_handler, from_currency)


def to_currency_handler(message: telebot.types.Message, from_currency):
    to_currency = message.text.strip()
    text = "Выберите количесвто конвертируемой валюты:"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, from_currency, to_currency)


def amount_handler(message: telebot.types.Message, from_currency, to_currency):
    amount = message.text.strip()
    try:
        result = CurrencyConverter.get_price(from_currency, to_currency, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f"{amount} \"{currencies[from_currency]}\" = {result * float(amount)} \"{currencies[to_currency]}\""
        bot.send_message(message.chat.id, text)


bot.polling()