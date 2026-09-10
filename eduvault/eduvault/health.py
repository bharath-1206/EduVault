from django.http import JsonResponse


def health_check(request):
    """Lightweight endpoint used by Render and external uptime monitors."""
    return JsonResponse({"status": "ok"})
