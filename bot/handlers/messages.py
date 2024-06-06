import bot.keyboards.inline as inline_kb

from logging import getLogger
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from datetime import datetime
from bot.states import BotState
from aiogram.fsm.context import FSMContext
from bot.form_results import form_html, upload_html_results, delete_temp_file
from bot.texts.messages import (search_types,
                                no_results_message,
                                unsupported_content_message,
                                search_canceled_message)
from bot.crawler import uni_search
from bot.configuration import bot_configuration as bot_config
from database.requests import save_user_request
from translator.google import translate as google_translate

logger = getLogger(__name__)
messages_router = Router(name=__name__)


@messages_router.message(StateFilter(BotState.search))
async def message_while_search(message: Message, state: FSMContext) -> None:
    logger.debug(f'Message from user {message.from_user.id}, state: {await state.get_state()}')
    await message.answer(text=f'Be patient please. Search in progress...')


@messages_router.callback_query(StateFilter(BotState.dialog_name))
async def final_dialog(callback_query: CallbackQuery, state: FSMContext):
    logger.debug(f'Callback {repr(callback_query.data)} from user {callback_query.from_user.id}, '
                 f'state: {await state.get_state()}')
    await callback_query.message.edit_text(text=callback_query.message.text, reply_markup=None)
    if callback_query.data == 'do_search':
        await state.set_state(BotState.search)
        logger.debug(f'State is {await state.get_state()} now')
        stored_data = await state.get_data()
        search_type, search_name = stored_data['search_by'], stored_data['name']
        logger.debug(f'User: {callback_query.from_user.id} data: {search_type}, {search_name}')

        results = await uni_search(search_type=search_type, name=search_name)
        # logger.debug(f'Search results: {results}')

        if not any(results.values()):
            await callback_query.message.answer(no_results_message)
        else:
            logger.debug(f'Search results: {results}')
            name_eng = await google_translate(text=search_name, lang_code='en')
            results_filename = (datetime.now().strftime('%Y%m%d%H%M%S') + '-' +
                                str(callback_query.from_user.id) + '-' +
                                name_eng.replace(' ', '_') + '.html')
            logger.debug(f'Search results filename: {results_filename}')
            html_report_file = await form_html(results=results, file_path=results_filename,
                                               report_url=bot_config.reports_remote_url + results_filename)
            logger.debug(f'Temporary HTML report file: {html_report_file}')
            remote_report_filename = await upload_html_results(file_path=html_report_file, filename=results_filename)
            logger.debug(f'Remote HTML report file name: {remote_report_filename}')
            await callback_query.message.answer("Report is ready!",
                                                reply_markup=inline_kb.report_keyboard(
                                                    report_url=remote_report_filename))
            await save_user_request(tg_id=callback_query.from_user.id,
                                    tg_username=f'{callback_query.from_user.username} '
                                                f'({callback_query.from_user.full_name})',
                                    search_type=search_type,
                                    search_str=search_name,
                                    report_url=f'{remote_report_filename}')
            await delete_temp_file(file_path=html_report_file)
        await state.clear()
    else:  # Pressed Cancel
        await callback_query.message.answer(search_canceled_message)
    await state.clear()
    logger.debug(f'state: {await state.get_state()}')


@messages_router.message(StateFilter(BotState.dialog_type))
async def dialog_type(message: Message, state: FSMContext):
    logger.debug(f'Message {message.text} from user {message.from_user.id}, '
                 f'state: {await state.get_state()}')
    words_cnt = {'flp_name': 3, 'fl_name': 2, 'last_name': 1, 'nickname': 1}
    search_type = await state.get_data()
    words_required = words_cnt[search_type['search_by']]
    if len(message.text.split()) == words_required:
        await state.update_data(name=message.text)
        await state.set_state(BotState.dialog_name)
        logger.debug(f'Message data from state: {await state.get_data()}, State is {await state.get_state()}')
        await message.answer(text=f'The search by {search_types[search_type["search_by"]]} will be performed '
                                  f'for <b>{message.text}</b>', reply_markup=inline_kb.search_keyboard())
    else:
        await message.reply(text=f'You must enter {words_required} word(s)')
        await message.answer(text=f'Input {search_types[search_type["search_by"]]} ⬇️')


@messages_router.callback_query(StateFilter(BotState.start))
async def messages_start(callback_query: CallbackQuery, state: FSMContext) -> None:
    logger.debug(f'Callback {repr(callback_query.data)} from user {callback_query.from_user.id}, '
                 f'state: {await state.get_state()}')
    await state.update_data(search_by=callback_query.data)
    logger.debug(f'Callback query data from state: {await state.get_data()}')
    await state.set_state(BotState.dialog_type)
    logger.debug(f'State is {await state.get_state()} now')
    await callback_query.message.edit_text(text=callback_query.message.text, reply_markup=None)
    await callback_query.message.answer(text=f'✔️You have chosen to search by {search_types[callback_query.data]}')
    await callback_query.message.answer(text=f'Input {search_types[callback_query.data]} ⬇️')


@messages_router.message(F.animation | F.document | F.file | F.video | F.photo | F.gif | F.audio | F.sticker)
async def message_with_unsupported_content(message: Message):
    await message.answer_sticker('CAACAgIAAxkBAAINkmZNIk8x2f9eg2LbFGVK0SvRZPiqAAL5GQACRceASCpKdk9ErHumNQQ')
    await message.answer(unsupported_content_message)
