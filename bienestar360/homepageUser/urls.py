
from django.urls import path
from . import views

app_name = "homepageUser"

urlpatterns = [
    path('', views.homepageUser, name='homepageUser'),

]

