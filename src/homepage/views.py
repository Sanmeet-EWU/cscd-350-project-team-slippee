from django.http import HttpResponse
from django.template import loader
from homepage.translate import return_something


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


def guide_body(request):
    template = loader.get_template('partials/guide_body.html')
    return HttpResponse(template.render({}, request))


def index_body(request):
    template = loader.get_template('partials/index_body.html')
    return HttpResponse(template.render({}, request))


def test_page(request):
    template = loader.get_template('partials/test_page.html')
    return HttpResponse(template.render({}, request))


def translate(request):
    if request.method == "POST":
        emu_from = request.POST.get('from', 'default_from')
        emu_to = request.POST.get('to', 'default_to')
        file_name = request.POST.get('file-input', 'default_file')
        return HttpResponse(f"<p>{emu_from, emu_to, file_name}</p>")
# Create your views here.
