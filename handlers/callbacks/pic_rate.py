from aiogram import types, Router
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.pic_rate_callback_factory import PicRateCallbackFactory

router = Router()

rates_to_chars = {
    5: 'S',
    4: 'A',
    3: 'B',
    2: 'C',
    1: 'TRASH',
}


@router.callback_query(PicRateCallbackFactory.filter())
async def cb_pic_rate(callback: types.CallbackQuery, callback_data: PicRateCallbackFactory, session: AsyncSession):
    user_id = callback.from_user.id
    pic_id = callback_data.pic_id

    if callback_data.rate == 0:
        db_query = await session.execute(
            text(
                """SELECT pic_id, user_id, rate, users.username
                FROM (SELECT * FROM pic_user_rate WHERE pic_id=:pic_id) A
                LEFT JOIN users ON A.user_id = users.tg_id
                """),
            {"pic_id": pic_id}
        )
        print(db_query)
        res = db_query.fetchall()
        print(res)
        if res:
            result_text = '\n'.join([f'{el[3]} {rates_to_chars[el[2]]}' for el in res])
        else:
            result_text = 'Никто не оценил мем'
        await callback.message.reply(text=result_text)
        return

    rate = await session.execute(
        text(
            """SELECT * FROM pic_user_rate WHERE pic_id=:pic_id AND user_id=:user_id;"""
        ),
        {"pic_id": pic_id, "user_id": user_id}
    )
    user_mark = rate.fetchone()

    if not user_mark:
        await session.execute(
            text(
                """INSERT INTO pic_user_rate(pic_id,user_id,rate) VALUES(:pic_id,:user_id,:rate);"""
            ),
            {"pic_id": pic_id, "user_id": user_id, "rate": callback_data.rate}
        )
        await session.commit()
        new_markup = callback.message.reply_markup
        match callback_data.rate:
            case 5:
                button_text = new_markup.inline_keyboard[0][0].text
                new_markup.inline_keyboard[0][0].text = button_text[:-1] + str(int(button_text[-1]) + 1)
                await callback.message.edit_reply_markup(reply_markup=new_markup)
            case 4:
                button_text = new_markup.inline_keyboard[0][1].text
                new_markup.inline_keyboard[0][1].text = button_text[:-1] + str(int(button_text[-1]) + 1)
                await callback.message.edit_reply_markup(reply_markup=new_markup)
            case 3:
                button_text = new_markup.inline_keyboard[0][2].text
                new_markup.inline_keyboard[0][2].text = button_text[:-1] + str(int(button_text[-1]) + 1)
                await callback.message.edit_reply_markup(reply_markup=new_markup)
            case 2:
                button_text = new_markup.inline_keyboard[0][3].text
                new_markup.inline_keyboard[0][3].text = button_text[:-1] + str(int(button_text[-1]) + 1)
                await callback.message.edit_reply_markup(reply_markup=new_markup)
            case _:
                button_text = new_markup.inline_keyboard[1][1].text
                new_markup.inline_keyboard[1][1].text = button_text[:-1] + str(int(button_text[-1]) + 1)
                await callback.message.edit_reply_markup(reply_markup=new_markup)
    else:
        await callback.answer(
            text=f"Вы уже оценили фото на {rates_to_chars[user_mark[3]]}",
            show_alert=True,
        )
    await callback.answer()
