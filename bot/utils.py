import re

from datetime import datetime, timedelta
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from database.engine import drop_tables, create_tables


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(
            command="start",
            description="Start the bot"
        ),
        BotCommand(
            command="search",
            description="Search information about a person"
        ),
        BotCommand(
            command="help",
            description="How to use the bot"
        ),
        BotCommand(
            command="about",
            description="About the bot"
        ),
        BotCommand(
            command="support",
            description="Contact support"
        )
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


async def on_startup() -> None:
    await create_tables()
    pass


async def on_shutdown() -> None:
    ...


def parse_time(time_str: str | None) -> datetime | None:
    if not time_str:
        return None
    current_datetime = datetime.now()
    match_ = re.match(r'(\d+)([a-z])', time_str.lower().strip())
    if match_:
        value, unit = int(match_.group(1)), match_.group(2)
        match unit:
            case 'm':
                time_delta = timedelta(minutes=value)
            case 'h':
                time_delta = timedelta(hours=value)
            case 'd':
                time_delta = timedelta(days=value)
            case 'w':
                time_delta = timedelta(weeks=value)
            case _:
                return None
    else:
        return None
    return current_datetime + time_delta
