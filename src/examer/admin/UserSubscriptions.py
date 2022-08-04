from django.contrib import admin
from django.utils.safestring import mark_safe

from ..models import UserSubscriptions


class UserSubscriptionsAdmin(admin.ModelAdmin):
    list_display = ["Пользователь", "group"]
    list_filter = ["group"]

    def Пользователь(self, obj):
        return mark_safe(
            f"<a href=/admin/examer/telegramuser/{obj.user.pk}/change/>{obj.user.name}</a>"
        )

    def __init__(self, *args, **kwargs):
        super(UserSubscriptionsAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ("Пользователь",)


admin.site.register(UserSubscriptions, UserSubscriptionsAdmin)
