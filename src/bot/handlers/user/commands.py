from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot
from bot.keyboards import inline as ik
from bot.services.db import user as user_db
from bot.states import UserState
from bot.utils import deleter


async def start_cmd(message: types.Message, state: FSMContext):
    user = await user_db.get_user(message.chat.id)
    try:
        data = await state.get_data()
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=data.get("main_menu")
        )
    except:
        pass
    if not user:
        mes = await bot.send_message(
            chat_id=message.chat.id,
            text="Чтобы продолжить надо пройти регистрацию",
            reply_markup=await ik.reg_btn()
        )
    else:
        mes = await user_menu(message, state)

    await deleter.delete_mes(message.chat.id, message.message_id)
    await UserState.mm.set()
    await state.update_data({"main_menu": mes.message_id})


async def user_menu_call(call: types.CallbackQuery, state: FSMContext):
    await user_menu(call.message, state)


async def user_menu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.chat.id
    user = await user_db.get_user(user_id)
    try:
        message_id = data.get("main_menu")
        mes = await bot.edit_message_text(
            chat_id=message.chat.id,
            text=f"{user.name}, здравствуйте!",
            message_id=message_id,
            reply_markup=await ik.get_user_actions()
        )
    except:
        mes = await bot.send_message(
            chat_id=message.chat.id,
            text=f"{user.name}, здравствуйте!",
            reply_markup=await ik.get_user_actions()
        )
        await UserState.mm.set()
        await state.update_data({"main_menu": mes.message_id})
    return mes


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
