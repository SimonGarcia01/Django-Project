from django import forms
from .models import Tournament, Schedule, TournamentGame, Participant
from .models import Team

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = [
            'name',
            'sport',
            'gender',
            'modality',   
            'start_date',
            'max_participants',
        ]
        labels = {
            'name': 'Nombre del torneo',
            'sport': 'Deporte',
            'gender': 'Género',
            'modality': 'Modalidad',
            'start_date': 'Fecha de inicio',
            'max_participants': 'Cantidad máxima de participantes (equipos y/o individuales)',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(),
            'modality': forms.Select(), 
        }


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['date', 'start_time', 'end_time', 'capacity', 'space']
        labels = {
            'date': 'Fecha',
            'start_time': 'Hora de inicio',
            'end_time': 'Hora de finalización',
            'capacity': 'Capacidad',
            'space': 'Lugar',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class TournamentGameForm(forms.ModelForm):
    class Meta:
        model = TournamentGame
        fields = ['home_team', 'guest_team', 'home_player', 'guest_player']
        # 🔹 Eliminamos los scores del formulario de creación

    def __init__(self, *args, **kwargs):
        tournament = kwargs.pop('tournament', None)
        super().__init__(*args, **kwargs)

        if tournament:
            if tournament.modality == 'individual':
                # Oculta equipos
                self.fields['home_team'].widget = forms.HiddenInput()
                self.fields['guest_team'].widget = forms.HiddenInput()

                # Muestra solo participantes de ese torneo
                self.fields['home_player'].queryset = Participant.objects.filter(tournament=tournament)
                self.fields['guest_player'].queryset = Participant.objects.filter(tournament=tournament)

            elif tournament.modality == 'equipos':
                # Oculta jugadores individuales
                self.fields['home_player'].widget = forms.HiddenInput()
                self.fields['guest_player'].widget = forms.HiddenInput()

                # Muestra solo equipos del torneo
                self.fields['home_team'].queryset = Team.objects.filter(tournament=tournament)
                self.fields['guest_team'].queryset = Team.objects.filter(tournament=tournament)


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name']  
        labels = {
            'name': 'Nombre participante',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Nombre participante',
                'class': 'form-control'
            }),
        }






class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "members"]
        labels = {
            "name": "Nombre del equipo",
            "members": "Integrantes (separados por coma)",
        }
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Nombre del equipo",
                "class": "form-control"
            }),
            "members": forms.Textarea(attrs={
                "placeholder": "Integrantes separados por coma",
                "class": "form-control",
                "rows": 3
            }),
        }

class TournamentResultForm(forms.ModelForm):
    class Meta:
        model = TournamentGame
        fields = [
            'home_team', 'guest_team',
            'home_player', 'guest_player',
            'homeScore', 'guestScore'
        ]
        labels = {
            'home_team': 'Equipo local',
            'guest_team': 'Equipo visitante',
            'home_player': 'Participante local',
            'guest_player': 'Participante visitante',
            'homeScore': 'Marcador local',
            'guestScore': 'Marcador visitante',
        }

    def __init__(self, *args, **kwargs):
        game = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        if game and game.tournament:
            tournament = game.tournament

            if tournament.modality == 'Individual':
                self.fields['home_team'].widget = forms.HiddenInput()
                self.fields['guest_team'].widget = forms.HiddenInput()

                self.fields['home_player'].queryset = Participant.objects.filter(tournament=tournament)
                self.fields['guest_player'].queryset = Participant.objects.filter(tournament=tournament)

            elif tournament.modality == 'Equipos':
                self.fields['home_player'].widget = forms.HiddenInput()
                self.fields['guest_player'].widget = forms.HiddenInput()

                self.fields['home_team'].queryset = Team.objects.filter(tournament=tournament)
                self.fields['guest_team'].queryset = Team.objects.filter(tournament=tournament)