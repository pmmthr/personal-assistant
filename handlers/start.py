import datetime

from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from db_api.dal.user_dal import UserDAL
from db_api.model import Users
from loader import dp


@dp.message_handler(CommandStart(), chat_type=[types.ChatType.PRIVATE])
async def bot_start(message: types.Message):
    await message.answer('Это бот помощник. Здесь ты можешь добавить встречу в календарь, либо подписать договора')

    # if not await UserDAL.get(id=message.chat.id):
    # await UserDAL.insert_or_update(index_elements=[Users.id],
    #                                id=message.chat.id)
    await UserDAL.add(id=message.chat.id)
