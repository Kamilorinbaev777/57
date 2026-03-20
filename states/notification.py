from logging import captureWarnings
from aiogram.fsm.state import State, StatesGroup

class newNotificaton(StatesGroup):
    group = State()
    date = State()
    content = State()
    content_type = State()
    caption = State()