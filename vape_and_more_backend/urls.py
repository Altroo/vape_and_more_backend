from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health_check(_request):
    return JsonResponse({"status": "healthy"})


urlpatterns = [
    path("api/health/", health_check, name="health-check"),
    path("api/website/", include("catalog.urls")),
    path("gestion-interne-vm62/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
