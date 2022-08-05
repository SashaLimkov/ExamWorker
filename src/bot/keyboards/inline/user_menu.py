from aiogram.types import InlineKeyboardMarkup

from bot.data import callback_data as cd
from bot.data import list_data as ld
from bot.utils.button_worker import add_button

__all__ = [
    "setup_client",
    "get_user_actions",
    "reg_btn",
    "get_groups",
    "get_events",
    "sub_to_event",
    "un_subscribe"
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
            cd=cd.user_actions.new(
                action="check"
            )))
    keyboard.add(
        await add_button(
            text="Мой поток",
            cd=cd.user_actions.new(
                action="my"
            )))
    return keyboard


async def get_groups(groups, callback_data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for group in groups:
        keyboard.add(
            await add_button(
                text=group.name,
                cd=cd.choose_group.new(
                    action=callback_data["action"],
                    group_id=group.id
                )
            )
        )
    keyboard.add(
        await add_button(
            text="Назад",
            cd="back"
        )
    )
    return keyboard


async def get_events(events, callback_data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    if events:
        for event in events:
            keyboard.add(
                await add_button(
                    text=event.exam.name,
                    cd=cd.choose_event.new(
                        action=callback_data["action"],
                        group_id=callback_data["group_id"],
                        event_id=event.id
                    )
                )
            )
    keyboard.add(
        await add_button(
            text="Подписаться",
            cd=cd.sub_to_group.new(
                action=callback_data["action"],
                group_id=callback_data["group_id"],
                sub="1",
            )
        )
    )
    keyboard.add(
        await add_button(
            text="Назад",
            cd=cd.user_actions.new(
                action=callback_data["action"],
            )
        )
    )
    return keyboard


async def sub_to_event(callback_data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        await add_button(
            text="Подписаться",
            cd=cd.sub_to_event.new(
                action=callback_data["action"],
                group_id=callback_data["group_id"],
                event_id=callback_data["event_id"],
                sub="1",
            )
        )
    )
    keyboard.add(
        await add_button(
            text="Назад",
            cd=cd.choose_group.new(
                action=callback_data["action"],
                group_id=callback_data["group_id"]
            )
        )
    )
    return keyboard


async def un_subscribe(exam):
    keyboard = InlineKeyboardMarkup(row_width=1)
    if exam:
        keyboard.add(
            await add_button(
                text="Отписаться от экзамена",
                cd="unsubex"
            ))
    keyboard.add(
        await add_button(
            text="Отписаться от потока",
            cd="unsubgr"
        )
    )
    keyboard.add(
        await add_button(
            text="Назад",
            cd="back"
        )
    )
    return keyboard
