from dataclasses import dataclass
from typing import List
from telebot.types import LabeledPrice

@dataclass
class Product:
    title: str
    description: str
    start_parameter: str
    currency: str
    prices: List[LabeledPrice]
    provider_token: str = '398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065'
    provider_data: dict = None
    need_name: bool = False
    is_flexible: bool = True

    def generate_invoice(self):
        return self.__dict__