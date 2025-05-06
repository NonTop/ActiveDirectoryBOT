from aiogram.fsm.state import State, StatesGroup

class AuthState(StatesGroup):
    awaiting_login = State()
    awaiting_code = State()