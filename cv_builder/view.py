from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Django Backend is Live!"})
