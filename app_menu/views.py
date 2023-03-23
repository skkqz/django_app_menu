from django.views.generic import TemplateView


class IndexPageView(TemplateView):
    """
    Представление главной страницы сайта
    """
    template_name = 'index.html'
