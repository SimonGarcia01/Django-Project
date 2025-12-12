from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        "password_mismatch": _("Las contraseñas no coinciden."),
    }

    class Meta:
        model = CustomUser
        fields = [
            "identification",
            "username",
            "first_name",
            "last_name",
            "gender",
            "email",
            "faculty",
            "password1",
            "password2",
        ]
        labels = {
            "identification": _("Número de identificación"),
            "username": _("Usuario"),
            "first_name": _("Primer Nombre"),
            "last_name": _("Primer Apellido"),
            "gender": _("Género"),
            "email": _("Correo Electrónico"),
            "faculty": _("Facultad"),
            "password1": _("Contraseña"),
            "password2": _("Confirmar Contraseña"),   
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Traducir manualmente los labels heredados
        self.fields["password1"].label = _("Contraseña")
        self.fields["password2"].label = _("Confirmar Contraseña")


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _(
            "Por favor, introduce un nombre de usuario y contraseña correctos. "
            "Ten en cuenta que ambos campos pueden ser sensibles a mayúsculas."
        ),
        "inactive": _("Esta cuenta está inactiva."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sobrescribir etiquetas predeterminadas
        self.fields["username"].label = _("Usuario")
        self.fields["password"].label = _("Contraseña")
        self.fields["username"].widget.attrs.update({"placeholder": "Usuario"})
        self.fields["password"].widget.attrs.update({"placeholder": "Contraseña"})