from django.http import HttpResponse
from django.template import loader
from django.http import FileResponse
import os

from django.urls import reverse


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


from django.http import HttpResponse, HttpResponseBadRequest


def translate(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("savefile")
        from_emulator = request.POST.get("from")
        to_emulator = request.POST.get("to")
        if uploaded_file:
            print(f"File size: {uploaded_file.size} bytes")

        if not uploaded_file or not from_emulator or not to_emulator:
            return HttpResponseBadRequest("Missing data.")

        # Save the uploaded file (for testing)
        with open(f"/tmp/{uploaded_file.name}", "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        file_path = f"/tmp/{uploaded_file.name}"

        if os.path.exists(file_path):
            download_url = reverse("download_file") + f"?filename={file_path}"
            return HttpResponse(f'<script>window.location="{download_url}"</script>')
        else:
            return HttpResponse("File not found", status=404)

        # return HttpResponse(f"""
        #     <p>Uploaded file: {uploaded_file.name}</p>
        #     <p>From: {from_emulator}</p>
        #     <p>To: {to_emulator}</p>
        # """)

    return HttpResponseBadRequest("Invalid request method.")


def download_file(request):
    filename = request.GET.get("filename")
    filepath = os.path.join("/tmp", filename)

    if os.path.exists(filepath):
        return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)
    return HttpResponse("File not found", status=404)
