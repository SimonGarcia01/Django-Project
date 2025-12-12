from django.urls import path
from .views import LoginView, RegisterView

app_name = "login"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegisterView.as_view(), name='registration'),
]
