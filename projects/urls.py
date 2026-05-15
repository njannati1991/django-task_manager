from django.urls import path
from .views import (
    ProjectCreateView,
    ProjectDetailView,
)

urlpatterns = [
    path('workspaces/<int:workspace_id>/projects/create/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    

]