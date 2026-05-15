from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'workspace__name')
    list_display_links = ('id', 'name')
    list_filter = ('workspace__name', )

    search_fields = ('name', 'workspcase__name')


    prepopulated_fields = {'slug': ('name', )}
    
