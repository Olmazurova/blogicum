from collections.abc import Callable

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.urls import reverse_lazy, reverse

from .forms import PostForm, CommentForm
from .models import Category, Post, Comment
from .utils import add_default_filters, get_selection_of_posts

NUMBER_OF_POSTS = 10


class IndexListView(ListView):
    """Представление для главной страницы сайта."""

    model = Post
    ordering = 'pub_date'
    paginate_by = NUMBER_OF_POSTS
    template_name = 'blog/index.html'

    def get_queryset(self):
        """Отфильтровывает нужные посты на страницу."""
        return Post.objects.filter(**add_default_filters())


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
    """Представление для отдельного поста."""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self):
        return get_object_or_404(
            get_selection_of_posts('author').filter(id=self.kwargs['post_id']),
            **add_default_filters(),
        )

    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст:
        - форму для создания комментария,
        - авторов комментариев.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


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
    model = Category  # или Post???
    # ordering = 'pub_date'
    # paginate_by = NUMBER_OF_POSTS
    template_name = 'blog/category.html'

    def get_queryset(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )

    # def get_object(self):
    #     return get_object_or_404(
    #         Category,
    #         slug=self.kwargs['category_slug'],
    #         is_published=True
    #     )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = get_selection_of_posts('category').filter(
            category__slug=self.kwargs['category_slug'],
            **add_default_filters(),
        ).order_by('pub_date')
        return context


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


class PostCreateView(LoginRequiredMixin, CreateView):
    """Представление добавления нового поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    # success_url = reverse_lazy('blog:profile')  # Как здесь написать?

    # С помощью этого метода наконец-то стала загружаться
    # страница профиля profile/username
    def get_success_url(self):
        """Перенаправляет на страницу профиля пользователя."""
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )

    def form_valid(self, form):
        """Заполняет поле формы автор и возвращает валидацию формы."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    # TODO: фильтрация


class PostUpdateView(UserPassesTestMixin, UpdateView):
    """Представление редактирования существующего поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        """Добавляем в контекст заполненную форму."""
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form = PostForm(self.request.POST or None, instance=instance)
        context['form'] = form
        return context

    def test_func(self):
        """Проверяет является ли пользователь автором поста."""
        object = self.get_object()
        return object.author == self.request.user

    def get_success_url(self):
        """Перенаправляет пользователя на страницу поста."""
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']},
        )


class PostDeleteView(UserPassesTestMixin, DeleteView):
    """Представление удаления текущего поста."""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        """Добавляем в контекст заполненную форму."""
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form = PostForm(self.request.POST or None, instance=instance)
        context['form'] = form
        return context

    def test_func(self):
        """Проверяет является ли пользователь автором поста."""
        object = self.get_object()
        return object.author == self.request.user

    def get_success_url(self):
        """Перенаправляет на страницу профиля пользователя."""
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Представление создания комментария к посту."""

    post_obj = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        print(kwargs)
        self.post_obj = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.post_obj.pk})


class CommentUpdateView(UserPassesTestMixin, UpdateView):
    """Представление для редактирования комментария к посту."""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def test_func(self):
        """Проверяет является ли пользователь автором поста."""
        object = self.get_object()
        return object.author == self.request.user


class CommentDeleteView(UserPassesTestMixin, DeleteView):
    """Представления для удаления комментария к посту."""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        """Проверяет является ли пользователь автором поста."""
        object = self.get_object()
        return object.author == self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']},
        )
