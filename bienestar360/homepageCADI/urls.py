from django.urls import include, path
from . import views

app_name = "homepageCADI"

urlpatterns = [
    path('', views.homepageCADI, name='homepageCADI'),
    path('tournaments/', include('tournaments.urls')),
]