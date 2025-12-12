from django import forms
from .models import Activity, Schedule, WeekDay
from login.models import CustomUser

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['day', 'start_time', 'end_time']
        widgets = {
            'day': forms.Select(choices=WeekDay.choices),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            "name",
            "description",
            "category",
            "type",
            "location",
            "is_published",
            "requires_registration",
            "max_capacity",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"required": True}),
            "location": forms.TextInput(attrs={"required": True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make name and location required fields
        self.fields["name"].required = True
        self.fields["location"].required = True
        # Opcional: puedes agregar aquí validaciones, placeholders, etc.

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name or not name.strip():
            raise forms.ValidationError("El nombre de la actividad es requerido.")
        return name.strip()

    def clean_location(self):
        location = self.cleaned_data.get("location")
        if not location or not location.strip():
            raise forms.ValidationError("La ubicación de la actividad es requerida.")
        return location.strip()

    def clean(self):
        cleaned_data = super().clean()
        requires_reg = cleaned_data.get("requires_registration")
        max_cap = cleaned_data.get("max_capacity")
        if requires_reg and not max_cap:
            self.add_error("max_capacity", "Debe definir un cupo máximo si la actividad requiere inscripción.")
        if not requires_reg:
            cleaned_data["max_capacity"] = None
        return cleaned_data


class AdminAttendanceRegistrationForm(forms.Form):
    """Form for administrators to register attendance by student ID number"""
    student_identification = forms.CharField(
        label="Número de identificación del estudiante",
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 123456789',
            'autocomplete': 'off'
        })
    )
    activity = forms.ModelChoiceField(
        label="Actividad",
        queryset=Activity.objects.filter(is_published=True).order_by('name'),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    attendance_date = forms.DateField(
        label="Fecha de asistencia",
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    attendance_time = forms.TimeField(
        label="Hora de asistencia (opcional)",
        required=False,
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        })
    )

    def clean_student_identification(self):
        identification = self.cleaned_data.get('student_identification')
        if identification:
            # Try to find user by identification
            try:
                user = CustomUser.objects.get(identification=identification)
                return identification
            except CustomUser.DoesNotExist:
                raise forms.ValidationError(
                    f"No se encontró un estudiante con el número de identificación: {identification}"
                )
            except CustomUser.MultipleObjectsReturned:
                # If multiple users have the same identification, get the first one
                user = CustomUser.objects.filter(identification=identification).first()
                return identification
        return identification
