from aiogram import Router, F, types, Bot
from aiogram.types import BufferedInputFile
from aiogram.utils.chat_action import ChatActionSender
from mega import Mega
from sqlalchemy import text

from config_reader import config
from keyboards.for_pic_rate import get_rate_keyboard
from utils.mega_files import mega_func_2


router = Router()


@router.callback_query(F.data == "Yes", flags={'long_operation': 'uploading_image'})
async def cb_wannamem_yes(callback: types.CallbackQuery, session, bot: Bot, mega: Mega):
    try:
        if callback.message.chat.id == int(config.ue_land_group.get_secret_value()):
            async with ChatActionSender(bot=bot, chat_id=callback.message.from_user.id, action="upload_photo"):

                db_query = await session.execute(
                    text("""SELECT * FROM images WHERE file_used=0 ORDER BY RANDOM() LIMIT 1;""")
                )
                image = db_query.fetchone()

                if not image:
                    return await bot.send_message(chat_id=callback.message.chat.id,
                                                  text='Все фото были просмотрены, поздравляю!')

                f_id = image[1]
                file_key = tuple(map(int, image[2].split(',')))
                bytes_photo = await (mega_func_2(f_id, file_key, mega))
                photo_id = await callback.message.answer_photo(
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
    except Exception as e:
        print(e)
        await bot.send_message(chat_id=callback.message.chat.id, text="АШЫПКА хехеее))")
