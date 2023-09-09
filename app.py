import asyncio
import os

from aiogram import executor, Dispatcher
from aiohttp import web
import handlers
from calendar_google.calendar_api import GoogleCalendar
# from calendar_google.calendar_api import GoogleCalendar
from db_api.postgresql import db
from loader import dp
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    # obj = GoogleCalendar()
    # print(obj.get_calendar_list())
    # print(obj.add_calendar('ivanluki78@gmail.com'))
    # event = {
    #     'summary': '111',
    #     'location': 'санкт-петербург',
    #     'description': '222',
    #     'start': {
    #         'date': '2023-09-09',
    #     },
    #     'end': {
    #         'date': '2023-09-10',
    #     },
    # }
    # print(obj.add_event('ivanluki78@gmail.com', event))
    await db.drop_all()
    await db.create_all()
    await on_startup_notify(dispatcher)

async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
