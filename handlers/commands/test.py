from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(F.text, Command("test"))
async def answer_yes(message: Message):
    await message.reply('test ok!')
