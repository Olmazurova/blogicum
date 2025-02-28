from django.shortcuts import render


def page_not_found(request, exeption):
    """
    Настраивает отображение нужного шаблона при ошибке 404.
    """
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """
    Настраивает отображение нужного шаблона при ошибке 403.
    """
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """
    Настраивает отображение нужного шаблона при ошбике 500.
    """
    return render(request, 'pages/500.html', status=500)
