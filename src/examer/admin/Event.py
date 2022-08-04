from django.contrib import admin
from django.utils.safestring import mark_safe

from ..models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = [
        "Поток",
        "exam",
        "date_time",
        "link",
        "Пользователи",
        "Количество"
    ]
    list_filter = ["group", "exam"]

    def Поток(self, obj):
        return mark_safe(
            f"<a href=/admin/examer/group/{obj.group.pk}/change/>{obj.group.name}</a>"
        )

    def Пользователи(self, obj):
        return mark_safe(
            f'<a href="/admin/examer/userexams/?event__id__exact={obj.pk}">Список Пользователей</a>')

    def Количество(self, obj):
        return f'{obj.userexams_set.filter(event=obj).count()}'

    def __init__(self, *args, **kwargs):
        super(EventAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ("Пользователи", "link", "date_time")

    # def google(self, obj):
    #     return mark_safe(
    #         '<a href="/admin/app/googletranslate/%s/change/">%s</a>'
    #         % (obj.get_google.pk, obj.get_google.translate))
    #
    # def g_score(self, obj):
    #     return f"{obj.get_google.google_score}"
    #
    # def __init__(self, *args, **kwargs):
    #     super(OriginalAdmin, self).__init__(*args, **kwargs)
    #     self.list_display_links = ("yandex", "google", "tatsoft", "string")
    #     self.ordering = ["-rates"]


admin.site.register(Event, EventAdmin)
