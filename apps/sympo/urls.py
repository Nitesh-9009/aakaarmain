from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'sympo'

urlpatterns = [
    path('', views.main_view1, name="index"),
    path('paper/', views.home, name="home"),
    path('paper/submission', views.submission, name="submission"),
    path('paper/submitted', views.submitted, name="submitted"),
    path('new', views.new, name="new"),
    path('academic_writing', views.academic_home, name="academic_writing"),
    path('noniitb_register', views.noniitb_view, name="non_iitb_url"),
    path('iitb_register', views.iitb_view, name="iitb_url"),
    # path('poster_url', views.poster_view, name="poster_name"),
    path('mtt/', views.mtt, name="mtt"), # Added /
    path('thesis', views.mtt, name="mtt"),
    path('city_front', views.city_front, name="city_front"),
    path('poster', views.poster, name="poster"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
