from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .forms import UserBlogicumCreationForm

User = get_user_model()


class UserCreateView(CreateView):
    """Представление для создания нового пользователя."""

    template_name = 'registration/registration_form.html'
    form_class = UserBlogicumCreationForm
    success_url = reverse_lazy('blog:index')


class UserDetailView(DetailView):
    """Представление страницы профиля пользователя."""

    model = User
    template_name = 'blog/profile.html'
    