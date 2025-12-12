from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from activities.models import Enrollment, Evento, Schedule
from django.utils import timezone
from UserPreference.models import UserPreference

@login_required
def homepageUser(request):
    user = request.user

    # ===========================
    # Actividades y eventos
    # ===========================
    enrollments = Enrollment.objects.filter(user=user).select_related("activity")
    actividades = [e.activity for e in enrollments]

    eventos = Evento.objects.filter(fecha__gte=timezone.now()).order_by("fecha")[:3]

    total_actividades = len(actividades)
    actividades_completadas = 0

    hoy = timezone.localtime().date()
    
    dias_espanol_ingles = {
        'Lunes': 'Monday',
        'Martes': 'Tuesday', 
        'Miércoles': 'Wednesday',
        'Jueves': 'Thursday',
        'Viernes': 'Friday',
        'Sábado': 'Saturday',
        'Domingo': 'Sunday'
    }
    
    nombre_dia_ingles = hoy.strftime("%A")  # Ej: "Saturday"
    nombre_dia = hoy.strftime("%A").capitalize()

    actividades_hoy = []
    dias_con_actividades = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    if nombre_dia_ingles in dias_con_actividades:
        dia_espanol = next((esp for esp, ing in dias_espanol_ingles.items() if ing == nombre_dia_ingles), None)
        if dia_espanol:
            actividades_hoy = [
                act for act in actividades
                if act.schedules.filter(day=dia_espanol).exists()
            ]

    # ===========================
    # Preferencias del usuario
    # ===========================
    preferences = None
    alertas_personalizadas = []
    
    if hasattr(user, 'preferences'):
        preferences = user.preferences
        # Generar alertas basadas en las preferencias REALES del usuario
        alertas_personalizadas = generar_alertas_personalizadas(user, preferences)

    # Calcular horas de participación y eventos asistidos (valores temporales)
    horas_participacion = 0
    eventos_asistidos = 0

    context = {
        "usuario": user,
        "actividades": actividades,
        "eventos": eventos,
        "total_actividades": total_actividades,
        "actividades_completadas": actividades_completadas,
        "actividades_hoy": actividades_hoy,
        "today_name": nombre_dia,
        "preferences": preferences,
        "alertas_personalizadas": alertas_personalizadas,
        "horas_participacion": horas_participacion,
        "eventos_asistidos": eventos_asistidos,
    }

    return render(request, "homepageUser/homepageUser.html", context)

def generar_alertas_personalizadas(user, preferences):
    """
    Función para generar alertas personalizadas basadas en las preferencias REALES del usuario
    """
    alertas = []
    
    # Verificar si el usuario tiene preferencias configuradas
    if not preferences:
        alertas.append("Configura tus preferencias para recibir alertas personalizadas")
        return alertas
    
    # Alertas basadas en recepción de alertas
    if not preferences.receive_alerts:
        alertas.append("Las alertas están desactivadas. Actívalas para no perderte actividades importantes")
    
    # Alertas basadas en tipo de actividad preferida
    tipo_actividad = []
    if preferences.is_group_activity:
        tipo_actividad.append("grupales")
    if preferences.is_individual_activity:
        tipo_actividad.append("individuales")
    
    if tipo_actividad:
        alertas.append(f"Te recomendamos actividades {', '.join(tipo_actividad)} que coinciden con tus preferencias")
    
    # Alertas basadas en categorías de interés
    intereses = []
    if preferences.is_sport:
        intereses.append("deportes")
    if preferences.is_art:
        intereses.append("arte")
    if preferences.is_psychology:
        intereses.append("psicología")
    
    if intereses:
        alertas.append(f"Tenemos novedades en {', '.join(intereses)} basado en tus intereses")
    
    # Alertas basadas en actividades inscritas
    actividades_inscritas = Enrollment.objects.filter(user=user).count()
    if actividades_inscritas == 0:
        alertas.append("¡Aún no te has inscrito en ninguna actividad! Explora nuestras opciones")
    elif actividades_inscritas == 1:
        alertas.append("Solo tienes 1 actividad inscrita. ¡Descubre más opciones!")
    
    # Alertas basadas en eventos próximos
    hoy = timezone.now().date()
    eventos_proximos = Evento.objects.filter(
        fecha__gte=hoy,
        fecha__lte=hoy + timezone.timedelta(days=3)
    )
    
    if eventos_proximos.exists():
        alertas.append(f"Tienes {eventos_proximos.count()} evento(s) próximo(s) esta semana")
    
    # Si no hay alertas específicas, mostrar una genérica
    if not alertas:
        alertas.append("Todo está al día. ¡Sigue participando en las actividades!")
    
    return alertas[:3]  # Limitar a 3 alertas máximo