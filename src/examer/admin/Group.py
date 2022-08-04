from django.contrib import admin

from src.examer.models import Group


class GroupAdmin(admin.ModelAdmin):
    list_display = ["title", "visible"]
    list_display_links = ["title"]
    search_fields = ["title"]
    list_editable = ["visible"]
    list_filter = ["visible"]


admin.site.register(Group, GroupAdmin)
