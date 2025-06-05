import tempfile

from django.template import loader
from django.http import FileResponse
import os
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
import main as mn
import zipfile


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
        uploaded_file = request.FILES.get("savefile")
        if request.FILES.get("savefile2"):
            uploaded_files = [uploaded_file, request.FILES.get("savefile2")]
        else:
            uploaded_files = [uploaded_file,]
        from_emulator = request.POST.get("from")
        to_emulator = request.POST.get("to")
        temp = tempfile.gettempdir()

        if not uploaded_file or not from_emulator or not to_emulator:
            return HttpResponseBadRequest("Missing data.")

        # Save the uploaded file (for testing)
        for f in uploaded_files:
            with open(f"{temp}{f.name}", "wb+") as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        input_files = []
        for f in uploaded_files:
            input_files.append(f"{temp}{f.name}")

        print("INPUT FILE", input_files)
        arg_list = ["-f", from_emulator,
                    "-t", to_emulator,
                    "-i", input_files if len(input_files) > 1 else input_files[0],
                    "-o", f"translated_{uploaded_file.name}",]
        print(arg_list)
        mn.main_web(arg_list)

        zip_filename = f"translated_{uploaded_file.name}.zip"

        with zipfile.ZipFile(f"output/{zip_filename}", 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in os.listdir("output"):
                if "translated" in filename and "zip" not in filename:
                    if os.path.isfile(f"output/{filename}"):
                        zipf.write(f"output/{filename}", arcname=filename)
                        print("wrote", filename)
                        os.remove(f"output/{filename}")
        if os.path.exists(f"output/"):
            download_url = reverse("download_file") + f"?filename=output/{zip_filename}"
            return HttpResponse(f'<script>window.location="{download_url}"</script>')
        else:
            return HttpResponse("File not found", status=404)

    return HttpResponseBadRequest("Invalid request method.")


def download_file(request):
    filename = request.GET.get("filename")


    if os.path.exists(filename):
        return FileResponse(open(filename, 'rb'), as_attachment=True, filename=filename)
    return HttpResponse("File not found download_file", status=404)
