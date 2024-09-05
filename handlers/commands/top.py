from sqlite3 import Connection

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(F.text, Command("top"))
async def top_rates_list(message: Message, con: Connection):
    cur = con.cursor()
    cur.execute("""
    SELECT  A.user_id, A.votes, users.username
    FROM users
    LEFT JOIN (SELECT user_id, COUNT(user_id) as votes FROM pic_user_rate GROUP BY user_id ORDER BY votes DESC) A ON A.user_id = users.tg_id
    ORDER BY votes DESC
    """)

    res = cur.fetchall()
    text = [f'{i[2].ljust(25)} {i[1]}' for i in res]
    result_text = '\n'.join(text)
    await message.answer(text='🏆 TOP пользователей 🏆\n'+f'{result_text}')



