from aiogram import Dispatcher
from aiogram.dispatcher import filters

from bot.data import callback_data as cd
from bot.handlers.user import cleaner, commands, user_registration
from bot.states import UserRegistration


def setup(dp: Dispatcher):
    dp.register_errors_handler(commands.error)
    dp.register_message_handler(commands.start_cmd, filters.CommandStart(), state="*")
    dp.register_callback_query_handler(user_registration.start_client, filters.Text("registration"), state="*")
    dp.register_callback_query_handler(user_registration.start_register_client, cd.reg.filter(),
                                       state=UserRegistration.registration)
    dp.register_message_handler(user_registration.get_phone_number, state=UserRegistration.phone_number)

    dp.register_message_handler(cleaner.clean_s)
