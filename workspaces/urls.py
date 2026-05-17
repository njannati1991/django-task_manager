from django.urls import path
from .views import (
    WorkspaceListView,
    WorkspaceDetailView,
    WorkspaceCreateView,

    AddMemberView,
)

urlpatterns = [

    path('', WorkspaceListView.as_view(), name='workspace-list'),
    path('create/', WorkspaceCreateView.as_view(), name='workspace-create'),
    path('<int:workspace_id>/members/add/', AddMemberView.as_view(), name='add-member'),
    path('<int:pk>/', WorkspaceDetailView.as_view(), name='workspace-detail'),

    
]