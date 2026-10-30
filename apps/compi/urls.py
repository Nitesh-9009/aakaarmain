from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'compi'

urlpatterns = [
    path('', views.index, name="index"),
    path('logiq', views.logiq, name="logiq"),
    path('register-logiq', views.registerLogiq, name="registerLogiq"),
    path('submitted', views.submitted, name="submitted"),
    path('seismic', views.seismic, name="seismic"),
    path('seismic_reg', views.seismic_reg, name="seismic_reg"),
    path('bridgeit', views.bridgeit, name="bridgeit"),
    path('bridgeit_reg', views.bridgeit_reg, name="bridgeit_reg"),
    path('conquerit', views.conquerit, name="conquerit"),
    path('conquerit_reg', views.conquerit_reg, name="conquerit_reg"),
    # path('after_login_url',views.login_soln,name="solved_login"),
    path('msewall', views.msewall_view, name="msewall_url"), 
    path('idp', views.idp, name="idp"), 

    # --- THIS WAS MISSING ---
    path('crackathon', views.crackathon, name="crackathon"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)