from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.for_mem import get_mem_keyboard


router = Router()


@router.message(F.text, Command("wannamem"))
async def cmd_wannamem(message: Message):
    try:
        await message.answer("Оцените мем?", reply_markup=get_mem_keyboard())
    except Exception as e:
        await message.answer(text="АШЫПКА хехеее))")
