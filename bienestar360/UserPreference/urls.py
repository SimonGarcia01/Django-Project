from django.urls import path
from . import views

app_name = "userpreference"


urlpatterns = [
    path('setup/', views.setup_preferences, name='setup_preferences'),
]
