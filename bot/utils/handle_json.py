import json
from datetime import datetime, timedelta
from bot.config import Config

def get_column_names(file_path = "data.json") -> list:
    with open(file_path, 'r') as file:
        data = json.load(file)
        if isinstance(data, dict):
            return list(data["Коефіцієнти"].keys())
        else:
            raise ValueError("JSON file must contain a dictionary.")
        
def save_stats_to_json(stats: dict, date=datetime.now() - timedelta(hours=Config.TRESHOLD_HOURS), file_path = "data.json"):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    
    data[date.strftime("%d.%m.%Y")] = stats
    
    with open(file_path, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)