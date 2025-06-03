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
        from_emulator = request.POST.get("from")
        to_emulator = request.POST.get("to")
        if not os.path.exists(tempfile.gettempdir() + "/zeldat/"):
            os.mkdir(tempfile.gettempdir() + "/zeldat/")
        temp = tempfile.gettempdir() + "/zeldat/"
        if uploaded_file:
            print(f"File size: {uploaded_file.size} bytes")

        if not uploaded_file or not from_emulator or not to_emulator:
            return HttpResponseBadRequest("Missing data.")

        # Save the uploaded file (for testing)
        with open(f"{temp}{uploaded_file.name}", "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        file_path = f"{temp}{uploaded_file.name}"
        output_path = f"{temp}"

        input_files = f"{temp}{uploaded_file.name}"
        print("INPUT FILE", input_files)
        arg_list = ["-f", from_emulator,
                    "-t", to_emulator,
                    "-i", input_files,
                    "-o", f"translated_{uploaded_file.name}",]
        print(arg_list)
        active_list = mn.parse_args(arg_list)
        print(active_list)
        mn.main_web(arg_list)

        zip_filename = f"translated_{uploaded_file.name}.zip"

        with zipfile.ZipFile(f"output/{zip_filename}", 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in os.listdir("output"):
                print("filename", filename)
                if "translated" in filename and "zip" not in filename:
                    if os.path.isfile(f"output/{filename}"):
                        zipf.write(temp, arcname=filename)
                        print("wrote", filename)
                        os.remove(f"output/{filename}")
        if os.path.exists(output_path):
            print("first if")
            download_url = reverse("download_file") + f"?filename=output/{zip_filename}"
            return HttpResponse(f'<script>window.location="{download_url}"</script>')
        else:
            print("elsed")
            return HttpResponse("File not found", status=404)

        # return HttpResponse(f"""
        #     <p>Uploaded file: {uploaded_file.name}</p>
        #     <p>From: {from_emulator}</p>
        #     <p>To: {to_emulator}</p>
        # """)

    return HttpResponseBadRequest("Invalid request method.")


def download_file(request):
    print("download_file called")
    filename = request.GET.get("filename")


    if os.path.exists(filename):
        return FileResponse(open(filename, 'rb'), as_attachment=True, filename=filename)
    return HttpResponse("File not found download_file", status=404)
