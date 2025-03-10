from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post
from .utils import add_default_filters, get_selection_of_posts

NUMBER_OF_POSTS = 10


class AuthorTestMixin(UserPassesTestMixin):
    """
    Миксин добавляет test_func,
    которая проверяет является ли пользователь автором поста.
    """

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class ReverseMixin:
    """
    Миксин добавляет get_success_url,
    которая перенаправляет пользователя на страницу поста.
    """

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']},
        )


class IndexListView(ListView):
    """Представление для главной страницы сайта."""

    model = Post
    paginate_by = NUMBER_OF_POSTS
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.objects.filter(
            **add_default_filters()
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')


class PostDetailView(DetailView):
    """Представление для отдельного поста."""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self):
        obj = get_selection_of_posts('author').filter(
            id=self.kwargs['post_id']
        )
        if obj and not obj[0].author == self.request.user:
            filters = add_default_filters()
        else:
            filters = dict()
        return get_object_or_404(obj, **filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class CategoryListView(ListView):
    """Представление для категорий постов."""

    paginate_by = NUMBER_OF_POSTS
    template_name = 'blog/category.html'

    def get_queryset(self):
        queryset = get_selection_of_posts('category').filter(
            category__slug=self.kwargs['category_slug'],
        ).filter(
            **add_default_filters()
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True,
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Представление добавления нового поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(AuthorTestMixin, ReverseMixin, UpdateView):
    """Представление редактирования существующего поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form = PostForm(self.request.POST or None, instance=instance)
        context['form'] = form
        return context

    def handle_no_permission(self):
        return redirect(self.get_success_url())


class PostDeleteView(AuthorTestMixin, DeleteView):
    """Представление удаления текущего поста."""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form = PostForm(self.request.POST or None, instance=instance)
        context['form'] = form
        return context

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CommentCreateView(LoginRequiredMixin, ReverseMixin, CreateView):
    """Представление создания комментария к посту."""

    post_obj = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)


class CommentUpdateView(AuthorTestMixin, ReverseMixin, UpdateView):
    """Представление для редактирования комментария к посту."""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Comment,
            id=self.kwargs['comment_id'],
        )


class CommentDeleteView(AuthorTestMixin, ReverseMixin, DeleteView):
    """Представления для удаления комментария к посту."""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
