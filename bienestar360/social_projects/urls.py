from django.urls import path
from . import views

app_name = "social_projects"  # 👈 ESTA LÍNEA ES OBLIGATORIA

urlpatterns = [
    path("", views.social_project_home, name="social_project_home"),
    path("inscritos/", views.social_project_enrollments, name="social_project_enrollments"),
    path("crear-evento/", views.social_project_create, name="social_project_create"),
]

