from aiogram.fsm.state import StatesGroup, State


class BotState(StatesGroup):
    start = State()
    dialog_type = State()
    dialog_name = State()
    search = State()

