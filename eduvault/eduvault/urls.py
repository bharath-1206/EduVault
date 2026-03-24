from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from materials.views import get_materials
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('student/', include('students.urls')),
    path('materials/', include('materials.urls')),
    path('staff/', include('staff.urls')),
    path('api/materials/', get_materials),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)