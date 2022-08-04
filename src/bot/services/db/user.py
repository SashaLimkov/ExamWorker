from asgiref.sync import sync_to_async

from examer.models import TelegramUser


@sync_to_async
def get_user(chat_id) -> TelegramUser:
    user = TelegramUser.objects.filter(chat_id=chat_id).first()
    return user


@sync_to_async
def create_user(chat_id, name, phone_number):
    try:
        user = TelegramUser(chat_id=chat_id, name=name, phone_number=phone_number)
        user.save()
        return user
    except Exception:
        return get_user(chat_id)
