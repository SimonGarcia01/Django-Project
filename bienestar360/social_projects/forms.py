from django import forms
from .models import SocialEvent, SocialProject

class SocialEventForm(forms.ModelForm):
    class Meta:
        model = SocialEvent
        fields = ["name", "description", "location", "event_date", "project"]
        widgets = {
            "event_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "project": forms.HiddenInput(),  # 👈 Ocultamos el campo
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtenemos o creamos el proyecto social por defecto
        default_project, created = SocialProject.objects.get_or_create(
            name="Proyecto Social Universitario",
            defaults={
                'description': 'Proyecto social de la universidad',
                'is_published': True
            }
        )
        # Establecemos el valor por defecto
        self.initial['project'] = default_project
        # También podemos limitar las opciones del campo a solo este proyecto
        self.fields['project'].queryset = SocialProject.objects.filter(pk=default_project.pk)