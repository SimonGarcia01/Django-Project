from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    
    # Opcional: recibir alertas
    receive_alerts = models.BooleanField(default=False)
    
    # Preferencias por tipo de actividad
    is_group_activity = models.BooleanField(default=False)
    is_individual_activity = models.BooleanField(default=False)
    
    # Categorías de interés
    is_sport = models.BooleanField(default=False)
    is_art = models.BooleanField(default=False)
    is_psychology = models.BooleanField(default=False)

    def __str__(self):
        return f"Preferencias de {self.user.username}"
