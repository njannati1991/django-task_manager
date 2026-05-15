from django.urls import path
from .views import (
    WorkspaceListView,
    WorkspaceCreateView,
)

urlpatterns = [
    path('', WorkspaceListView.as_view(), name='workspace-list'),
    path('create/', WorkspaceCreateView.as_view(), name='workspace-create'),
    
]