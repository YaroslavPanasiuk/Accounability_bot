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

def get_stats_from_json(date: datetime, file_path = "data.json") -> dict:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get(date.strftime("%d.%m.%Y"), {})
    except FileNotFoundError:
        return {}
    
def get_all_stats_from_json(file_path = "data.json") -> dict:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return {k: v for k, v in data.items() if k != "Коефіцієнти"}
    except FileNotFoundError:
        return {}
    
def get_date_list():
    try:
        with open("data.json", 'r') as file:
            data = json.load(file)
            result = []
            for k in data.keys():
                if k == "Коефіцієнти":
                    continue
                if datetime.strptime(k, "%d.%m.%Y") > datetime.now():
                    break
                score = assess_day(datetime.strptime(k, "%d.%m.%Y"))
                result.append(f"{k} - {score}")
            return result
    except FileNotFoundError:
        return []
    
def assess_day(date: datetime) -> int:
    stats = get_stats_from_json(date)
    coefficients = get_coefficients_from_json()
    if not stats:
        return 0
    result = 0
    for key, value in stats.items():
        if key not in coefficients:
            continue
        if value is None or value == "":
            continue
        result += int(value) * int(coefficients[key])
    return result

def get_coefficients_from_json(file_path = "data.json") -> dict:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get("Коефіцієнти", {})
    except FileNotFoundError:
        return {}
    
def stats_exist_for_date(date, file_path = "data.json") -> bool:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        values = list(data.get(date.strftime("%d.%m.%Y"), {}).values())
        return len("".join(values)) > 7
        
    except FileNotFoundError:
        return False