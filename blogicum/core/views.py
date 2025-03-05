from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from blog.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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

    def get_context_data(self, **kwargs):
        """Добавляем в контекст данные профиля и посты автора."""
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(User, username=self.kwargs['username'])
        page_obj = Post.objects.filter(author=profile.id)
        context['profile'] = profile
        context['page_obj'] = page_obj
        return context

class UserUpdateView(UserPassesTestMixin, UpdateView):
    """Представление редактирования профиля пользователя."""

    model = User
    form_class = UserChangeForm
    template_name = 'registration/registration_form.html'

    def get_context_data(self, **kwargs):
        """Добавляем в контекст заполненную форму."""
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(User, username=self.kwargs['username'])
        form = UserChangeForm(self.request.POST or None, instance=instance)
        context['form'] = form
        return context

    def test_func(self):
        """Проверяет является ли пользователь автором поста."""
        object = self.get_object()
        return object == self.request.user

    def get_success_url(self):
        """Перенаправляет на страницу профиля пользователя."""
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


def page_not_found(request, exeption):
    """Настраивает отображение нужного шаблона при ошибке 404."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Настраивает отображение нужного шаблона при ошибке 403."""
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """Настраивает отображение нужного шаблона при ошбике 500."""
    return render(request, 'pages/500.html', status=500)
