from aiogram.fsm.state import State, StatesGroup

class Adverts(StatesGroup):
    adverts = State()

class Users(StatesGroup):
    first_name = State()
    phone_number = State()
    age = State()
    role = State()
    selected_option = State()