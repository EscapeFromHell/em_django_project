from django.contrib import admin
from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "assignee",
        "deadline",
        "status",
        "estimated_time",
    )
    search_fields = (
        "title",
        "description",
        "author__first_name",
        "author__last_name",
        "assignee__first_name",
        "assignee__last_name",
    )
    list_filter = ("status", "deadline")
