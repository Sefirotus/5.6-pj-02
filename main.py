import telebot

from CONFIG import *
from extensions import CryptoConverter, ConvExc


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтобы конвертировать, введие валюту через пробел, в формате \n<имя валюты>' \
           '<во что перевод>' \
           '<количество>' \
           'Увидеть список всех доступных валют'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text='\n'.join((text, key, ))
        bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ConvExc("Слишком много параметров")
        if len(values)  < 3:
            raise ConvExc("Слишком мало параметров")

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)

    except ConvExc as e:
        bot.reply_to(message, f'Ощибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()