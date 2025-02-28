from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
# from django.contrib.auth.forms import UserCreationForm

from .forms import UserBlogicumCreationForm


class UserCreateView(CreateView):
    """
    Представление для создания нового пользователя.
    """

    template_name = 'registration/registration_form.html'
    form_class = UserBlogicumCreationForm
    success_url = reverse_lazy('blog:index')
