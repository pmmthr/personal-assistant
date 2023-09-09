from aiogram.dispatcher.filters.state import StatesGroup, State


class CalendarStates(StatesGroup):
    waiting_key = State()