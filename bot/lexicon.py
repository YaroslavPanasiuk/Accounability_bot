import gspread
import random
import re
from aiogram import types
from aiogram.filters import Filter
from bot.config import config

class Lexicon:
    WORKSHEET_NAME = "Підзвітність"
    SEND_STATS_CMD = "Оцінити день"
    START_STAT_COLLECTION = "Оцнимо {0}"
    DAILY_REMINDER = "Привіт! Час оцінити свій день. Натисни кнопку нижче, щоб почати."
    STATS_MAIN_QUESTION = "Оціни показник '{0}'"
    STATS_COLLECTED = "Дякую, твої дані збережено!"
    DEFAULT_MESSAGE = "👨🏼‍❤️‍👨🏻"

class LexiconFilter(Filter):
    def __init__(self, key: str):
        self.key = key

    async def __call__(self, message: types.Message) -> bool:
        expected_text = getattr(Lexicon, self.key, None)
        return message.text == expected_text
    

