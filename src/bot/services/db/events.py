from asgiref.sync import sync_to_async

from examer.models import Event, Group


@sync_to_async
def get_group_events(group_id):
    group = Group.objects.get(pk=group_id)
    events = Event.objects.filter(group=group).all()
    return events

@sync_to_async
def get_event(event_id):
    event = Event.objects.get(pk=event_id)
    return event
