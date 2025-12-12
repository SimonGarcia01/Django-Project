# userpreference/forms.py
from django import forms
from .models import UserPreference

class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = [
            'receive_alerts',
            'is_group_activity',
            'is_individual_activity',
            'is_sport',
            'is_art',
            'is_psychology',
        ]
        widgets = {
            'receive_alerts': forms.CheckboxInput(),
            'is_group_activity': forms.CheckboxInput(),
            'is_individual_activity': forms.CheckboxInput(),
            'is_sport': forms.CheckboxInput(),
            'is_art': forms.CheckboxInput(),
            'is_psychology': forms.CheckboxInput(),
        }
        labels = {
            'receive_alerts': 'Recibir alertas personalizadas',
            'is_group_activity': 'Actividades grupales',
            'is_individual_activity': 'Actividades individuales',
            'is_sport': 'Deportes',
            'is_art': 'Arte',
            'is_psychology': 'Psicología',
        }
