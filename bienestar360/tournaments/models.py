from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Tournament(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('X', 'Mixto'),
    ]

    MODALITY_CHOICES = [
        ('E', 'Equipos'),
        ('I', 'Individual'),
        ('X', 'Mixto'),
    ]

    STATUS_CHOICES = [
        ('P', 'Por empezar'),
        ('I', 'En progreso'),
        ('F', 'Finalizado'),
    ]

    name = models.CharField(max_length=100)
    sport = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    modality = models.CharField(max_length=1, choices=MODALITY_CHOICES)
    start_date = models.DateField()
    max_participants = models.PositiveIntegerField(default=0)
    current_participants = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return f"{self.name} - {self.sport}"

    @property
    def progress(self):
        """Porcentaje de inscripción."""
        if self.max_participants > 0:
            return (self.current_participants / self.max_participants) * 100
        return 0

    def register_participant(self):
        """Agrega un participante si hay cupo."""
        if self.current_participants < self.max_participants:
            self.current_participants += 1
            self.save()
            return True
        return False

    def clean(self):
        """Validaciones de negocio."""
        if self.start_date and self.start_date < timezone.now().date():
            raise ValidationError("La fecha de inicio no puede estar en el pasado.")


class Schedule(models.Model):
    scheduleID = models.AutoField(primary_key=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField(default=1)
    space = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.date} {self.start_time}-{self.end_time}"

    def has_capacity(self):
        """Revisa si aún hay cupo disponible en este horario."""
        return self.capacity > self.games.count()


class Team(models.Model):
    teamId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    members = models.TextField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="teams")

    def clean(self):
        """Valida que el torneo permita equipos."""
        if self.tournament.modality == 'I':
            raise ValidationError("No se pueden registrar equipos en torneos individuales.")

    def __str__(self):
        return f"{self.name} ({self.tournament.name})"


class Participant(models.Model):
    participantId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="participants")
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="participants",
        null=True, blank=True
    )
    points = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class TournamentGame(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="games")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    home_team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="home_games"
    )
    guest_team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="guest_games"
    )
    home_player = models.ForeignKey(
        Participant, on_delete=models.SET_NULL, null=True, blank=True, related_name="home_games_as_player"
    )
    guest_player = models.ForeignKey(
        Participant, on_delete=models.SET_NULL, null=True, blank=True, related_name="guest_games_as_player"
    )
    homeScore = models.IntegerField(default=0)
    guestScore = models.IntegerField(default=0)
    played = models.BooleanField(default=False)

    def __str__(self):
        home = self.home_team or self.home_player or "?"
        guest = self.guest_team or self.guest_player or "?"
        return f"{home} vs {guest} ({self.tournament.name})"

    def clean(self):
        if not self.tournament:
            return

        if self.tournament.modality == "I":
            if self.home_player == self.guest_player:
                raise ValidationError("Un participante no puede jugar contra sí mismo.")
        else:
            if self.home_team == self.guest_team:
                raise ValidationError("Un equipo no puede jugar contra sí mismo.")

        if self.homeScore < 0 or self.guestScore < 0:
            raise ValidationError("Los puntajes no pueden ser negativos.")

    def save(self, *args, **kwargs):
        """Guarda y actualiza las estadísticas del torneo."""
        super().save(*args, **kwargs)
        self.update_standings()

    def update_standings(self):
        """Actualizar posiciones del ranking (pendiente)."""
        pass
