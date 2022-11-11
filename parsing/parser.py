import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.url = 'https://elmakon.uz/tehnika-dlya-kuhni/holodilniki/'
        self.host = 'https://elmakon.uz'

    def get_html(self, url):
        html = requests.get(url).text
        return html

    def get_soup(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def get_data(self):
        soup = self.get_soup(self.get_html(self.url))
        categories = soup.find_all('li', class_='ut2-item')
        data = {}
        for category in categories:
            title = category.find('span').get_text(strip=True)
            data[title] = []
            category_link = category.find('a').get('href')

            category_page = self.get_html(category_link)
            category_soup = self.get_soup(category_page)
            products = category_soup.find_all('div', class_='ty-column4')

            for product in products:
                try:
                    product_title = product.find('a', class_='product-title').get_text(strip=True)
                    product_link = product.find('a', class_='product-title').get('href')
                    product_price = int(
                        product.find('span', {'class': 'ty-price-num'}).get_text(strip=True).replace('.', ''))
                    product_image_link = product.find('img').get('src')
                    product_page = self.get_html(product_link)
                    product_soup = self.get_soup(product_page)
                    characteristics = product_soup.find('div', class_='ty-product-feature-group')
                    text = 'Общие характеристики\n'
                    char_blocks = characteristics.find_all('div', class_='ty-product-feature')
                    for block in char_blocks:
                        text += f'{block.find("div", class_="ty-product-feature__label").get_text(strip=True)}: {block.find("div", class_="ty-product-feature__value").get_text(strip=True)}\n'

                    data[title].append({
                        'product_title': product_title,
                        'product_price': product_price,
                        'product_image_link': product_image_link,
                        'product_link': product_link,
                        'characteristics': text
                    })


                except:
                    continue

        return data



