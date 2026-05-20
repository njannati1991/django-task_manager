from django.urls import path

from invitation.views import InviteMemberView

urlpatterns = [
    path('workspaces/<int:workspace_pk>/', InviteMemberView.as_view(), name='invite-member'),
]

