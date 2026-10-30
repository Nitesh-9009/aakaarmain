from django.contrib import admin
from django.urls import path, include

 
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='aakaar_new.html'), name='home'),
    path('events/', include('events.urls')),
    path('compi/', include('compi.urls')),
    path('sympo/', include('sympo.urls')),
    path('accounts/', include('allauth.urls')),
    path('about/', TemplateView.as_view(template_name='about_legacy.html'), name='about'),
    path('partners/', TemplateView.as_view(template_name='partners_sponsors.html'), name='partners'),
    path('accomodation/', TemplateView.as_view(template_name='accomodation.html'), name='accomodation'),
]

# Serve static and media files automatically in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

