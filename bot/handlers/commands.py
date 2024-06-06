import bot.keyboards.inline as inline_kb

from logging import getLogger
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from bot.states import BotState
from aiogram.fsm.context import FSMContext
from bot.texts.messages import search_message, help_message, about_message, support_message

logger = getLogger(__name__)
commands_router = Router(name=__name__)


@commands_router.message(CommandStart())
@commands_router.message(Command(commands='search'))
async def cmd_start(message: Message, state: FSMContext) -> None:
    logger.debug(f'Command start or search from user {message.from_user.id}, state: {await state.get_state()}')
    await message.answer(text=f'Hello, <b>{message.from_user.full_name}</b>!\n'
                              f'{search_message}'
                              f'Make your choice below.', reply_markup=inline_kb.main_keyboard(),
                         one_time_keyboard=True)
    await state.set_state(BotState.start)
    logger.debug(f'Command start from user {message.from_user.id} executed, state: {await state.get_state()}')


@commands_router.message(Command(commands='help'))
async def cmd_help(message: Message, state: FSMContext) -> None:
    logger.debug(f'Command help from user {message.from_user.id}')
    await message.answer(text=help_message)


@commands_router.message(Command(commands='about'))
async def cmd_about(message: Message, state: FSMContext) -> None:
    logger.debug(f'Command about from user {message.from_user.id}, state: {await state.get_state()}')
    await message.answer(text=about_message)


@commands_router.message(Command(commands='support'))
async def cmd_about(message: Message, state: FSMContext) -> None:
    logger.debug(f'Command support from user {message.from_user.id}, state: {await state.get_state()}')
    await message.answer(text=support_message)
