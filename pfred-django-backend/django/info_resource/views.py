from django.http import HttpRequest, HttpResponse

VERSION="2.0.0"

# Create your views here.
def get_version(request: HttpRequest):
    return HttpResponse(VERSION, status=200, content_type="text/plain")
