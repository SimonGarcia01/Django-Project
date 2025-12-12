from django.urls import path
from . import views


app_name = 'tournaments'

urlpatterns = [
    # ===============================
    # MENÚS Y LISTAS
    # ===============================
    path('', views.TournamentsMenuView.as_view(), name="tournaments_menu"),
    path("teams/", views.TeamsMenuView.as_view(), name="teams_menu"),
    path("results/", views.ResultsMenuView.as_view(), name="results_menu"),
    path("inscriptions/", views.InscriptionsMenuView.as_view(), name="inscriptions_menu"),
    path("participants/", views.ParticipantsMenuView.as_view(), name="participants_menu"),
    
    # ===============================
    # CREACIÓN
    # ===============================
    path('createTournament', views.CreateTournamentView.as_view(), name="create_tournament"),
    path('createSchedule', views.CreateScheduleView.as_view(), name="create_schedule"),
    path("createTournamentGame/<int:tournament_id>/", views.CreateTournamentGameView.as_view(), name="create_tournament_game"),
    
    # ===============================
    # INSCRIPCIONES Y PARTICIPANTES
    # ===============================
    path("inscriptions/register/<int:tournament_id>/", views.RegisterParticipantView.as_view(), name="register_participant"),
    path("participants/add/<int:tournament_id>/", views.AddParticipantView.as_view(), name="add_participant"),
    path("participants/edit/<int:participant_id>/", views.EditParticipantView.as_view(), name="edit_participant"),
    path("participants/delete/<int:participant_id>/", views.DeleteParticipantView.as_view(), name="delete_participant"),
    
    # ===============================
    # EQUIPOS
    # ===============================
    path("teams/edit/<int:teamId>/", views.EditTeamView.as_view(), name="edit_team"),
    path("teams/delete/<int:teamId>/", views.DeleteTeamView.as_view(), name="delete_team"),
    path("teams/<int:teamId>/add-participant/", views.AddParticipantToTeamView.as_view(), name="add_participant_to_team"),
    
    # ===============================
    # RESULTADOS Y RANKING
    # ===============================
    path("register_result/<int:game_id>/", views.RegisterResultView.as_view(), name="register_result"),
    path('ranking/<int:tournament_id>/', views.RankingView.as_view(), name='ranking_view'),
    
    # ===============================
    # CALENDARIO
    # ===============================
    path('calendar/', views.CalendarGeneralView.as_view(), name='calendar_general'),
    
    # ===============================
    # VISTA PARA USUARIOS
    # ===============================
    path('user/results/', views.UserTournamentsResultsView.as_view(), name='user_results'),

]

