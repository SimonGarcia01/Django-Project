from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date, timedelta, datetime
import re
from activities.models import Activity, Schedule as ActivitySchedule
from tournaments.models import Tournament


def extract_event_date(description):
    """Extrae la fecha del formato FECHA:YYYY-MM-DD HH:MM"""
    if not description:
        return None
    match = re.search(r'FECHA:(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})', description)
    if match:
        try:
            fecha_str = match.group(1)
            hora_str = match.group(2)
            return datetime.strptime(f"{fecha_str} {hora_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            return None
    return None


from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden

@login_required
def homepageCADI(request):
    # Verificar si el usuario pertenece al grupo 'admin' o es superusuario
    if not request.user.is_superuser and not request.user.groups.filter(name='admin').exists():
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    today = timezone.now().date()
    now = timezone.now()

    

    return render(request, "homepageCADI/homepageCADI.html")
