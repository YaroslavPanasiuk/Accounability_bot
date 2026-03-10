import gspread
import random
import re
from aiogram import types
from aiogram.filters import Filter
from bot.config import config

class Lexicon:
    WORKSHEET_NAME = "Підзвітність"
    SEND_STATS_CMD = "Оцінити день"
    SEND_PREVIOUS_STATS_CMD = "Оцінити попередній день"
    SHOW_PREVIOUS_STATS_CMD = "Показати статистику за попередні дні"
    START_STAT_COLLECTION = "Оцнимо {0}"
    DAILY_REMINDER = "Привіт! Час оцінити свій день. Натисни кнопку нижче, щоб почати."
    STATS_MAIN_QUESTION = "Оціни показник '{0}'"
    STATS_COLLECTED = "Дякую, твої дані збережено!"
    DEFAULT_MESSAGE = "👨🏼‍❤️‍👨🏻"
    MENTOR_START_MESSAGE = "Привіт, наставнику! Я сповіщатиму тебе про статистику учня щоразу, коли він її заповнюватиме. Або повідомлятиму тебе, якщо він забув заповнити її до кінця дня. 👨🏼‍❤️‍👨🏻"
    SHOW_STATS_CMD = "Показати статистику учня за сьогодні"
    DISCIPLE_HASNT_FILLED_STATS = "Учень не заповнив статистику за сьогоднішній день. Можеш перепитати його про це"
    NO_STATS_AVAILABLE = "Немає доступної статистики для перегляду."
    SELECT_PREVIOUS_DAY = "Оберіть день:"

class LexiconFilter(Filter):
    def __init__(self, key: str):
        self.key = key

    async def __call__(self, message: types.Message) -> bool:
        expected_text = getattr(Lexicon, self.key, None)
        return message.text == expected_text
    

