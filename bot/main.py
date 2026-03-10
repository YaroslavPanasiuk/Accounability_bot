# main.py
import asyncio
from aiogram import Bot, Dispatcher
from bot.config import config
from bot.lexicon import Lexicon
from datetime import datetime, timedelta
from bot.handlers import register_handlers
from bot.utils.spreadsheets import import_stats_from_sheet
from bot.utils.handle_json import get_stats_from_json
from bot.utils.schedulers import *
from bot.utils.formatters import format_daily_stats
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def main():
    await import_stats_from_sheet()
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    register_handlers(dp)
    scheduler = AsyncIOScheduler(timezone=config.TIMEZONE)
    scheduler.add_job(lambda: asyncio.create_task(send_daily_reminder(bot)), 'cron', hour=config.REMINDER_HOUR)
    scheduler.add_job(lambda: asyncio.create_task(send_stats_to_mentor(bot)), 'cron', hour=config.REMINDER_HOUR, minute=30)
    dp["scheduler"] = scheduler
    
    scheduler.start()

    print('bot started')
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())