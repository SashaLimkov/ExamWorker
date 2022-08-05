from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot
from bot.handlers.user.commands import user_menu_call
from bot.services.db import user_groups as db_user_groups
from bot.services.db import user_events as db_user_events
from bot.keyboards import inline as ik
from bot.utils.date_time_worker import date_time_formater


async def groups(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    groupss = await db_user_groups.get_user_sub(call.message.chat.id)
    if groupss:
        exam = await db_user_events.get_user_sub(call.message.chat.id)
        text = f"Вы числитесь в потоке {groupss.group.name}\n"
        data = await state.get_data()
        message_id = data.get('main_menu')
        if exam:
            text += f"Выбранный экзамен: {exam.event.exam}\n" \
                    f"Время экзамена: {date_time_formater(str(exam.event.date_time))}\n" \
                    f"Ссылка для подключения: {exam.event.link}"
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            text=text,
            message_id=message_id,
            reply_markup=await ik.un_subscribe(exam)
        )
    else:
        await call.answer(text="Вы не числитесь ни на одном потоке", show_alert=True)


async def unsub_ex(call: types.CallbackQuery, state: FSMContext):
    await db_user_events.delete_user_ex(call.message.chat.id)
    await call.answer(text="Вы отписались от экзамена", show_alert=True)
    await user_menu_call(call, state)


async def unsub_gr(call: types.CallbackQuery, state: FSMContext):
    await db_user_events.delete_user_ex(call.message.chat.id)
    await db_user_groups.delete_user_ex(call.message.chat.id)
    await call.answer(text="Вы отписались от потока и экзамена",show_alert=True)
    await user_menu_call(call, state)
