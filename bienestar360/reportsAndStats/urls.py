from django.urls import path
from . import views

app_name = 'reportsAndStats'  

urlpatterns = [
    path('', views.GeneralReportsView.as_view(), name='general_reports'),
    path('filtered/', views.FilteredReportsView.as_view(), name='filtered_reports'),
    path('participation-formal-report/', views.ParticipationFormalReportView.as_view(), name='participation_formal_report'),
    path('participation-formal-report/export/', views.ParticipationReportExportView.as_view(), name='participation_report_export'),
    path('download-table-excel/', views.download_table_excel, name='download_table_excel'),
    path('download-table-csv/', views.download_table_csv, name='download_table_csv'),
]