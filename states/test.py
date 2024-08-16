from aiogram.fsm.state import StatesGroup, State


class Test(StatesGroup):
    fullName = State() 

class TestStates(StatesGroup):
    fullname = State()
    QUESTION_1 = State()
    QUESTION_2 = State()
    QUESTION_3 = State()
    QUESTION_4 = State()
    QUESTION_5 = State()
    QUESTION_6 = State()
    QUESTION_7 = State()
    QUESTION_8 = State()
    QUESTION_9 = State()
    QUESTION_10 = State()
    QUESTION_11 = State()
    QUESTION_12 = State()
