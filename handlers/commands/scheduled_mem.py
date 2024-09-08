from asyncio import sleep

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message
from mega import Mega
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from config_reader import config
from keyboards.for_pic_rate import get_rate_keyboard
from utils.mega_files import mega_func_2

FLAG = 0
CHAT_ID = int(config.ue_land_group.get_secret_value())
TIMER = 10 * 60

router = Router()


@router.message(F.text, Command("sched"))
async def cmd_sched(message: Message, session: AsyncSession, bot: Bot, mega: Mega):
    global FLAG
    if not FLAG:
        FLAG = 1
        while True:
            db_query = await session.execute(
                text("""SELECT * FROM images WHERE file_used=0 ORDER BY RANDOM() LIMIT 1;""")
            )
            image = db_query.fetchone()

            if not image:
                return await bot.send_message(chat_id=CHAT_ID, text='Все фото были просмотрены, поздравляю!')

            f_id = image[1]
            file_key = tuple(map(int, image[2].split(',')))
            bytes_photo = await (mega_func_2(f_id, file_key, mega))
            photo_id = await bot.send_photo(
                chat_id=CHAT_ID,
                photo=BufferedInputFile(bytes_photo, f"{image[3]}.jpg"),
                reply_markup=get_rate_keyboard(pic_id=image[1]),
            )
            file_tg_id = photo_id.photo[-1].file_id
            values = {
                'file_used': 1,
                'file_tg_id': file_tg_id,
                'id': image[0],
            }
            await session.execute(
                text(f"""UPDATE images SET file_used=:file_used, file_tg_id=:file_tg_id WHERE id=:id;"""),
                values
            )
            await session.commit()
            await sleep(TIMER)
