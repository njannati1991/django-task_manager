from django.urls import path
from .views import (
    WorkspaceListView,
    WorkspaceDetailView,
    WorkspaceCreateView,
    WorkspaceUpdateView,
    WorkspaceDeleteView,

    AddMemberView,
    DeleteMemberView,
    UpdateMemberView,

)

urlpatterns = [

    path('', WorkspaceListView.as_view(), name='workspace-list'),
    path('create/', WorkspaceCreateView.as_view(), name='workspace-create'),
    path('update/<int:workspace_pk>/', WorkspaceUpdateView.as_view(), name='workspace-update'),
    path('delete/<int:workspace_pk>/', WorkspaceDeleteView.as_view(), name='workspace-delete'),
    path('<int:workspace_pk>/members/add/', AddMemberView.as_view(), name='add-member'),
    path('<int:workspace_pk>/member/<str:username>/delete/', DeleteMemberView.as_view(), name='delete-member'),
    path('<int:workspace_pk>/members/<str:username>/update/', UpdateMemberView.as_view(), name='update-member'),
    path('<int:pk>/', WorkspaceDetailView.as_view(), name='workspace-detail'),

    
]