from logging import getLogger
from aiogram.types import Message
from aiogram.filters import Filter
from bot.configuration import bot_configuration as bot_config
from database.requests import is_user_banned

logger = getLogger(__name__)


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        logger.debug(f"Admin IDs: {bot_config.admin_ids}, Check user: {message.from_user.id} -> "
                     f"{message.from_user.id in bot_config.admin_ids}")
        return message.from_user.id in bot_config.admin_ids


class IsBanned(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        banned = await is_user_banned(message.from_user.id)
        logger.debug(f"Check user: {message.from_user.id} -> Banned user: {banned}")
        return banned
