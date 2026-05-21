from django.contrib import admin

from .models import Workspace, WorkspaceMember



@admin.register(WorkspaceMember)
class WorkspaceMemberShipAdmin(admin.ModelAdmin):
    list_display = ['id', 'member', 'workspace', 'role', 'is_active']
    list_display_links = ('id', 'member')

    



@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner')
    list_display_links = ('id', 'name')

    search_fields = ('name', 'owner__username')
    


    # def get_member_name(self, obj):
    #     return ", ".join([member.username for member in obj.members.all()])

    # get_member_name.short_description = 'Members'