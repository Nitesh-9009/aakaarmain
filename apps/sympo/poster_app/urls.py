from django.urls import path, include
from . import views

app_name = 'poster_app'

urlpatterns = [
    path('', views.poster_view, name="index"),
    path('poster/', views.poster_view, name="poster_url"),
    path('poster/poster_submit', views.poster_submit, name="poster_submit"),
    path('accounts/', include('allauth.urls')),
]
