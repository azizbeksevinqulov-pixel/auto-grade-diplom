from django.http import HttpResponse

def test_page(request):
    return HttpResponse("Test tizimi ishlayapti ✅")
