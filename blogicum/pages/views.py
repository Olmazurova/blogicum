from django.views.generic import TemplateView


class AboutTemplateView(TemplateView):
    """Представление отображения статичной страницы "О проекте"."""

    template_name = 'pages/about.html'


class RulesTemplateView(TemplateView):
    """Представление отображения статичной страницы "Правила"."""

    template_name='pages/rules.html'
