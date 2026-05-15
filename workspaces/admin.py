from django.contrib import admin

from .models import Workspace



@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner__username', 'get_member_name')
    list_display_links = ('id', 'name')

    search_fields = ('name', 'owner__')


    def get_member_name(self, obj):
        return ", ".join([member.username for member in obj.members.all()])

    get_member_name.short_description = 'Members'