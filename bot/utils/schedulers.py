import asyncio
from aiogram import Bot
from bot.utils.keyboards import get_main_menu_keyboard
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