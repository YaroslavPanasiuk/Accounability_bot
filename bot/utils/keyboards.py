from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from datetime import datetime, timedelta
from bot.config import Config
from bot.lexicon import Lexicon
from babel.dates import format_datetime
from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup

def get_disciple_main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=Lexicon.SEND_STATS_CMD)
    builder.button(text=Lexicon.SEND_PREVIOUS_STATS_CMD)
    
    builder.adjust(1)
    
    return builder.as_markup(
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Select an action..."
    )

def get_mentor_main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=Lexicon.SHOW_STATS_CMD)
    builder.button(text=Lexicon.SHOW_PREVIOUS_STATS_CMD)
    
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

def get_previous_days_keyboard(items, page=0, page_size=7):
    start = page * page_size
    end = start + page_size
    current_items = items[start:end]
    
    keyboard = []
    for item in current_items:
        keyboard.append([InlineKeyboardButton(text=item, callback_data=f"item_{item}")])
    
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton(text="⏮️", callback_data=f"page_0"))
        nav_row.append(InlineKeyboardButton(text="⏪", callback_data=f"page_{page-1}"))
    
    if end < len(items):
        nav_row.append(InlineKeyboardButton(text="⏩", callback_data=f"page_{page+1}"))
        last_page = len(items)//page_size - (0 if len(items)%page_size > 0 else 1)
        nav_row.append(InlineKeyboardButton(text="⏭️", callback_data=f"page_{last_page}"))
    
    if nav_row:
        keyboard.append(nav_row)
        
    return InlineKeyboardMarkup(inline_keyboard=keyboard)