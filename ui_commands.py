from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_ui_commands(bot: Bot):
    commands = [
        BotCommand(command="mem", description="МЕМ"),
        BotCommand(command="top", description="ТОП"),
        BotCommand(command="stats", description="ПРОГРЕСС"),
    ]
    await bot.set_my_commands(
        commands=commands,
        # scope=BotCommandScopeAllPrivateChats()
    )
