from django.contrib import admin
from django.utils.safestring import mark_safe

from src.examer.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = [
        "group",
        "exam",
        "date_time",
        "link",
    ]
    list_filter = ["group", "exam", "date_time"]

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
