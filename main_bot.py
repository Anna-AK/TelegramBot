import telebot
from extensions import CriptoConverter, APIException
from config import TOKEN, valuts

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = "Чтобы сделать расчет конвертации, введите названия валют в следующем виде: \n " \
           "<что имеем>  <во что переводим>  <сколько хотим взять>. \n" \
           "Например: евро биткоин 3\n\n Список доступных для расчета валют можно увидеть по /valeus"
    bot.reply_to(message, text)

@bot.message_handler(commands=['valeus',])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for k in valuts.keys():
        text = '\n'.join((text, k,))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text',])
def converter(message: telebot.types.Message):
    try:
        vars = message.text.split(' ')

        if len(vars) != 3:
            raise APIException('Параметров должно быть 3.\nПодсказка: /help')

        base, quote, amount = vars
        total, price = CriptoConverter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду{e}')
        
    else:
        text = f'На данный момент цена {quote} в {base} = {price} \nСтоимость {amount} {quote} = {total} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()
