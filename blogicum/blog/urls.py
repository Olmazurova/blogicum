from django.urls import path

from . import views

app_name: str = 'blog'

urlpatterns: list[path] = [
    path('', views.IndexListView.as_view(), name='index'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/delete', views.PostDeleteView.as_view(), name='delete'),
    path('<int:post_id>/edit/', views.PostUpdateView.as_view(), name='edit'),
    path('<slug:category_slug>/', views.CategoryListView.as_view(), name='category_posts'),
]
