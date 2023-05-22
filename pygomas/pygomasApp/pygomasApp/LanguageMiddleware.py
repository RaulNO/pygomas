from django.utils.translation import activate
from django.utils import translation

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lenguage_code = request.COOKIES.get('idioma')
        activate(lenguage_code)
        return self.get_response(request)