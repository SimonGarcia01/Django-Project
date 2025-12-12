from django.db import models
from django.utils.timezone import now
from login.models import CustomUser


class SocialProject(models.Model):
    projectId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, default="Proyecto Social Universitario")
    description = models.TextField(default="Proyecto social de la universidad")
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def id(self):
        return self.projectId

    @property
    def total_participants_count(self):
        return CustomUser.objects.filter(
            social_event_enrollments__event__project=self
        ).distinct().count()

    @property
    def total_events_count(self):
        return self.events.count()


class SocialEvent(models.Model):
    project = models.ForeignKey(
        SocialProject, on_delete=models.CASCADE, related_name="events"
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    event_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.event_date}"

    @property
    def attendance_count(self):
        return self.enrollments.count()


class SocialEventEnrollment(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="social_event_enrollments"
    )
    event = models.ForeignKey(
        SocialEvent, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=True)
    confirmed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")
        verbose_name = "Inscripción/Asistencia a evento"
        verbose_name_plural = "Inscripciones/Asistencias a eventos"

    def __str__(self):
        return f"{self.user.username} → {self.event.name}"

    def save(self, *args, **kwargs):
        if not self.confirmed_at and self.confirmed:
            self.confirmed_at = now()
        super().save(*args, **kwargs)