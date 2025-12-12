from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from login.models import CustomUser


# ==============================================================
# ENUMS / CHOICES
# ==============================================================

class ActivityType(models.TextChoices):
    DEPORTIVA = "Deportiva", "Deportiva"
    ARTISTICA = "Artística", "Artística"
    EVENTOS = "Eventos", "Eventos"


class CategoryType(models.TextChoices):
    GRUPAL = "Grupal", "Grupal"
    INDIVIDUAL = "Individual", "Individual"


class WeekDay(models.TextChoices):
    MONDAY = "Lunes", "Lunes"
    TUESDAY = "Martes", "Martes"
    WEDNESDAY = "Miércoles", "Miércoles"
    THURSDAY = "Jueves", "Jueves"
    FRIDAY = "Viernes", "Viernes"
    # Puedes agregar más días si lo necesitas


# ==============================================================
# MODELO PRINCIPAL: ACTIVIDAD
# ==============================================================

class Activity(models.Model):
    """
    Representa una actividad publicada o administrada dentro del sistema.
    """
    activityId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(default="Actividad sin descripción")
    location = models.CharField(max_length=200, default="Ubicación por definir")
    type = models.CharField(max_length=20, choices=ActivityType.choices, null=True, blank=True, default=ActivityType.DEPORTIVA)
    category = models.CharField(max_length=20, choices=CategoryType.choices, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    requires_registration = models.BooleanField(default=False)
    max_capacity = models.PositiveIntegerField(null=True, blank=True)

    participants = models.ManyToManyField(
        CustomUser,
        through="Enrollment",
        related_name="activities"
    )

    def __str__(self):
        return f"{self.name} ({self.type}, {self.category})"

    # ----------------------------------------------------------
    # Propiedades útiles
    # ----------------------------------------------------------

    @property
    def id(self):
        """
        Alias para `activityId` para compatibilidad con Django.
        Permite usar `activity.id` en lugar de `activity.activityId`
        en templates y URLs sin romper nada.
        """
        return self.activityId

    @property
    def current_registrations_count(self):
        """Devuelve el número actual de inscripciones."""
        return self.enrollments.count()

    @property
    def is_full_status(self):
        """Indica si el cupo máximo fue alcanzado."""
        if self.requires_registration and self.max_capacity:
            return self.current_registrations_count >= self.max_capacity
        return False


# ==============================================================
# HORARIOS DE ACTIVIDADES
# ==============================================================

class Schedule(models.Model):
    """
    Define los horarios asociados a una actividad (día y hora).
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="schedules")
    day = models.CharField(max_length=10, choices=WeekDay.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.activity.name} - {self.day} ({self.start_time} - {self.end_time})"

# ==============================================================
# INSCRIPCIÓN A ACTIVIDADES
# ==============================================================

class Enrollment(models.Model):
    """
    Representa la inscripción de un usuario a una actividad.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="enrollments")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="enrollments")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    # To mark the confirmation status from the email
    confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "activity", "schedule")  # Allow multiple enrollments with different schedules

    def __str__(self):
        return f"{self.user.username} en {self.activity.name}"

    def confirm(self):
        """Marca la inscripción como confirmada y guarda la fecha."""
        self.confirmed = True
        self.confirmed_at = now()
        self.save()



# ==============================================================
# RESEÑAS DE ACTIVIDADES
# ==============================================================

class ActivityReview(models.Model):
    """
    Reseñas enviadas por los estudiantes sobre las actividades.
    Incluye un campo `is_read` para marcar si un administrador ya la revisó.
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Reseña de {self.user} para {self.activity.name} ({self.rating}⭐)"


class Participation(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True, blank=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    attendance_date = models.DateField(null=True, blank=True)  # <-- nuevo
    attendance_time = models.TimeField(null=True, blank=True)  # <-- opcional

    class Meta:
        unique_together = ("user", "activity", "attendance_date")  # evita duplicados
        verbose_name = "Participación"
        verbose_name_plural = "Participaciones"

    def __str__(self):
        return f"{self.user.username} → {self.activity.name}"
    

class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    categoria = models.CharField(max_length=50)

    def _str_(self):
        return self.titulo