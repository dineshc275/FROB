from django.http import HttpResponse
from django.views import View


class PageLoadView(View):

    def get(self, request):
        return HttpResponse("<h1 align=center>Hello</h1>"
                            "<h1 align=center>Frob app server is working</h1>")
