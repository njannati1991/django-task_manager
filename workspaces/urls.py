from django.urls import path
from .views import (
    WorkspaceListView,
    WorkspaceDetailView,
    WorkspaceCreateView,

    AddMemberView,
    DeleteMemberView,
    UpdateMemberView,

)

urlpatterns = [

    path('', WorkspaceListView.as_view(), name='workspace-list'),
    path('create/', WorkspaceCreateView.as_view(), name='workspace-create'),
    path('<int:workspace_pk>/members/add/', AddMemberView.as_view(), name='add-member'),
    path('<int:workspace_pk>/member/<str:username>/delete/', DeleteMemberView.as_view(), name='delete-member'),
    path('<int:workspace_pk>/members/<str:username>/update/', UpdateMemberView.as_view(), name='update-member'),
    path('<int:pk>/', WorkspaceDetailView.as_view(), name='workspace-detail'),

    
]