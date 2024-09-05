from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

router = Router()


@router.message(F.text, Command("top"))
async def cmd_top_rates_list(message: Message, session: AsyncSession):
    cursor = await session.execute(text('''
    SELECT  A.user_id, A.votes, users.username
    FROM users
    LEFT JOIN (SELECT user_id, COUNT(user_id) as votes FROM pic_user_rate 
    GROUP BY user_id ORDER BY votes DESC) A ON A.user_id = users.tg_id
    ORDER BY votes DESC
    '''))

    res = cursor.fetchall()
    rtext = [f'{i[2].ljust(25)} {i[1]}' for i in res]
    result_text = '\n'.join(rtext)
    await message.answer(text='🏆 TOP пользователей 🏆\n'+f'{result_text}')



