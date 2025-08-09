from django.http import JsonResponse, HttpResponseRedirect, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import URLMap
import json
from django.shortcuts import render
@csrf_exempt
def shorten_url(request):
    if request.method == "POST":
        data = json.loads(request.body)
        long_url = data.get("url")
        if not long_url:
            return JsonResponse({"error": "URL is required"}, status=400)
        url_obj = URLMap(long_url=long_url)
        url_obj.save()
        return JsonResponse({"short_url": f"http://localhost:8000/{url_obj.short_code}"})
    return JsonResponse({"error": "Only POST method allowed"}, status=405)

def redirect_url(request, short_code):
    try:
        url = URLMap.objects.get(short_code=short_code)
        return HttpResponseRedirect(url.long_url)
    except URLMap.DoesNotExist:
        raise Http404("Short URL not found")

def home(request):
    urls = URLMap.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'urls': urls})