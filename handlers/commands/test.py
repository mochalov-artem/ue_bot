from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(F.text, Command("test"))
async def cmd_test(message: Message):
    await message.reply('test ok!')
