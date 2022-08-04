from django.contrib import admin

from src.examer.models import Exam


class ExamAdmin(admin.ModelAdmin):
    list_display = ["title"]
    list_display_links = ["title"]
    search_fields = ["title"]


admin.site.register(Exam, ExamAdmin)
