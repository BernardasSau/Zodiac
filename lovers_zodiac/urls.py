from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = ([
                   path("admin/", admin.site.urls),
                   path("main/", include("zodiacapp.urls")),
                   path('', RedirectView.as_view(url='/main/', permanent=True)),
               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
               static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
