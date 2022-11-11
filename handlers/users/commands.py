from telebot.types import Message
from data.loader import bot, db
from .text_handlers import start_register

@bot.message_handler(commands=['start', 'help', 'about'])
def commands(message: Message):
    chat_id = message.chat.id
    if message.text == '/start':
        text = f'''Здравствуйте, {message.from_user.first_name}
Вас приветствует бот интернет магазин'''
        bot.send_message(chat_id, text)
        start_register(message)

    elif message.text == '/help':
        text = f'''Если у вас возникли ошибки, или идеи
Напишите нам сюда: @FomichevEvgeniy'''
        bot.send_message(chat_id, text)
    elif message.text == '/about':
        text = f'''Данный бот был создан при поддержке PROWEB
Во время написания бота ни один студент не пострадал'''
        bot.send_message(chat_id, text)


