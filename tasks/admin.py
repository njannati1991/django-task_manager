from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'project', 'status', 'priority', 'assigned_to', 'due_date')
    list_display_links = ('id', 'title')

    list_filter = ('status', 'priority', )

    search_fields = ('title', )

