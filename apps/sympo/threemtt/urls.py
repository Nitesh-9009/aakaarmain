from django.urls import path, include
from . import views

app_name = 'threemtt'

urlpatterns = [
   path('', views.mtt, name="index"),
   path('mtt_reg', views.mtt_reg, name="mtt_reg"),
   path('accounts/', include('allauth.urls')),
]
   #  path('accounts/', include('allauth.urls')),

