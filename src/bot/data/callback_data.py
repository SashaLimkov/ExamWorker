from aiogram.utils.callback_data import CallbackData

reg = CallbackData("reg", "action")
user_actions = CallbackData("ua", "action")
choose_group = CallbackData("cg", "action", "group_id")
choose_event = CallbackData("ce", "action", "group_id", "event_id")
sub_to_event = CallbackData("se", "action", "group_id", "event_id", "sub")
sub_to_group = CallbackData("sg", "action", "group_id", "sub")