from django.urls import path
from . import views

urlpatterns = [
    # ===============================
    # ADMINISTRACIÓN DE ACTIVIDADES
    # ===============================
    path("new/", views.CreateActivityView.as_view(), name="create_activity"),
    path("<int:pk>/update/", views.UpdateActivityView.as_view(), name="update_activity"),
    path("<int:pk>/delete/", views.DeleteActivityView.as_view(), name="delete_activity"),

    # ===============================
    # VISTA PÚBLICA (ADMIN)
    # ===============================
    path("", views.PublicActivitiesListView.as_view(), name="public_activities"),
    path("view/", views.ActivityView.as_view(), name="activityView"),

    # ===============================
    # VISTA CADI (Retroalimentaciones)
    # ===============================
    path("cadi/reviews/", views.CADIActivityReviewView.as_view(), name="cadi_activity_review"),
    path("cadi/reviews/<int:pk>/", views.CADIActivityReviewView.as_view(), name="cadi_activity_review_detail"),
    # ruta para marcar reseñas como leídas (POST)
    path("cadi/reviews/mark_read/<int:review_id>/", views.MarkReviewReadView.as_view(), name="mark_review_read"),

    # ===============================
    # ESTUDIANTES
    # ===============================
    path("list/", views.ActivityListView.as_view(), name="activity_list"),

    # rutas específicas de actividad (es importante que estén *antes* de la ruta genérica)
    path("confirm/<str:token>/", views.ConfirmEnrollmentView.as_view(), name="confirm_enrollment"),
    path("<int:activity_id>/enroll/", views.EnrollInActivityView.as_view(), name="enroll_in_activity"),
    path("<int:pk>/review/", views.ReviewActivityView.as_view(), name="review_activity"),
    path("<int:pk>/reviews/", views.ActivityReviewsView.as_view(), name="activity_reviews"),

    # ruta genérica (detalle) al final para evitar conflictos con las anteriores
    path("<int:activity_id>/", views.ActivityDetailView.as_view(), name="activity_detail"),

    # ===============================
    # CALENDARIO DE ACTIVIDADES
    # ===============================
    path("calendar/", views.MyCalendarView.as_view(), name="my_calendar"),
    # ¡NUEVA RUTA AÑADIDA AQUÍ para eliminar actividades del calendario!
    path('calendar/unenroll/<int:enrollment_id>/', views.UnenrollFromActivityView.as_view(), name='unenroll_from_activity'),

    path("cadi/participation/", views.ParticipationSegmentationView.as_view(), name="participation_segmentation"),
    path("cadi/participation/download/excel/", views.DownloadSegmentationExcelView.as_view(), name="download_segmentation_excel"),
    path("cadi/participation/download/csv/", views.DownloadSegmentationCSVView.as_view(), name="download_segmentation_csv"),
    path("participation/register/", views.RegisterParticipationView.as_view(), name="register_participation"),
    path("participation/register/", views.RegisterParticipationView.as_view(), name="register_project_participation"),

    path("unified_calendar/", views.UnifiedCalendarView.as_view(), name="unified_calendar"),

]