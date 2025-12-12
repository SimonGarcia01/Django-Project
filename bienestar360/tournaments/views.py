from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.views.generic import (
    CreateView, UpdateView, DeleteView, ListView, DetailView, 
    TemplateView, View
)
from .forms import TournamentForm, ScheduleForm, TournamentGameForm, TournamentResultForm
from .models import Tournament, Schedule, TournamentGame, Participant, Team
from .forms import ParticipantForm, TeamForm
from datetime import date, datetime, time
import calendar
from django.utils import timezone


# ==============================================================
# Helper Functions
# ==============================================================

def update_game_statuses():
    """Actualiza automáticamente el estado lógico de los partidos según la fecha y hora actual."""
    now = timezone.localtime()
    today = now.date()
    current_time = now.time()

    for game in TournamentGame.objects.select_related("schedule"):
        schedule = game.schedule

        if schedule.date < today or (schedule.date == today and schedule.end_time < current_time):
            game.status_display = "Finalizado"

        elif schedule.date == today and schedule.start_time <= current_time <= schedule.end_time:
            game.status_display = "En progreso"

        else:
            game.status_display = "Por empezar"

        game._computed_status = game.status_display


# ==============================================================
# CRUD de Torneos
# ==============================================================

class CreateTournamentView(LoginRequiredMixin, CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = "tournaments/tournament_form.html"

    def form_valid(self, form):
        # Llamar a super().form_valid() para que guarde el objeto
        response = super().form_valid(form)
        messages.success(self.request, "Torneo creado exitosamente.")
        return response
    
    def get_success_url(self):
        return reverse("tournaments:tournaments_menu")


class CreateScheduleView(LoginRequiredMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = "tournaments/schedule_form.html"

    def form_valid(self, form):
        # Llamar a super().form_valid() para que guarde el objeto
        response = super().form_valid(form)
        messages.success(self.request, "Horario creado exitosamente.")
        return response
    
    def get_success_url(self):
        return reverse("tournaments:tournaments_menu")


class CreateTournamentGameView(LoginRequiredMixin, View):
    template_name = 'tournaments/tournament_game_form.html'

    def get(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, id=tournament_id)
        game_form = TournamentGameForm(tournament=tournament)
        schedule_form = ScheduleForm()

        return render(request, self.template_name, {
            'game_form': game_form,
            'schedule_form': schedule_form,
            'tournament': tournament
        })

    def post(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, id=tournament_id)
        game_form = TournamentGameForm(request.POST, tournament=tournament)
        schedule_form = ScheduleForm(request.POST)

        if game_form.is_valid() and schedule_form.is_valid():
            schedule = schedule_form.save()
            game = game_form.save(commit=False)

            game.tournament = tournament
            game.schedule = schedule

            game.full_clean()
            game.save()
            messages.success(request, "Partido creado exitosamente.")
            return redirect('tournaments:results_menu')

        return render(request, self.template_name, {
            'game_form': game_form,
            'schedule_form': schedule_form,
            'tournament': tournament
        })


# ==============================================================
# Menús y Listas
# ==============================================================

class TournamentsMenuView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = "tournaments/tournament_view.html"
    context_object_name = "tournaments"

    def get_queryset(self):
        return Tournament.objects.all()


class TeamsMenuView(LoginRequiredMixin, ListView):
    model = Team
    template_name = "tournaments/teams_view.html"
    context_object_name = "teams"

    def get_queryset(self):
        return Team.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for team in context['teams']:
            if team.members:
                team.members_list = [m.strip() for m in team.members.split(',')]
            else:
                team.members_list = []
        return context


class ResultsMenuView(LoginRequiredMixin, TemplateView):
    template_name = "tournaments/results_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update_game_statuses()
        games = TournamentGame.objects.select_related("schedule", "tournament").all()
        now = timezone.localtime()

        visible_games = []
        for game in games:
            schedule = game.schedule
            if schedule.date < now.date() or (
                schedule.date == now.date() and schedule.end_time < now.time()
            ):
                visible_games.append(game)

        context['games'] = visible_games
        context['now'] = now
        context['is_admin'] = self.request.user.groups.filter(name='admin').exists() or self.request.user.is_superuser
        return context


class UserTournamentsResultsView(LoginRequiredMixin, TemplateView):
    """Vista de resultados de torneos para usuarios (sin botón de editar)"""
    template_name = "tournaments/user_results_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update_game_statuses()
        games = TournamentGame.objects.select_related("schedule", "tournament").all()
        now = timezone.localtime()

        visible_games = []
        for game in games:
            schedule = game.schedule
            if schedule.date < now.date() or (
                schedule.date == now.date() and schedule.end_time < now.time()
            ):
                visible_games.append(game)

        context['games'] = visible_games
        context['now'] = now
        return context


class InscriptionsMenuView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = "tournaments/inscriptions_view.html"
    context_object_name = "tournaments"

    def get_queryset(self):
        return Tournament.objects.all()


class ParticipantsMenuView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = "tournaments/participants_view.html"
    context_object_name = "tournaments"

    def get_queryset(self):
        return Tournament.objects.all()


# ==============================================================
# Inscripciones y Registro de Participantes
# ==============================================================

class RegisterParticipantView(LoginRequiredMixin, View):
    template_name = "tournaments/tournament_view.html"

    def get(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, pk=tournament_id)
        
        if tournament.modality == "I":
            form = ParticipantForm()
        else:
            form = TeamForm()

        return render(request, self.template_name, {
            "form": form,
            "tournament": tournament
        })

    def post(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, pk=tournament_id)

        if tournament.modality == "I":
            form = ParticipantForm(request.POST)
            if form.is_valid():
                participant = form.save(commit=False)
                participant.tournament = tournament
                participant.save()
                tournament.register_participant()
                messages.success(request, "Participante registrado exitosamente.")
                return redirect("tournaments:inscriptions_menu")
        else:
            team_instance = Team(tournament=tournament)
            form = TeamForm(request.POST, instance=team_instance)
            if form.is_valid():
                team = form.save()
                tournament.register_participant()
                messages.success(request, "Equipo registrado exitosamente.")
                return redirect("tournaments:inscriptions_menu")

        return render(request, self.template_name, {
            "form": form,
            "tournament": tournament
        })


class AddParticipantView(LoginRequiredMixin, View):
    template_name = "tournaments/participant_form.html"

    def get(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, pk=tournament_id)

        if tournament.current_participants >= tournament.max_participants:
            return render(request, self.template_name, {
                "tournament": tournament,
                "form": None,
                "error": "No se pueden agregar más participantes, el torneo está completo."
            })

        form = ParticipantForm()
        return render(request, self.template_name, {
            "form": form,
            "tournament": tournament
        })

    def post(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, pk=tournament_id)

        if tournament.current_participants >= tournament.max_participants:
            return render(request, self.template_name, {
                "tournament": tournament,
                "form": None,
                "error": "No se pueden agregar más participantes, el torneo está completo."
            })

        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.tournament = tournament
            participant.save()
            tournament.register_participant()
            messages.success(request, "Participante agregado exitosamente.")
            return redirect("tournaments:participants_menu")

        return render(request, self.template_name, {
            "form": form,
            "tournament": tournament
        })


class AddParticipantToTeamView(LoginRequiredMixin, View):
    template_name = "tournaments/participant_form.html"

    def get(self, request, teamId):
        team = get_object_or_404(Team, pk=teamId)
        form = ParticipantForm()
        return render(request, self.template_name, {
            "form": form,
            "team": team
        })

    def post(self, request, teamId):
        team = get_object_or_404(Team, pk=teamId)
        form = ParticipantForm(request.POST)
        
        if form.is_valid():
            participant = form.save(commit=False)
            participant.team = team
            participant.tournament = team.tournament
            participant.save()
            messages.success(request, "Participante agregado al equipo exitosamente.")
            return redirect("tournaments:teams_menu")

        return render(request, self.template_name, {
            "form": form,
            "team": team
        })


class EditParticipantView(LoginRequiredMixin, UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = "tournaments/participant_form.html"
    pk_url_kwarg = "participant_id"

    def get_success_url(self):
        messages.success(self.request, "Participante actualizado exitosamente.")
        return reverse("tournaments:participants_menu")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tournament"] = self.object.tournament
        return context


class DeleteParticipantView(LoginRequiredMixin, View):
    def post(self, request, participant_id):
        participant = get_object_or_404(Participant, pk=participant_id)
        tournament = participant.tournament
        participant.delete()
        
        if tournament.current_participants > 0:
            tournament.current_participants -= 1
            tournament.save()
        messages.success(request, "Participante eliminado exitosamente.")
        return redirect("tournaments:participants_menu")
    
    def get(self, request, participant_id):
        return self.post(request, participant_id)


class EditTeamView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = "tournaments/team_form.html"
    pk_url_kwarg = "teamId"

    def get_success_url(self):
        messages.success(self.request, "Equipo actualizado exitosamente.")
        return reverse("tournaments:teams_menu")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = self.object
        return context


class DeleteTeamView(LoginRequiredMixin, View):
    def post(self, request, teamId):
        team = get_object_or_404(Team, pk=teamId)
        team.delete()
        messages.success(request, "Equipo eliminado exitosamente.")
        return redirect("tournaments:teams_menu")
    
    def get(self, request, teamId):
        return self.post(request, teamId)


# ==============================================================
# Registro de Resultados
# ==============================================================

class RegisterResultView(LoginRequiredMixin, View):
    template_name = "tournaments/register_result_form.html"

    def get(self, request, game_id):
        game = get_object_or_404(TournamentGame, pk=game_id)
        form = TournamentResultForm(instance=game)
        return render(request, self.template_name, {
            "form": form,
            "game": game,
        })

    def post(self, request, game_id):
        game = get_object_or_404(TournamentGame, pk=game_id)
        form = TournamentResultForm(request.POST, instance=game)
        
        if 'homeScore' in request.POST and 'guestScore' in request.POST:
            game.homeScore = request.POST['homeScore']
            game.guestScore = request.POST['guestScore']
            game.played = True
            game.save()

        if form.is_valid():
            schedule = game.schedule
            now = timezone.localtime()

            if schedule.date > now.date() or (
                schedule.date == now.date() and schedule.end_time > now.time()
            ):
                messages.error(request, "No puedes registrar ni editar resultados de un partido que aún no ha finalizado.")
                return redirect('tournaments:results_menu')

            result = form.save(commit=False)
            result.homeScore = form.cleaned_data['homeScore']
            result.guestScore = form.cleaned_data['guestScore']
            result.played = True
            result.save()
            messages.success(request, "Resultado registrado exitosamente.")
            return redirect('tournaments:results_menu')

        return render(request, self.template_name, {
            "form": form,
            "game": game,
        })


# ==============================================================
# Calendario
# ==============================================================

class CalendarGeneralView(LoginRequiredMixin, TemplateView):
    template_name = "tournaments/calendar_general.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update_game_statuses()
        
        year = int(self.request.GET.get('year', date.today().year))
        month = int(self.request.GET.get('month', date.today().month))

        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdatescalendar(year, month)

        games = TournamentGame.objects.select_related(
            'tournament', 'schedule'
        ).order_by('schedule__date', 'schedule__start_time')

        # Obtener torneos que inician en este mes/año
        tournaments = Tournament.objects.filter(
            start_date__year=year,
            start_date__month=month
        )

        games_by_date = {}
        for g in games:
            game_date = g.schedule.date
            games_by_date.setdefault(game_date, []).append(g)

        # Agrupar torneos por fecha de inicio
        tournaments_by_date = {}
        for t in tournaments:
            tournaments_by_date.setdefault(t.start_date, []).append(t)

        calendar_days = []
        for week in month_days:
            for day in week:
                calendar_days.append({
                    "day": day.day,
                    "date": day,
                    "current_month": (day.month == month),
                    "games": games_by_date.get(day, []),
                    "tournaments": tournaments_by_date.get(day, []),
                })

        month_name = calendar.month_name[month]

        prev_month = month - 1
        prev_year = year
        next_month = month + 1
        next_year = year

        if prev_month < 1:
            prev_month = 12
            prev_year -= 1

        if next_month > 12:
            next_month = 1
            next_year += 1

        context.update({
            "year": year,
            "month": month,
            "month_name": month_name,
            "calendar_days": calendar_days,
            "prev_month": prev_month,
            "prev_year": prev_year,
            "next_month": next_month,
            "next_year": next_year,
        })
        return context


# ==============================================================
# Ranking
# ==============================================================

class RankingView(LoginRequiredMixin, DetailView):
    model = Tournament
    template_name = "tournaments/ranking_view.html"
    pk_url_kwarg = "tournament_id"
    context_object_name = "tournament"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.object

        if tournament.modality == "I":
            participants = Participant.objects.filter(tournament=tournament)

            if not participants.exists():
                context['message'] = "No hay participantes registrados en este torneo."
                context['ranked'] = []
            else:
                participant_stats = {}
                for participant in participants:
                    participant_stats[participant.participantId] = {
                        'participant': participant,
                        'points': 0,
                        'games_played': 0,
                        'wins': 0,
                        'draws': 0,
                        'losses': 0,
                        'goals_scored': 0,
                        'goals_conceded': 0,
                    }

                # Obtener todos los juegos jugados del torneo
                games = TournamentGame.objects.filter(
                    tournament=tournament,
                    played=True
                ).select_related('home_player', 'guest_player')

                for game in games:
                    # Estadísticas del jugador local
                    if game.home_player and game.home_player.participantId in participant_stats:
                        stats = participant_stats[game.home_player.participantId]
                        stats['games_played'] += 1
                        stats['goals_scored'] += game.homeScore
                        stats['goals_conceded'] += game.guestScore
                        if game.homeScore > game.guestScore:
                            stats['wins'] += 1
                            stats['points'] += 3
                        elif game.homeScore == game.guestScore:
                            stats['draws'] += 1
                            stats['points'] += 1
                        else:
                            stats['losses'] += 1

                    if game.guest_player and game.guest_player.participantId in participant_stats:
                        stats = participant_stats[game.guest_player.participantId]
                        stats['games_played'] += 1
                        stats['goals_scored'] += game.guestScore
                        stats['goals_conceded'] += game.homeScore
                        if game.guestScore > game.homeScore:
                            stats['wins'] += 1
                            stats['points'] += 3
                        elif game.homeScore == game.guestScore:
                            stats['draws'] += 1
                            stats['points'] += 1
                        else:
                            stats['losses'] += 1

                ranked_participants = sorted(
                    participant_stats.values(),
                    key=lambda p: (
                        -p['points'],
                        -(p['goals_scored'] - p['goals_conceded']),
                        -p['goals_scored']
                    )
                )

                ranked = []
                pos = 1
                for stats in ranked_participants:
                    goal_difference = stats['goals_scored'] - stats['goals_conceded']
                    win_percentage = (stats['wins'] / stats['games_played'] * 100) if stats['games_played'] > 0 else 0
                    
                    ranked.append({
                        "position": pos,
                        "name": stats['participant'].name,
                        "points": stats['points'],
                        "games_played": stats['games_played'],
                        "wins": stats['wins'],
                        "draws": stats['draws'],
                        "losses": stats['losses'],
                        "goals_scored": stats['goals_scored'],
                        "goals_conceded": stats['goals_conceded'],
                        "goal_difference": goal_difference,
                        "win_percentage": round(win_percentage, 1),
                    })
                    pos += 1

                context['ranked'] = ranked

        else:  # Torneo por equipos
            teams = Team.objects.filter(tournament=tournament)

            if not teams.exists():
                context['message'] = "No hay equipos registrados en este torneo."
                context['ranked'] = []
            else:
                team_stats = {}
                for team in teams:
                    team_stats[team.teamId] = {
                        'team': team,
                        'points': 0,
                        'games_played': 0,
                        'wins': 0,
                        'draws': 0,
                        'losses': 0,
                        'goals_scored': 0,
                        'goals_conceded': 0,
                    }

                # Obtener todos los juegos jugados del torneo
                games = TournamentGame.objects.filter(
                    tournament=tournament,
                    played=True
                ).select_related('home_team', 'guest_team')

                for game in games:
                    # Estadísticas del equipo local
                    if game.home_team and game.home_team.teamId in team_stats:
                        stats = team_stats[game.home_team.teamId]
                        stats['games_played'] += 1
                        stats['goals_scored'] += game.homeScore
                        stats['goals_conceded'] += game.guestScore
                        if game.homeScore > game.guestScore:
                            stats['wins'] += 1
                            stats['points'] += 3
                        elif game.homeScore == game.guestScore:
                            stats['draws'] += 1
                            stats['points'] += 1
                        else:
                            stats['losses'] += 1

                    if game.guest_team and game.guest_team.teamId in team_stats:
                        stats = team_stats[game.guest_team.teamId]
                        stats['games_played'] += 1
                        stats['goals_scored'] += game.guestScore
                        stats['goals_conceded'] += game.homeScore
                        if game.guestScore > game.homeScore:
                            stats['wins'] += 1
                            stats['points'] += 3
                        elif game.homeScore == game.guestScore:
                            stats['draws'] += 1
                            stats['points'] += 1
                        else:
                            stats['losses'] += 1

                ranked_teams = sorted(
                    team_stats.values(),
                    key=lambda t: (
                        -t['points'],
                        -(t['goals_scored'] - t['goals_conceded']),
                        -t['goals_scored']
                    )
                )

                ranked = []
                pos = 1
                for team_data in ranked_teams:
                    goal_difference = team_data['goals_scored'] - team_data['goals_conceded']
                    win_percentage = (team_data['wins'] / team_data['games_played'] * 100) if team_data['games_played'] > 0 else 0
                    
                    ranked.append({
                        "position": pos,
                        "name": team_data['team'].name,
                        "points": team_data['points'],
                        "games_played": team_data['games_played'],
                        "wins": team_data['wins'],
                        "draws": team_data['draws'],
                        "losses": team_data['losses'],
                        "goals_scored": team_data['goals_scored'],
                        "goals_conceded": team_data['goals_conceded'],
                        "goal_difference": goal_difference,
                        "win_percentage": round(win_percentage, 1),
                    })
                    pos += 1

                context['ranked'] = ranked

        return context
