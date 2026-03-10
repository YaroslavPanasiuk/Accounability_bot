from bot.config import Config
from aiogram import Router, types
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime, timedelta
from babel.dates import format_date
from aiogram import F
from bot.filters.by_id import IsDisciple
from bot.utils.keyboards import *
from bot.lexicon import Lexicon, LexiconFilter
from bot.config import Config
from bot.utils.handle_json import *
from bot.utils.spreadsheets import export_stats_to_sheet

class StatisticsCollection(StatesGroup):
    waiting_for_answer = State()

router = Router()
router.message.filter(IsDisciple())

@router.message(or_f(Command("fill_stats"),LexiconFilter("SEND_STATS_CMD")))
async def cmd_fill_stats(message: types.Message, state: FSMContext):
    now = datetime.now() - timedelta(hours=Config.TRESHOLD_HOURS)
    await message.answer(Lexicon.START_STAT_COLLECTION.format(format_date(now, format="d MMMM", locale=Config.LOCALE)))
    await message.answer(
        f"{Lexicon.STATS_MAIN_QUESTION.format(get_column_names()[0])}",
        reply_markup=get_inline_numeric_keyboard("question_1")
    )
    await state.set_state(StatisticsCollection.waiting_for_answer)

def get_next_question_index(user_data: dict) -> int:
    answers = [k for k in user_data.keys() if k in get_column_names()]
    return len(answers) + 1

@router.callback_query(StatisticsCollection.waiting_for_answer, F.data.startswith("question_"))
async def process_any_answer(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_index = get_next_question_index(data)

    await state.update_data({get_column_names()[current_index - 1]: callback.data.split(":")[1]})
    await ask_next_question_or_finish(callback.message, state)

async def ask_next_question_or_finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    next_index = get_next_question_index(data)
    
    if next_index > 13:
        await finalize_and_save_stats(message, state)
    else:
        question = get_column_names()[next_index-1]
        
        await message.edit_text(Lexicon.STATS_MAIN_QUESTION.format(question), reply_markup=get_inline_numeric_keyboard(f"question_{next_index}"))
        await state.set_state(StatisticsCollection.waiting_for_answer)

async def finalize_and_save_stats(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    
    stats_dict = {k: v for k, v in user_data.items() if k != "selected_week" and k != "selected_day"}
    save_stats_to_json(stats_dict)
    await export_stats_to_sheet(stats_dict, date=user_data.get("selected_day"))
    await message.edit_text(Lexicon.STATS_COLLECTED)
    await message.answer(Lexicon.DEFAULT_MESSAGE, reply_markup=get_disciple_main_menu_keyboard())
    await state.clear()

@router.message(or_f(Command("fill_old_stats"),LexiconFilter("SEND_PREVIOUS_STATS_CMD")))
async def cmd_fill_previous_stats(message: types.Message):
    dates = get_date_list()
    dates.reverse()
    if not dates:
        await message.answer(Lexicon.NO_STATS_AVAILABLE)
        return
    keyboard = get_previous_days_keyboard(dates)
    
    await message.answer(Lexicon.SELECT_PREVIOUS_DAY, reply_markup=keyboard)

@router.callback_query(F.data.startswith("page_"))
async def set_page(callback: types.CallbackQuery):
    dates = get_date_list()
    dates.reverse()
    data = callback.data 
    new_page = int(data.split("_")[1])
    new_kb = get_previous_days_keyboard(dates, page=new_page)
    await callback.message.edit_text(callback.message.text, reply_markup=new_kb)
    await callback.answer()

@router.callback_query(F.data.startswith("item_"))
async def fill_stats_for_selected_day(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data 
    date = datetime.strptime(data.split("_")[1].split(" - ")[0], "%d.%m.%Y")
    await callback.message.edit_text(Lexicon.START_STAT_COLLECTION.format(format_date(date, format="d MMMM", locale=Config.LOCALE)))
    await callback.message.answer(
        f"{Lexicon.STATS_MAIN_QUESTION.format(get_column_names()[0])}",
        reply_markup=get_inline_numeric_keyboard("question_1")
    )
    await state.update_data({"selected_day": date})
    await state.set_state(StatisticsCollection.waiting_for_answer)
    await callback.answer()
