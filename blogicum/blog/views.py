from collections.abc import Callable

from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from .models import Category, Post
from .utils import add_default_filters, get_selection_of_posts

NUMBER_OF_POSTS = 5


def index(request: HttpRequest) -> Callable:
    """Представление для главной страницы сайта."""
    post_list = Post.objects.filter(
        **add_default_filters()
    )[:NUMBER_OF_POSTS]
    context: dict = {
        'post_list': post_list
    }
    return render(request, 'blog/index.html', context)


def post_detail(request: HttpRequest, post_id: int) -> Callable:
    """Представление для отдельного поста."""
    post = get_object_or_404(
        get_selection_of_posts('author').filter(id=post_id),
        **add_default_filters(),
    )
    context: dict = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request: HttpRequest, category_slug: str) -> Callable:
    """Представление для категорий постов."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_selection_of_posts('category').filter(
        category__slug=category_slug,
        **add_default_filters(),
    )
    context: dict = {'category': category, 'post_list': post_list}
    return render(request, 'blog/category.html', context)
