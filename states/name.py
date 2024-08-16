from aiogram.fsm.state import State, StatesGroup

class User(StatesGroup):
    photo = State()
    name = State()