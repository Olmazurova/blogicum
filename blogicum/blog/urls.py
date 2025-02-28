from django.urls import path

from . import views

app_name: str = 'blog'

urlpatterns: list[path] = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('<slug:category_slug>/', views.category_posts, name='category_posts'),
]
