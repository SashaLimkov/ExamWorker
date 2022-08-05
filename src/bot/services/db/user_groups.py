from asgiref.sync import sync_to_async

from examer.models import UserSubscriptions, TelegramUser, Group


@sync_to_async
def sub_to_group(group_id, user_id):
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    group = Group.objects.filter(pk=group_id).first()
    sub = UserSubscriptions(group=group, user=user)
    sub.save()
    return sub


@sync_to_async
def get_user_sub(user_id):
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    sub = UserSubscriptions.objects.filter(user=user).first()
    return sub


@sync_to_async
def delete_user_ex(user_id):
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    sub = UserSubscriptions.objects.filter(user=user).first()
    sub.delete()
