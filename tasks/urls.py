from django.urls import path
from .views import (
    TaskCreateView,
)

urlpatterns = [
    path('projects/<int:project_id>/tasks/create/', TaskCreateView.as_view(), name='task-create'),

]