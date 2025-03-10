from django.shortcuts import render
from django.views.generic import TemplateView


class AboutTemplateView(TemplateView):
    """Представление отображения статичной страницы 'О проекте'."""

    template_name = 'pages/about.html'


class RulesTemplateView(TemplateView):
    """Представление отображения статичной страницы 'Правила'."""

    template_name='pages/rules.html'


def page_not_found(request, exception):
    """Настраивает отображение нужного шаблона при ошибке 404."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Настраивает отображение нужного шаблона при ошибке 403."""
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """Настраивает отображение нужного шаблона при ошибке 500."""
    return render(request, 'pages/500.html', status=500)