from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse


class AuthorTestMixin(UserPassesTestMixin):
    """
    Миксин добавляет функцию test_func,
    которая проверяет является ли пользователь автором поста.
    """

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class ReverseMixin:
    """
    Миксин добавляет функцию get_success_url,
    которая перенаправляет пользователя на страницу поста.
    """

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']},
        )
