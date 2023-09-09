from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from calendar_google.calendar_api import GoogleCalendar
from data.instrustions import google_calendar
from db_api.dal.user_dal import UserDAL
from loader import dp
from states.calendar import CalendarStates


@dp.message_handler(Command('calendar'),  chat_type=[types.ChatType.PRIVATE])
async def calendar_add(message: types.Message, state: FSMContext):
    await message.answer(
        google_calendar
    )
    await CalendarStates.waiting_key.set()


@dp.message_handler(state=CalendarStates.waiting_key, chat_type=[types.ChatType.PRIVATE])
async def calendar_add(message: types.Message, state: FSMContext):
    _key = message.text

    obj = GoogleCalendar()
    if obj.add_calendar(_key):
        await UserDAL.update(id=message.chat.id, calendar_id=_key)
        await message.answer('Ключ успешно добавлен')
    else:
        await message.answer('Произошла ошибка. Попробуйте снова')
    await state.reset_state()

