from datetime import datetime
from bot.utils.handle_json import get_column_names, assess_day
from bot.lexicon import Lexicon
from bot.config import config
from babel.dates import format_datetime
import xml.etree.ElementTree as ET
import random
from bot.res.Bible_books_dict import BIBLE_BOOKS_UA

def random_bible_verse():
    tree = ET.parse("bot/res/Bible.xml")
    root = tree.getroot()
    
    all_data = []

    for testament in root.findall('testament'):
        t_name = testament.get('name')
        
        for book in testament.findall('book'):
            b_num = book.get('number')
            b_name = BIBLE_BOOKS_UA.get(b_num, f"Книга {b_num}")
            
            for chapter in book.findall('chapter'):
                c_num = chapter.get('number')
                
                for verse in chapter.findall('verse'):
                    v_num = verse.get('number')
                    v_text = verse.text
                    
                    all_data.append({
                        "testament": t_name,
                        "book": b_name,
                        "chapter": c_num,
                        "verse": v_num,
                        "text": v_text
                    })

    # Pick a random entry
    selection = random.choice(all_data)
    
    return (
        f"📖 {selection['text']}\n"
        f"📍 {selection['book']} {selection['chapter']}:{selection['verse']}\n"
        "👨🏼‍❤️‍👨🏻"
    )

def format_daily_stats(date: datetime, stats: dict) -> str:
    if not stats:
        return Lexicon.NO_STATS_MESSAGE
    smile_map = {
        "5": "😇",
        "4": "😁",
        "3": "🙂",
        "2": "🙃",
        "1": "🫠",
        "0": "😭"
    }
    formatted = f"📊 Статистика учня за {format_datetime(date, format='d MMMM', locale='uk') }:\n\n"
    for key, value in stats.items():
        if key not in get_column_names():
            continue
        row = f"`{(key[:23] + '…:') if len(key) > 25 else f"{key}: ".ljust(25, ".")} {value}`"
        value = "➖" if value is None or value == "" else value
        formatted += f"• {row} {smile_map.get(value, '')}\n"
    formatted += f"\nЗагальна оцінка дня: {assess_day(date)}"
    
    return formatted