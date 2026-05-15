from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

from .forms import CustomUserCreationForm



class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('workspace-list')

    def form_valid(self, form):

        user = form.save()
        login(self.request, user)

        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'login'
    

