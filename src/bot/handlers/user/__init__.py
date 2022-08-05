from aiogram import Dispatcher
from aiogram.dispatcher import filters

from bot.data import callback_data as cd
from bot.handlers.user import cleaner, commands, user_registration, groups_and_events, user_groups
from bot.states import UserRegistration


def setup(dp: Dispatcher):
    dp.register_errors_handler(commands.error)
    dp.register_message_handler(commands.start_cmd, filters.CommandStart(), state="*")
    dp.register_callback_query_handler(commands.user_menu_call, filters.Text("back"), state="*")
    dp.register_callback_query_handler(user_registration.start_client, filters.Text("registration"), state="*")
    dp.register_callback_query_handler(user_registration.start_register_client, cd.reg.filter(),
                                       state=UserRegistration.registration)
    dp.register_message_handler(user_registration.get_phone_number, state=UserRegistration.phone_number)
    dp.register_callback_query_handler(groups_and_events.groups, cd.user_actions.filter(action="check"), state="*")
    dp.register_callback_query_handler(user_groups.groups, cd.user_actions.filter(action="my"), state="*")
    dp.register_callback_query_handler(groups_and_events.group_events, cd.choose_group.filter(), state="*")
    dp.register_callback_query_handler(groups_and_events.sub_user_to_group, cd.sub_to_group.filter(), state="*")
    dp.register_callback_query_handler(groups_and_events.select_event, cd.choose_event.filter(), state="*")
    dp.register_callback_query_handler(groups_and_events.sub_user_to_event, cd.sub_to_event.filter(), state="*")
    dp.register_callback_query_handler(user_groups.unsub_gr, filters.Text("unsubgr"), state="*")
    dp.register_callback_query_handler(user_groups.unsub_ex, filters.Text("unsubex"), state="*")
    dp.register_message_handler(cleaner.clean_s)
