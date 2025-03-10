from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from blog.models import Post
from core.forms import UserEditForm

NUMBER_OF_POSTS = 10

User = get_user_model()


class UserCreateView(CreateView):
    """Представление для создания нового пользователя."""

    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:index')


class UserListView(ListView):
    """Представление профиля пользователя."""

    model = User
    template_name = 'blog/profile.html'
    paginate_by = NUMBER_OF_POSTS

    def get_queryset(self):
        return Post.objects.filter(
            author=get_object_or_404(User, username=self.kwargs['username']).id
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(User, username=self.kwargs['username'])
        context['profile'] = profile
        return context

class UserUpdateView(UserPassesTestMixin, UpdateView):
    """Представление редактирования профиля пользователя."""

    model = User
    form_class = UserEditForm
    template_name = 'blog/profile_edit.html'

    def get_object(self, queryset = None):
        return get_object_or_404(User, username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(User, id=self.request.user.id)
        form = UserEditForm(self.request.POST or None, instance=instance)
        context['profile'] = instance
        context['form'] = form
        return context

    def test_func(self):
        object = self.get_object()
        return object == self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )
