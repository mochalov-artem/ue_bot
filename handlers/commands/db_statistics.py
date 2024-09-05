from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiosqlite import Connection

from utils.progressbar import progressbar

router = Router()


@router.message(F.text, Command("stats"))
async def progress_bar(message: Message, async_con: Connection):
    cursor = await async_con.execute("SELECT COUNT(DISTINCT(pic_id)) FROM pic_user_rate")
    res = await cursor.fetchone()
    print(res)
    current = res[0]
    await message.answer(text=progressbar(current, total=85_015, bar_length=15))
