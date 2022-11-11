from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, db
from keyboards.reply import generate_contact_button,\
    generate_main_menu, generate_locations, generate_categories

from keyboards.inline import generate_products_pagination

def start_register(message: Message):
    chat_id = message.chat.id
    '''Спросить, а есть ли в базе пользователь с таким chat_id
    Если его нет - начать регистрацию, а если есть - показать главное меню'''
    user = db.get_user_by_id(chat_id)
    if user:
        '''Показать главное меню'''
        show_main_menu(message)
    else:
        msg = bot.send_message(chat_id, 'Отправьте свои имя и фамилию')
        bot.register_next_step_handler(msg, get_name_ask_phone)


def get_name_ask_phone(message: Message):
    full_name = message.text
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Отправьте номер телефона, нажав на кнопку',
                           reply_markup=generate_contact_button())
    bot.register_next_step_handler(msg, finish_register, full_name)


def finish_register(message: Message, full_name):
    telegram_id = message.chat.id
    contact = message.contact.phone_number
    db.register_user(telegram_id, full_name, contact)
    bot.send_message(telegram_id, 'Регистрация прошла успешно')
    show_main_menu(message)


def show_main_menu(message: Message):
    chat_id = message.chat.id
    text = 'Что хотите сделать?'
    bot.send_message(chat_id, text, reply_markup=generate_main_menu())


@bot.message_handler(regexp='Информация ⚠')
def info(message: Message):
    chat_id = message.chat.id

    #bot.send_location(chat_id, 41.29691342529716, 69.27442629920108, longitude)
    bot.send_message(chat_id, 'Выберите филиал', reply_markup=generate_locations())


locations = db.get_locations()
locations = [i[3] for i in locations]


@bot.message_handler(func=lambda message: message.text in locations)
def send_loc_by_name(message: Message):
    chat_id = message.chat.id
    loc = db.get_loc_by_name(message.text)
    bot.send_location(chat_id, loc[1], loc[2])
    show_main_menu(message)


@bot.message_handler(regexp='Сделать заказ 🛍')
def make_order(message: Message):
    chat_id = message.chat.id
    text = 'Выберите категорию товаров'
    bot.send_message(chat_id, text, reply_markup=generate_categories())


categories = db.get_categories()
categories = [item[0] for item in categories]


@bot.message_handler(func=lambda message: message.text in categories)
def reaction_to_category(message: Message):
    chat_id = message.chat.id
    text = 'Выберите товар: '
    your_choice = f'Вы выбрали категорию: {message.text}'
    bot.send_message(chat_id, your_choice, reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id, text, reply_markup=generate_products_pagination(message.text))
    # 1 >>
    # <<  3  >>
    # <<  6




