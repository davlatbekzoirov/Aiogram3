from aiogram.fsm.state import State, StatesGroup

class Adverts(StatesGroup):
    adverts = State()

class TM(StatesGroup):
    tuman = State()
    mahalla = State()
    ovoz= State()
    name = State()

class Mahalla(StatesGroup):
    mahalla = State()
    maktab = State()
    nomzod = State()
