import telebot

from config import keys, TOKEN
from extensions import APIException, CryptoConverter, ServerException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = (
        "Чтобы начать работу, введите команду боту в следующем формате:\n"
        "<имя валюты, цену которой хотите узнать> "
        "<имя валюты, в которой надо узнать цену первой валюты> "
        "<количество первой валюты>\n"
        "Пример: евро рубль 100\n\n"
        "Увидеть список всех доступных валют: /values"
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values (message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров. Нужно ввести 3: изначальная валюту, валюту перевода и количество.')

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except ServerException as e:
        bot.reply_to(message, f'Ошибка сервера.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = total_base
        bot.send_message(message.chat.id, text)

bot.polling()