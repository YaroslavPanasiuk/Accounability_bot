from bot.lexicon import Lexicon
import gspread
from bot.config import Config
from datetime import datetime, timedelta
import json


async def import_stats_from_sheet():
    try:
        gc = gspread.service_account_from_dict(Config.GOOGLE_CREDS)
        sh = gc.open_by_url(Config.GOOGLE_SHEET_URL)
        worksheet = sh.worksheet(Lexicon.WORKSHEET_NAME)
        values = worksheet.get_all_values()
        headers = values[0][1:19]
        data = {"Коефіцієнти": dict(zip(headers, values[1][23:]))}
        for row in values[1:]:
            if not row[0]:
                continue
            data[row[0]] = dict(zip(headers, row[1:19]))
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Import failed: {e}")


def get_row_from_date(date: datetime) -> int:
    try:
        gc = gspread.service_account_from_dict(config.GOOGLE_CREDS)
        sh = gc.open_by_url(config.GOOGLE_SHEET_URL)
        worksheet = sh.worksheet(Lexicon.WORKSHEET_NAME)
        values = worksheet.get_all_values()
        for i, row in enumerate(values[1:], start=2):
            if row[0] == date.strftime("%d.%m.%Y"):
                return i
        return -1
    except Exception as e:
        print(f"Error fetching row: {e}")
        return -1


async def export_stats_to_sheet(stats: dict, date=datetime.now() - timedelta(hours=Config.TRESHOLD_HOURS)):
    try:
        gc = gspread.service_account_from_dict(Config.GOOGLE_CREDS)
        sh = gc.open_by_url(Config.GOOGLE_SHEET_URL)
        worksheet = sh.worksheet(Lexicon.WORKSHEET_NAME)
        headers = worksheet.row_values(1)[1:19]
        data = worksheet.get_all_values()
        current_row = get_row_from_date(date)
        if current_row == -1:
            range = f"B{worksheet.row_count + 1}:S{worksheet.row_count + 1}"
        else:
            range = f"B{current_row}:S{current_row}"
        row_data = [stats.get(header, "") for header in headers]
        worksheet.batch_update([{
            'range': range,
            'values': [row_data]
        }], value_input_option='USER_ENTERED')
    except Exception as e:
        print(f"Export failed: {e}")

    