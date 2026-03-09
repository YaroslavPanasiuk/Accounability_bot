import os
import json
from dotenv import load_dotenv

load_dotenv()

class Config:
    ADMIN_ID = int(os.getenv("ADMIN_ID"))
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    GOOGLE_SHEET_URL = os.getenv("GOOGLE_SHEET_URL")
    GOOGLE_CREDS = json.loads(os.getenv("GOOGLE_CREDS_JSON", "{}"))
    LOCALE = "uk"
    TRESHOLD_HOURS = 6
    TIMEZONE = os.getenv("TZ")
    REMINDER_HOUR = 23
    
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not found in .env file")

config = Config()