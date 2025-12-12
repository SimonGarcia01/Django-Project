from django.db import models
from django.conf import settings

class Activity(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    horario = models.CharField(max_length=100)
    progreso = models.IntegerField(default=0)
    estado = models.CharField(max_length=20)  # Ej: "Activo", "Inscrito", "Lista de espera"
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 🔹 Usa el CustomUser definido en settings.py
        on_delete=models.CASCADE
    )

    def _str_(self):
        return self.nombre


