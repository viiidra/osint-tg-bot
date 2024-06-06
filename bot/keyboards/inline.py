from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_keyboard():
    main_btns = {"Search by last name, first name and patronymic ▶️": "flp_name",
                 "Search by last and first name ▶️": "fl_name",
                 "Search by last name ▶️": "last_name",
                 "Search by nickname ▶️": "nickname"}
    return get_callback_btns(btns=main_btns)


def report_keyboard(report_url: str = ''):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🗓 Show report",
                                      web_app=WebAppInfo(url=report_url)))
    return keyboard.adjust(1, ).as_markup()


def search_keyboard():
    search_btns = {"✅ OK": "do_search",
                   "❌ Cancel": "do_cancel"}
    return get_callback_btns(btns=search_btns, sizes=(2,))


def get_callback_btns(*, btns: dict[str, str], sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()
