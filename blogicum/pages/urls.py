from django.urls import path
from .views import AboutTemplateView, RulesTemplateView

app_name: str = 'pages'

urlpatterns: list[path] = [
    path(
        'about/',
        AboutTemplateView.as_view(),
        name='about'
    ),
    path(
        'rules/',
        RulesTemplateView.as_view(),
        name='rules'
    ),
]
