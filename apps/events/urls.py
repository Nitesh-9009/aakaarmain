from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'events'

urlpatterns = [
    path('', views.index, name="index"),
    path('cenex', views.cenex, name="cenex"),
    path('cenex_reg', views.cenex_reg, name="cenex_reg"),
    path('workshops', views.workshop, name="workshop"),
    path('staadpro_reg', views.staadpro_reg, name="staadpro_reg"),
    path('fusion_reg', views.fusion_reg, name="fusion_reg"),
    path('labvisit', views.labvisit, name="labvisit"),
    path('labvisit_reg', views.labvisit_reg, name="labvisit_reg"),
    path('primavera_reg', views.primavera_reg, name="primavera_reg"),
    path('fusionplusstaad_reg', views.fusionplusstaad_reg, name="fusionplusstaad_reg"),
    path('payment_staad', views.staad_payment, name="staad_payment"),
    path('payment_fusion', views.fusion_payment, name="fusion_payment"),
    path('payment_primavera', views.primavera_payment, name="primavera_payment"),
    path('payment_primaveraplusstaad', views.primaveraplusstaad_payment, name="primavera_primaveraplusstaad_payment"),
    path('payment_fusionplusstaad', views.fusionplusstaad_payment, name="fusionplusstaad_payment"),
    path('payment_labvisit', views.lab_payment, name="lab_payment"),
    path('lecture_series', views.lecture_series, name="lecture_series"),
    path('ceo', views.ceo_reg, name="ceo_reg"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
