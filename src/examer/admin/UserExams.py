from django.contrib import admin
from django.utils.safestring import mark_safe

from ..models import UserExams


class UserExamsAdmin(admin.ModelAdmin):
    list_display = ["Пользователь", "event"]
    list_filter = ["event"]

    def Пользователь(self, obj):
        return mark_safe(
            f"<a href=/admin/examer/telegramuser/{obj.user.pk}/change/>{obj.user.name}</a>"
        )

    def __init__(self, *args, **kwargs):
        super(UserExamsAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ("Пользователь",)


admin.site.register(UserExams, UserExamsAdmin)
