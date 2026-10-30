from django.urls import path, include
from . import views

app_name = 'cityplan_app'

urlpatterns = [
    path('', views.front_page, name="index"),
    path('cityplanning/', views.front_page, name="cityplanning"),
    path('accounts/', include('allauth.urls')),
    path('cityplanning/register', views.register_cityplan, name="cityplanning_register"),
    path('cityplanning/registered', views.registered_cityplan, name="cityplanning_registered"),
]
