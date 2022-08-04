from aiogram.types import InlineKeyboardMarkup

from bot.data import callback_data as cd
from bot.data import list_data as ld
from bot.utils.button_worker import add_button

__all__ = [
    "setup_client",
    "get_user_actions",
    "reg_btn"
]


async def reg_btn():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        await add_button(
            text="Зарегистрироваться",
            cd="registration"
        )
    )
    return keyboard


async def setup_client(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for index, text in enumerate(ld.REG_CLIENT):
        keyboard.add(
            await add_button(
                text=text,
                cd=cd.reg.new(
                    action=index + 1
                ))
        )
    if "phone_number" in data:
        keyboard.add(
            await add_button(
                text="Подтвердить данные",
                cd=cd.reg.new(
                    action="submit"
                )
            )
        )
    return keyboard


async def get_user_actions():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        await add_button(
            text="Просмотреть потоки",
            cd="check"))
    keyboard.add(
        await add_button(
            text="Мои потоки",
            cd="my"))
    return keyboard
