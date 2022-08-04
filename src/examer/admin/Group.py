from django.contrib import admin
from django.utils.safestring import mark_safe

from ..models import Group


class GroupAdmin(admin.ModelAdmin):
    list_display = ["name", "visible", "Пользователи", "Количество"]
    search_fields = ["name"]
    list_editable = ["visible"]
    list_filter = ["visible"]

    def Пользователи(self, obj):
        return mark_safe(
            f'<a href="/admin/examer/usersubscriptions/?group__id__exact={obj.pk}">Список Пользователей</a>')

    def Количество(self, obj):
        return f'{obj.usersubscriptions_set.filter(group=obj).count()}'

    def __init__(self, *args, **kwargs):
        super(GroupAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ("Пользователи","name")


admin.site.register(Group, GroupAdmin)
