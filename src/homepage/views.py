from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


def guide_body(request):
    template = loader.get_template('partials/guide_body.html')
    return HttpResponse(template.render({}, request))


def index_body(request):
    template = loader.get_template('partials/index_body.html')
    return HttpResponse(template.render({}, request))
# Create your views here.
