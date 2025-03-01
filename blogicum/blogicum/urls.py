"""blogicum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.conf import settings

from core.views import UserCreateView, UserDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('category/', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('posts/', include('blog.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', UserCreateView.as_view(), name='registration'),
]

if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
