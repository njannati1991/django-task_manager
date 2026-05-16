from django.urls import path
from .views import (
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,

)

urlpatterns = [
    path('projects/<int:project_id>/tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),

]