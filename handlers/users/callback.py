from telebot.types import CallbackQuery, InputFile
from data.loader import bot
from keyboards.reply import *
from keyboards.inline import *
import requests
from states.states import CartStates
from shipping_data.shipping_detail import generate_product_invoice, REGION_SHIPPING, REGULAR_SHIPPING, EXPRESS_SHIPPING

@bot.callback_query_handler(lambda call: call.data == 'back_categories')
def reaction_to_back_categories(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.id
    bot.delete_message(chat_id, message_id)
    bot.send_message(chat_id, 'Выберите категорию: ', reply_markup=generate_categories())


@bot.callback_query_handler(lambda call: call.data == 'main_menu')
def reaction_to_main_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.id
    bot.delete_message(chat_id, message_id)
    bot.send_message(chat_id, 'Что хотите сделать?', reply_markup=generate_main_menu())


@bot.callback_query_handler(lambda call: call.data == 'next')
def reaction_to_next(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.id
    keyboards_list = call.message.reply_markup.keyboard[-2]
    print(keyboards_list)
    bot.delete_message(chat_id, message_id)
    for button in keyboards_list:
        if 'page' in button.callback_data:
            page = int(button.text)
            page += 1
            category_name = button.callback_data.split('_')[1]  # page_Samsung -> ['page', 'Samsung']
            bot.send_message(chat_id, category_name,
                             reply_markup=generate_products_pagination(category_name, page))


@bot.callback_query_handler(lambda call: call.data == 'prev')
def reaction_to_prev(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.id
    keyboards_list = call.message.reply_markup.keyboard[-2]
    print(keyboards_list)
    bot.delete_message(chat_id, message_id)
    for button in keyboards_list:
        if 'page' in button.callback_data:
            page = int(button.text)
            page -= 1
            category_name = button.callback_data.split('_')[1]  # page_Samsung -> ['page', 'Samsung']
            bot.send_message(chat_id, category_name,
                             reply_markup=generate_products_pagination(category_name, page))


@bot.callback_query_handler(lambda call: 'page' in call.data)
def reaction_to_page(call: CallbackQuery):
    keyboards_list = call.message.reply_markup.keyboard[-2]
    for button in keyboards_list:
        if 'page' in button.callback_data:
            page = button.text
            bot.answer_callback_query(call.id, f'Вы на странице {page}')


@bot.callback_query_handler(lambda call: 'product' in call.data)
def reaction_to_product(call: CallbackQuery):
    # product_1
    _, product_id = call.data.split('_')
    product_id = int(product_id)
    product = db.get_detail_product(product_id)
    product_name = product[1]
    product_price = product[2]
    product_photo = product[3]
    product_link = product[4]
    product_desc = product[5]
    category_id = product[6]
    print(product_photo)
    chat_id = call.message.chat.id
    message_id = call.message.id
    bot.delete_message(chat_id, message_id)
    caption = f'''Товар: {product_name}

Цена: {product_price} сум

Описание: {product_desc}

Подробнее: {product_link}
'''
    image = requests.get(product_photo).content  # Костыль
    # file = InputFile(product_photo)
    bot.send_photo(chat_id, photo=image, caption=caption,
                   reply_markup=generate_product_detail(category_id, product_id))


@bot.callback_query_handler(lambda call: call.data == 'plus')
def reaction_to_plus(call: CallbackQuery):
    chat_id = call.message.chat.id
    buttons = call.message.reply_markup.keyboard
    quantity = int(buttons[0][1].text)
    product_id = buttons[1][0].callback_data.split('_')[1]
    category_id = buttons[2][0].callback_data.split('_')[2]
    if quantity < 20:
        quantity += 1
        bot.edit_message_reply_markup(chat_id, call.message.id,
            reply_markup=generate_product_detail(category_id, product_id, quantity))
    else:
        bot.answer_callback_query(call.id, 'Вы не можете купить более 20 товаров')


@bot.callback_query_handler(lambda call: call.data == 'minus')
def reaction_to_minus(call: CallbackQuery):
    chat_id = call.message.chat.id
    buttons = call.message.reply_markup.keyboard
    quantity = int(buttons[0][1].text)
    product_id = buttons[1][0].callback_data.split('_')[1]
    category_id = buttons[2][0].callback_data.split('_')[2]
    if quantity > 1:
        quantity -= 1
        bot.edit_message_reply_markup(chat_id, call.message.id,
            reply_markup=generate_product_detail(category_id, product_id, quantity))
    else:
        bot.answer_callback_query(call.id, 'Нельзя купить менее 1 товара')


@bot.callback_query_handler(lambda call: call.data == 'quantity')
def reaction_to_quantity(call: CallbackQuery):
    buttons = call.message.reply_markup.keyboard
    quantity = int(buttons[0][1].text)
    bot.answer_callback_query(call.id, f'Выбранное количество: {quantity} шт')


@bot.callback_query_handler(lambda call: call.data.startswith('back_category_'))
def reaction_to_back_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    category_id = call.data.split('_')[2]
    category_name = db.get_category_name_by_id(category_id)
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, f'Категория: {category_name}',
                     reply_markup=generate_products_pagination(category_name))



@bot.callback_query_handler(lambda call: call.data.startswith('cart'))
def reaction_to_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    # cart_4
    product_id = int(call.data.split('_')[1])
    # cart_4 ->  ['cart', '4'] -> '4' -> 4
    product = db.get_detail_product(product_id)
    product_name = product[1]
    product_price = product[2]
    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    bot.set_state(user_id, CartStates.cart, chat_id)
    with bot.retrieve_data(user_id, chat_id) as data:
        if data.get('cart'):
            data['cart'][product_name] = {
                'quantity': quantity,
                'price': product_price,
                'product_id': product_id
            }
        else:
            data['cart'] = {
                product_name: {
                    'quantity': quantity,
                    'price': product_price,
                    'product_id': product_id
                }
            }
    bot.answer_callback_query(call.id, 'Товар успешно добавлен в корзину')


def get_text_reply_markup(data):
    text = 'Товары в вашей корзине:\n'
    total_price = 0
    for product_name, item in data['cart'].items():
        quantity = item['quantity']
        price = item['price']
        total_price += price * quantity
        text += f'{product_name} - {price} ✖ {quantity} = {price * quantity} сум\n'

    if total_price == 0:
        text = 'Ваша корзина пустая, но это никогда не поздно исправить :)'
        markup = generate_main_menu()
    else:
        text += f'Общая стоимость: {total_price}\n'
        markup = generate_cart_buttons(data['cart'])

    return {
        'markup': markup,
        'text': text,
        'total_price': total_price
    }


@bot.callback_query_handler(lambda call: call.data == 'show_cart')
def reaction_to_show_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.id)
    try:
        with bot.retrieve_data(user_id, chat_id) as data:
            result = get_text_reply_markup(data)
        text = result['text']
        markup = result['markup']
        bot.send_message(chat_id, text, reply_markup=markup)
    except:
        bot.send_message(chat_id, 'Ваша корзина пустая', reply_markup=generate_main_menu())



@bot.callback_query_handler(lambda call: 'remove' in call.data)
def reaction_to_remove(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    # remove_1
    product_id = int(call.data.split('_')[1])
    with bot.retrieve_data(user_id, chat_id) as data:
        keys = [key for key in data['cart'].keys()]
        for product_name in keys:
            if data['cart'][product_name]['product_id'] == product_id:
                del data['cart'][product_name]
    result = get_text_reply_markup(data)
    text = result['text']
    markup = result['markup']
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, text, reply_markup=markup)


@bot.callback_query_handler(lambda call: call.data == 'clear_cart')
def reaction_to_clear_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    bot.delete_state(user_id, chat_id)
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, 'Ваша корзина очищена')
    bot.send_message(chat_id, 'Что желаете сделать?', reply_markup=generate_main_menu())


@bot.callback_query_handler(lambda call: call.data == 'submit_order')
def reaction_to_submit_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        bot.send_invoice(chat_id, **generate_product_invoice(data['cart']).generate_invoice(),
                         invoice_payload='shop_bot')
    bot.delete_state(user_id, chat_id)



@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    bot.answer_shipping_query(shipping_query.id,
                              ok=True,
                              shipping_options=[REGION_SHIPPING, REGULAR_SHIPPING, EXPRESS_SHIPPING],
                              error_message='Простите, что-то не работает')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id,
                                  ok=True,
                                  error_message='Опять что-то пошло не так')


@bot.message_handler(content_types=['successful_payment'])
def get_payment(message):
    bot.send_message(message.chat.id, 'Ура. Оплата прошла успешно. Мы вас кинули')
















