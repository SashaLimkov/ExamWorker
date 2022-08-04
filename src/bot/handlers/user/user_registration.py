from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot
from bot.data import text_data as td
from bot.keyboards import inline as ik
from bot.states import UserRegistration
from bot.services.db import user as user_db
from bot.utils.deleter import delete_user_message

from bot.utils.number_validator import is_phone_number_valid
from bot.utils.state_worker import get_info_from_state
from examer.models import TelegramUser


async def start_client(call: types.CallbackQuery, state: FSMContext):
    await get_panel(call.message, state)


async def start_register_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    data = await state.get_data()
    mes_id = data.get("main_menu")
    user_id = call.message.chat.id
    if action == "1":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=mes_id,
            text=td.GET_NAME
        )
        await UserRegistration.phone_number.set()
    else:
        await state.reset_state(with_data=False)
        await confirm_data(call, state)


async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    valid = await is_phone_number_valid(phone_number)
    if valid:
        await state.update_data({"phone_number": phone_number})
        await delete_user_message(message=message)
        await get_panel(message, state)
    else:
        data = await state.get_data()
        mes_id = data.get("main_menu")
        await bot.delete_message(
            message.chat.id,
            mes_id
        )
        mes = await bot.send_message(
            message.chat.id,
            "Введите номер телефона в формате 89999999999"
        )
        await delete_user_message(message)
        await state.update_data({"main_menu": mes.message_id})


async def get_panel(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    data = await state.get_data()
    name = message.chat.first_name
    mes_id = data.get('main_menu')
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=mes_id,
        text=td.CLIENT_REG_MENU.format(
            name=name,
            phone_number=await get_info_from_state(data, "phone_number"),
        ),
        reply_markup=await ik.setup_client(data)
    )
    await UserRegistration.registration.set()


async def confirm_data(call: types.CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    data = await state.get_data()
    phone_number = await get_info_from_state(data, "phone_number")
    name = call.message.chat.first_name
    await user_db.create_user(chat_id=user_id, phone_number=phone_number, name=name)
    await client_act_menu(call=call)


async def client_act_menu(call: types.CallbackQuery):
    user_id = call.message.chat.id
    user = await user_db.get_user(user_id)
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        text=f"{user.name}, здравствуйте!",
        message_id=call.message.message_id,
        reply_markup=await ik.get_user_actions()
    )


async def check(call: types.CallbackQuery, state: FSMContext):
    print(call.data)
    print(await state.get_state())
    print(await state.get_data())
