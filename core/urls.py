from django.urls import path
from .views import (
    HomeView,
    AdminDashboard,
    UserDashboardView,

    EditPageView,
    DeletePageView

    
)




urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin-dashboard/', AdminDashboard.as_view(), name='admin-dashboard'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('dashboard/edit-page/', EditPageView.as_view(), name='edit-page'),
    path('dashboard/delete-page/', DeletePageView.as_view(), name='delete-page'),


]