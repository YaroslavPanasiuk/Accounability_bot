from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from datetime import datetime, timedelta
from bot.lexicon import Lexicon
from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=Lexicon.SEND_STATS_CMD)
    
    builder.adjust(1)
    
    return builder.as_markup(
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Select an action..."
    )

def get_inline_numeric_keyboard(prefix: str, start=0, end=5) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for i in range(start, end + 1):
        builder.button(text=str(i), callback_data=f"{prefix}:{i}")
    builder.adjust(2)
    return builder.as_markup()