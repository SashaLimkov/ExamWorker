from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot
from bot.services.db import groups as db_groups
from bot.services.db import events as db_events
from bot.services.db import user_events as db_user_events
from bot.services.db import user_groups as db_user_groups
from bot.keyboards import inline as ik
from bot.utils.date_time_worker import date_time_formater


async def groups(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    groupss = await db_groups.get_visible_groups()
    if groupss:
        data = await state.get_data()
        message_id = data.get('main_menu')
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            text="Выберите интересующий вас поток",
            message_id=message_id,
            reply_markup=await ik.get_groups(groupss, callback_data)

        )
    else:
        await call.answer(text="Нет доступных потоков", show_alert=True)


async def group_events(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    events = await db_events.get_group_events(callback_data["group_id"])
    group = await db_groups.get_group(callback_data["group_id"])
    if events:
        data = await state.get_data()
        message_id = data.get('main_menu')
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            text=f"Поток: {group.name}\n"
                 f"Выберите Экзамен на который вы хотите записаться. ",
            message_id=message_id,
            reply_markup=await ik.get_events(events, callback_data)
        )
    else:
        await call.answer(text="Нет доступных экзаменов", show_alert=True)
        data = await state.get_data()
        message_id = data.get('main_menu')
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            text=f"Поток: {group.name}",
            message_id=message_id,
            reply_markup=await ik.get_events(events, callback_data)
        )


async def sub_user_to_group(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    group = await db_groups.get_group(callback_data['group_id'])
    user_sub = await db_user_groups.get_user_sub(user_id=call.message.chat.id)
    if user_sub:
        await call.answer(text=f"Вы уже подписаны на {user_sub.group.name}", show_alert=True)
    else:
        await call.answer(text=f"Вы подписались на поток {group.name}", show_alert=True)
        await db_user_groups.sub_to_group(group_id=callback_data['group_id'], user_id=call.message.chat.id)


async def select_event(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('main_menu')
    event = await db_events.get_event(callback_data["event_id"])
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        text=f"Поток: {event.group.name}\n"
             f"Экзамен по предмету: {event.exam.name}\n"
             f"Дата и время: {date_time_formater(str(event.date_time))}",
        message_id=message_id,
        reply_markup=await ik.sub_to_event(callback_data)
    )


async def sub_user_to_event(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    group = await db_groups.get_group(callback_data['group_id'])
    user_sub = await db_user_groups.get_user_sub(user_id=call.message.chat.id)
    if user_sub:
        if str(user_sub.group.pk) != callback_data["group_id"]:
            await call.answer(
                text=f"Вы уже подписаны на другой поток: {user_sub.group.name}, сначала вам нужно отписаться от него и его экзаменов",
                show_alert=True)
        else:
            event = await db_events.get_event(callback_data["event_id"])
            user_ex = await db_user_events.get_user_sub(user_id=call.message.chat.id)
            if user_ex:
                await call.answer(text=f"Вы уже подписаны на {user_ex.event.exam} потока {user_sub.group.name}",
                                  show_alert=True)
            else:
                await call.answer(text=f"Вы подписались на экзамен {event.exam} потока {user_sub.group.name}",
                                  show_alert=True)
                await db_user_events.sub_to_event(event_id=callback_data['event_id'], user_id=call.message.chat.id)

    else:
        await call.answer(text=f"Сначала подпишитесь на поток {group.name}", show_alert=True)
