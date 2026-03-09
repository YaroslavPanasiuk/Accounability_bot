import asyncio
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from bot.db import database
from bot.lexicon import select_random_line
from bot.utils.keyboards import get_main_menu_keyboard
from bot.utils.spreadsheets import fetch_users_with_no_stats
from datetime import datetime
from bot.config import Config
from bot.lexicon import Lexicon

async def send_daily_reminder(bot: Bot):
    try:
        await bot.send_message(
            Config.ADMIN_ID,
            Lexicon.DAILY_REMINDER, 
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Failed to send to {Config.ADMIN_ID}: {e}")