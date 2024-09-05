from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.pic_rate_callback_factory import PicRateCallbackFactory


def get_rate_keyboard(pic_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='💎S0', callback_data=PicRateCallbackFactory(pic_id=f"{pic_id}", rate=5)
    )
    builder.button(
        text='🤣A0', callback_data=PicRateCallbackFactory(pic_id=f"{pic_id}", rate=4)
    )
    builder.button(
        text='🙂B0', callback_data=PicRateCallbackFactory(pic_id=f"{pic_id}", rate=3)
    )
    builder.button(
        text='😐C0', callback_data=PicRateCallbackFactory(pic_id=f"{pic_id}", rate=2)
    )
    builder.button(
        text='📊️ ?', callback_data=PicRateCallbackFactory(pic_id=f"{pic_id}", rate=0)
    )
    builder.button(
        text='♻️ TRASH 0', callback_data=PicRateCallbackFactory(pic_id=f"{pic_id}", rate=1)
    )
    builder.adjust(4)
    return builder.as_markup()
