from data.loader import db
from parsing.parser import Parser
from pprint import pprint

# db.create_categories_table()
# db.create_products_table()
#db.create_users_table()
# db.create_locations()
# db.insert_locations()
# parser = Parser()
# data = parser.get_data()
# pprint(data)
#
#
# for category, products in data.items():
#     db.insert_into_categories(category)
#     category_id = db.get_category_id(category)
#     for product in products:
#         product_name = product['product_title']
#         product_price = product['product_price']
#         product_image_link = product['product_image_link']
#         product_link = product['product_link']
#         characteristics = product['characteristics']
#         db.insert_into_products(product_name=product_name,
#                                 price=product_price,
#                                 image=product_image_link,
#                                 link=product_link,
#                                 characteristics=characteristics,
#                                 category_id=category_id)