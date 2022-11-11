from telebot import TeleBot, custom_filters
from .configs import TOKEN
from database.database import DataBase
from telebot.storage import StateMemoryStorage

bot = TeleBot(TOKEN, parse_mode='HTML',
              state_storage=StateMemoryStorage())

bot.add_custom_filter(custom_filters.StateFilter(bot))
db = DataBase()