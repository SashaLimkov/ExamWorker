from django.contrib import admin

from ..models import TelegramUser


class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "phone_number"]
    list_display_links = ["name"]
    search_fields = ["name", "phone_number"]


admin.site.register(TelegramUser, UserAdmin)
