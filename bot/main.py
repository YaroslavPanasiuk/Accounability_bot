# main.py
import asyncio
from aiogram import Bot, Dispatcher
from bot.config import config
from bot.lexicon import Lexicon
from bot.handlers import register_handlers
from bot.utils.spreadsheets import import_stats_from_sheet
from bot.utils.handle_json import get_column_names
from bot.utils.schedulers import send_daily_reminder
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def main():
    await import_stats_from_sheet()
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    register_handlers(dp)
    scheduler = AsyncIOScheduler(timezone=config.TIMEZONE)
    scheduler.add_job(lambda: asyncio.create_task(send_daily_reminder(bot)), 'cron', hour=config.REMINDER_HOUR)
    dp["scheduler"] = scheduler
    
    scheduler.start()

    print('bot started')
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())