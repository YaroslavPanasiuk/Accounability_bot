import asyncio
from aiogram import Bot
from bot.utils.keyboards import get_disciple_main_menu_keyboard, get_mentor_main_menu_keyboard
from datetime import datetime
from bot.config import Config
from bot.lexicon import Lexicon
from bot.utils.spreadsheets import import_stats_from_sheet
from bot.utils.handle_json import get_stats_from_json, stats_exist_for_date
from bot.utils.formatters import format_daily_stats

async def send_daily_reminder(bot: Bot):
    await import_stats_from_sheet()
    if stats_exist_for_date(datetime.now()):
        return
    try:
        await bot.send_message(
            Config.DISCIPLE_ID,
            Lexicon.DAILY_REMINDER, 
            reply_markup=get_disciple_main_menu_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Failed to send to {Config.ADMIN_ID}: {e}")

async def send_stats_to_mentor(bot: Bot):
    await import_stats_from_sheet()
    try:
        if not stats_exist_for_date(datetime.now()):
            await bot.send_message(
                Config.MENTOR_ID,
                Lexicon.DISCIPLE_HASNT_FILLED_STATS, 
                reply_markup=get_mentor_main_menu_keyboard(),
                parse_mode="HTML"
            )
            return
        await bot.send_message(
            Config.MENTOR_ID,
            format_daily_stats(datetime.now(), get_stats_from_json()), 
            reply_markup=get_mentor_main_menu_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Failed to send to {Config.ADMIN_ID}: {e}")