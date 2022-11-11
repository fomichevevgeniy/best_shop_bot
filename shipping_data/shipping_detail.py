from telebot.types import LabeledPrice, ShippingOption
from .shipping_product import Product

def generate_product_invoice(product_data):
    query = Product(
        title='Лучший телеграм бот магазин',
        description='\n'.join([product_name for product_name in product_data]),
        start_parameter='create_invoice_products',
        currency='UZS',
        prices=[LabeledPrice(
            label=f"{product_data[title]['quantity']} x {title}",
            amount=int(product_data[title]['quantity']) * int(product_data[title]['price'] * 100)
        ) for title in product_data],
        need_name=True,
        is_flexible=True
    )
    return query

EXPRESS_SHIPPING = ShippingOption(
    id='post_express',
    title='До 3х часов'
).add_price(LabeledPrice('До 3х часов', 25_000_00))


REGULAR_SHIPPING = ShippingOption(
    id='post_pickup',
    title='Самовывоз'
).add_price(LabeledPrice('Самовывоз', 0))

REGION_SHIPPING = ShippingOption(
    id='post_region',
    title='Доставка в регионы'
).add_price(LabeledPrice('Доставка в регионы', 250_000_00))

