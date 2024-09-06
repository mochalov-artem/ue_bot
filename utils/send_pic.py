from aiogram import Bot
from aiogram.types import Message, BufferedInputFile
from aiogram.utils.chat_action import ChatActionSender
from mega import Mega
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from config_reader import config

from keyboards.for_pic_rate import get_rate_keyboard
from orm.database import Images
from utils.mega_files import mega_func_2


async def send_pic_orm(message: Message, session: AsyncSession, bot: Bot, mega: Mega):
    async with ChatActionSender(bot=bot, chat_id=message.from_user.id, action="upload_photo"):
        if message.chat.id == int(config.ue_land_group.get_secret_value()):
            db_query = await session.execute(select(Images).where(Images.file_used == 0).order_by(func.random()))
            image: Images = db_query.scalar()

            if not image:
                return await message.reply(text='Все фото были просмотрены, поздравляю!')

            file_key = tuple(map(int, image.file_key.split(',')))

            bytes_photo = await (mega_func_2(image.file_id, file_key, mega))
            photo_id = await message.answer_photo(
                photo=BufferedInputFile(bytes_photo, f"{image.file_name}.jpg"),
                reply_markup=get_rate_keyboard(pic_id=image.file_id),
            )
            file_tg_id = photo_id.photo[-1].file_id

            image.file_used = 1
            image.file_tg_id = file_tg_id
            await session.commit()


async def send_pic_raw(message: Message, session: AsyncSession, bot: Bot, mega: Mega):
    async with ChatActionSender(bot=bot, chat_id=message.from_user.id, action="upload_photo"):
        if message.chat.id == int(config.ue_land_group.get_secret_value()):
            async with ChatActionSender(bot=bot, chat_id=message.from_user.id, action="upload_photo"):

                db_query = await session.execute(
                    text("""SELECT * FROM images WHERE file_used=0 ORDER BY RANDOM() LIMIT 1;""")
                )
                image = db_query.fetchone()

                if not image:
                    return await message.answer(text='Все фото были просмотрены, поздравляю!')

                f_id = image[1]
                file_key = tuple(map(int, image[2].split(',')))
                bytes_photo = await (mega_func_2(f_id, file_key, mega))
                photo_id = await message.answer_photo(
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
