from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateView(CreateView):
    """Представление для создания нового пользователя."""

    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:index')


class UserDetailView(DetailView):
    """Представление страницы профиля пользователя."""

    model = User
    template_name = 'blog/profile.html'

    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs.get('username'))


def page_not_found(request, exeption):
    """Настраивает отображение нужного шаблона при ошибке 404."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Настраивает отображение нужного шаблона при ошибке 403."""
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """Настраивает отображение нужного шаблона при ошбике 500."""
    return render(request, 'pages/500.html', status=500)
