from collections.abc import Callable

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.urls import reverse_lazy

from .forms import PostForm
from .models import Category, Post
from .utils import add_default_filters, get_selection_of_posts

NUMBER_OF_POSTS = 10


class IndexListView(ListView):
    """
    Представление для главной страницы сайта.
    """
    # Ещё нужно добавить правильную фильтрацию????
    model = Post
    ordering = 'pub_date'
    paginate_by = NUMBER_OF_POSTS
    template_name = 'blog/index.html'


# def index(request: HttpRequest) -> Callable:
#     """Представление для главной страницы сайта."""
#     post_list = Post.objects.filter(
#         **add_default_filters()
#     )[:NUMBER_OF_POSTS]
#     context: dict = {
#         'post_list': post_list
#     }
#     return render(request, 'blog/index.html', context)


class PostDetailView(DetailView):
    """
    Представление для отдельного поста.
    """
    # Фильтрация???
    model = Post
    template_name = 'blog/detail.html'



# def post_detail(request: HttpRequest, post_id: int) -> Callable:
#     """Представление для отдельного поста."""
#     post = get_object_or_404(
#         get_selection_of_posts('author').filter(id=post_id),
#         **add_default_filters(),
#     )
#     context: dict = {'post': post}
#     return render(request, 'blog/detail.html', context)


class CategoryListView(ListView):
    """Представление для категорий постов."""
    # Фильтрация
    model = Category # или Post???
    ordering = 'pub_date'
    paginate_by = NUMBER_OF_POSTS
    template_name = 'blog/category.html'


# def category_posts(request: HttpRequest, category_slug: str) -> Callable:
#     """Представление для категорий постов."""
#     category = get_object_or_404(
#         Category,
#         slug=category_slug,
#         is_published=True
#     )
#     post_list = get_selection_of_posts('category').filter(
#         category__slug=category_slug,
#         **add_default_filters(),
#     )
#     context: dict = {'category': category, 'post_list': post_list}
#     return render(request, 'blog/category.html', context)


class PostCreateView(CreateView):
    """Представление добавления нового поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('profile:<username>')  # Как правильно здесь написать?
    # TODO: Валидация формы, добавление данных в контекст, фильтрация


class PostUpdateView(UpdateView):
    """Представление редактирования существующего поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:post_detail')  # Как правильно???


class PostDeleteView(DeleteView):
    """Представление удаления текущего поста."""

    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('profile:<username>')
    