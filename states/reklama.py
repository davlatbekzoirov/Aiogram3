from aiogram.fsm.state import State, StatesGroup

class Adverts(StatesGroup):
    adverts = State()

class BookState(StatesGroup):
    title = State()
    price = State()
    description = State()
    photo = State()