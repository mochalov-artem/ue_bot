from aiogram.filters.callback_data import CallbackData


class PicRateCallbackFactory(CallbackData, prefix="fabnum"):
    pic_id: str
    rate: int
