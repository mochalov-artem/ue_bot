from mega import Mega

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from utils.send_pic import send_pic_raw


router = Router()


@router.message(F.text, Command("mem"), flags={'long_operation': 'uploading_image'})
async def cmd_mem(message: Message, session: AsyncSession, bot: Bot, mega: Mega):
    try:
        await send_pic_raw(message, session, bot, mega)
    except Exception as e:
        print(e)
        await message.answer(text="АШЫПКА хехеее))")
