from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegistration(StatesGroup):
    registration = State()
    phone_number = State()
