from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from data.loader import db

def generate_contact_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text='Отправить контакт', request_contact=True)
    markup.add(btn)
    return markup


def generate_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    order = KeyboardButton(text='Сделать заказ 🛍')
    cart = KeyboardButton(text='Корзина 🛒')
    feedback = KeyboardButton(text='Написать отзыв ✨')
    settings = KeyboardButton(text='Настройки ⚙')
    info = KeyboardButton(text='Информация ⚠')
    markup.row(order)
    markup.row(cart, feedback)
    markup.row(settings, info)
    return markup

def generate_locations():
    locations = db.get_locations()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for loc_id, latitude, longitude, name in locations:
        btn = KeyboardButton(text=name)
        markup.add(btn)
    return markup


def generate_categories():
    categories = db.get_categories()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []
    print(categories)
    btn1 = KeyboardButton(text=categories[0][0])
    markup.add(btn1)
    for item in categories[1:]:
        btn = KeyboardButton(text=item[0])
        buttons.append(btn)
    markup.add(*buttons)
    return markup







