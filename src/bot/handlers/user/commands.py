from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot
from bot.keyboards import inline as ik
from bot.services.db import user as user_db
from bot.states import UserState
from bot.utils import deleter


async def start_cmd(message: types.Message, state: FSMContext):
    await deleter.delete_mes(message.chat.id, message.message_id)
    user = await user_db.get_user(message.chat.id)
    if not user:
        mes = await bot.send_message(
            chat_id=message.chat.id,
            text="Чтобы продолжить надо пройти регистрацию",
            reply_markup=await ik.reg_btn()
        )

    else:
        mes = await bot.send_message(
            chat_id=message.chat.id,
            text="Текст меню",
        )
    try:
        data = await state.get_data()
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=data.get("main_menu")
        )
    except:
        pass
    await UserState.mm.set()
    await state.update_data({"main_menu": mes.message_id})

async def error(update: types.Update, exception):
    print(exception)
    r = update.get_current()
    try:
        chat_id = r.callback_query.from_user.id
    except:
        chat_id = r.message.from_user.id
    await bot.send_message(
        chat_id=chat_id,
        text="Напишите /start"
    )
    return
