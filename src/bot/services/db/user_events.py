from asgiref.sync import sync_to_async

from examer.models import TelegramUser, Event, UserExams


@sync_to_async
def sub_to_event(event_id, user_id):
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    event = Event.objects.filter(pk=event_id).first()
    sub = UserExams(event=event, user=user)
    sub.save()
    return sub


@sync_to_async
def get_user_sub(user_id):
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    sub = UserExams.objects.filter(user=user).first()
    return sub


@sync_to_async
def delete_user_ex(user_id):
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    sub = UserExams.objects.filter(user=user).first()
    try:
        sub.delete()
    except:
        pass


