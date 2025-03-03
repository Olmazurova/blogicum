from django.urls import path

from . import views
from core.views import UserDetailView

app_name: str = 'blog'

urlpatterns: list[path] = [
    path('', views.IndexListView.as_view(), name='index'),
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path('profile/<str:username>/', UserDetailView.as_view(), name='profile'),
    path('<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path(
        '<int:post_id>/delete/',
        views.PostDeleteView.as_view(),
        name='delete'
    ),
    path('<int:post_id>/edit/', views.PostUpdateView.as_view(), name='edit'),
    path(
        '<slug:category_slug>/',
        views.CategoryListView.as_view(),
        name='category_posts'
    ),
    path(
        '<int:post_id>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment'
    ),
    path(
        '<int:post_id>/edit_comment/<int:comment_id>',
        views.CommentUpdateView.as_view(),
        name='edit_comment'
    ),
    path(
        '<int:post_id>/delete_comment/<int:comment_id>',
        views.CommentDeleteView.as_view(),
        name='delete_comment'
    ),
]
