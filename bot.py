import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from mega import Mega
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config_reader import config
from handlers.callbacks import pic_rate, wannamem_yes
from handlers.commands import db_statistics, mem, test, wannamem, top, scheduled_mem
from middlewares.database import DbSessionMiddleware
from ui_commands import set_ui_commands

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=config.bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

try:
    m = Mega()
    m._login_user(config.mega_email.get_secret_value(), config.mega_password.get_secret_value())
except Exception as e:
    m = None
    logging.error(e)


async def on_startup():
    pass


async def main():
    engine = create_async_engine(url=config.db_url.get_secret_value())
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.startup.register(on_startup)
    dp['mega'] = m
    dp.include_routers(
        mem.router,
        wannamem.router,
        top.router,
        db_statistics.router,
        scheduled_mem.router,
        test.router
    )
    dp.include_routers(
        wannamem_yes.router,
        pic_rate.router
    )

    await set_ui_commands(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
