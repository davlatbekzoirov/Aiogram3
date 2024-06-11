from aiogram.fsm.state import State, StatesGroup

class Adverts(StatesGroup):
    adverts = State()

class AudioState(StatesGroup):
    title = State()
    voice_file_id = State()