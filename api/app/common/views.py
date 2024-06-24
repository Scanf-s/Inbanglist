from django.http import HttpResponse
from django.views import View


class RootView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("<h1>API</h1>")
