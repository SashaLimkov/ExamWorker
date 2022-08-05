from asgiref.sync import sync_to_async

from examer.models import Group


@sync_to_async
def get_visible_groups():
    groups = Group.objects.filter(visible=False).all()
    return groups


@sync_to_async
def get_group(group_id):
    group = Group.objects.filter(pk=group_id).first()
    return group

