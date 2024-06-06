from logging import getLogger
from aiogram import Bot
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BotCommand
from aiogram.filters import Command, CommandObject, invert_f, BaseFilter, Filter
from typing import Any
from bot.utils import parse_time
from database.requests import (ban_tg_user,
                               unban_tg_user,
                               unban_all,
                               is_user_banned,
                               get_banned_users,
                               get_spam_users, get_user_requests)
from bot.configuration import bot_configuration as bot_config
from bot.texts.messages import admin_welcome_message, banned_message, admin_wrong_message, no_results_message
from bot.filters import IsAdmin, IsBanned


logger = getLogger(__name__)
admin_router = Router(name=__name__)


@admin_router.message(IsBanned())
async def user_banned(message: Message, bot: Bot | None = None) -> Any:
    logger.debug(f'Message from user {message.from_user.id}, but User is Banned')
    await message.answer(banned_message)


@admin_router.message(invert_f(IsAdmin()), Command("admin", "ban", "tban",
                                                   "users", "unban", "isbanned", "banlist", "stat"))
async def cmd_not_admin(message: Message, bot: Bot | None = None) -> Any:
    logger.debug(f'Admin command from user {message.from_user.id}')
    await message.answer(f"User <b>{message.from_user.full_name}</b> doesn't have admin privileges!")


@admin_router.message(Command("admin"), IsAdmin())
# @admin_router.message(Command("admin"), F.from_user.id.in_(bot_config.admin_ids))
async def cmd_admin(message: Message) -> None:
    logger.debug(f'admin command from {message.from_user.id}, bot admins: {bot_config.admin_ids}')
    await message.answer(f'Welcome, <b>{message.from_user.full_name}</b>!\n{admin_welcome_message}')


@admin_router.message(Command("ban"), IsAdmin())
async def cmd_ban(message: Message, bot: Bot, command: CommandObject | None = None) -> Any:
    logger.debug(f'ban command from {message.from_user.id}, bot admins: {bot_config.admin_ids}')
    try:
        ban_tg_ids = map(int, command.args.split())
        for ban_tg_id in ban_tg_ids:
            await ban_tg_user(tg_id=ban_tg_id, ban_time=None)
            await message.answer(f'⚠️ User {ban_tg_id} is banned!')
    except:
        await message.answer(admin_wrong_message)


@admin_router.message(Command("tban"), IsAdmin())
async def cmd_tban(message: Message, bot: Bot, command: CommandObject | None = None) -> Any:
    logger.debug(f'tban command from {message.from_user.id}, bot admins: {bot_config.admin_ids}')
    try:
        ban_tg_id, ban_time = command.args.split()[:2]
        until_date = parse_time(ban_time)
        if until_date:
            await ban_tg_user(tg_id=int(ban_tg_id), ban_time=until_date)
            await message.answer(f'⚠️ User {ban_tg_id} is banned until {until_date}!')
        else:
            await ban_tg_user(tg_id=int(ban_tg_id), ban_time=None)
            await message.answer(f'⚠️ User {ban_tg_id} is banned!')
    except:
        await message.answer('')


@admin_router.message(Command("unban"), IsAdmin())
async def cmd_unban(message: Message, bot: Bot, command: CommandObject | None = None) -> Any:
    logger.debug(f'unban command from {message.from_user.id}, bot admins: {bot_config.admin_ids}')
    try:
        if not command.args:
            await unban_all()
            await message.answer(f'✅️ ALL users are unbanned!')
        else:
            unban_tg_ids = map(int, command.args.split())
            for unban_tg_id in unban_tg_ids:
                await unban_tg_user(tg_id=unban_tg_id)
                await message.answer(f'✅️ User {str(unban_tg_id)} is unbanned!')
    except:
        await message.answer(admin_wrong_message)


@admin_router.message(Command("isbanned"), IsAdmin())
async def cmd_is_banned(message: Message, bot: Bot, command: CommandObject | None = None) -> Any:
    logger.debug(f'banlist command from {message.from_user.id}, bot admins: {bot_config.admin_ids}')
    try:
        tg_id = int(command.args.split()[0])
        ban_status = await is_user_banned(tg_id=tg_id)
        ban_msg = f'⚠️ User {str(tg_id)} is banned!' if ban_status else f'✅️ User {str(tg_id)} is unbanned!'
        await message.answer(ban_msg)
    except:
        await message.answer(admin_wrong_message)


@admin_router.message(Command("banlist"), IsAdmin())
async def cmd_ban_list(message: Message, bot: Bot, command: CommandObject | None = None) -> Any:
    logger.debug(f'banlist command from {message.from_user.id}, bot admins: {bot_config.admin_ids}')
    try:
        if not command.args:
            num = 1000
        else:
            num = int(command.args.split()[0])
        ban_list = await get_banned_users(number_of_users=num)
        msg = ''
        if len(ban_list):
            for ban_user in ban_list:
                tg_id, ban_time = ban_user
                formatted_time = ban_time.strftime("%d/%m/%Y %H:%M:%S")
                msg = msg + f'User with ID <b>{tg_id}</b> is banned at <i>{formatted_time}</i>\n'
            await message.answer(msg)
    except:
        await message.answer(admin_wrong_message)


@admin_router.message(Command("stat"), IsAdmin())
async def cmd_stat(message: Message, bot: Bot, command: CommandObject | None = None) -> Any:
    logger.debug(f'stat command from {message.from_user.id}, bot admins: {bot_config.admin_ids}')
    try:
        if not command.args:
            num = 20
        else:
            num = int(command.args.split()[0])
        user_list = await get_spam_users(number_of_users=num)
        msg = ''
        if len(user_list):
            for user in user_list:
                tg_id, req = user
                msg = msg + f'User <b>{tg_id}</b> completed <b>{req}</b> request(s).\n'
            await message.answer(msg)
    except:
        await message.answer(admin_wrong_message)


@admin_router.message(Command("requests"), IsAdmin())
async def cmd_requests(message: Message, bot: Bot, command: CommandObject | None = None) -> Any:
    logger.debug(f'requests command from {message.from_user.id}, bot admins: {bot_config.admin_ids}')
    try:
        if not command.args:
            num = 5
        else:
            num = int(command.args.split()[0])
        requests_list = await get_user_requests(number_of_requests=num)
        msg = ''
        for request in requests_list:
            tg_id, tg_username, search_type, search_str, search_time, report_url = request
            msg = msg + (f'Telegram user ID: <b>{tg_id}</b>\n'
                         f'Telegram user name: <b>{tg_username}</b>\n'
                         f'Search type: <b>{search_type.value}</b>\n'
                         f'Search str: <b>{search_str}</b>\n'
                         f'Time: <b>{search_time.strftime("%d/%m/%Y %H:%M:%S")}</b>\n'
                         f'Report URL: <b>{report_url}</b>\n') + '-' * 30 + '\n'
        await message.answer(msg)
    except:
        await message.answer(admin_wrong_message)
