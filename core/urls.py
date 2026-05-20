from django.urls import path
from .views import (
    HomeView,
    UserDashboardView,

    EditPageView,
    DeletePageView

    
)




urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('dashboard/edit-page/', EditPageView.as_view(), name='edit-page'),
    path('dashboard/delete-page/', DeletePageView.as_view(), name='delete-page'),


]