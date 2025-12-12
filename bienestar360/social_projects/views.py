from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import SocialEvent, SocialEventEnrollment, SocialProject
from .forms import SocialEventForm

# ✅ Verifica si el usuario es CADI
def is_cadi(user):
    if user.is_superuser:
        return True
    if user.faculty and user.faculty.name == "CADI":
        return True
    return False


# 🧱 Vista principal para estudiantes (inscripción)
@login_required
def social_project_home(request):
    events = SocialEvent.objects.select_related("project").all().order_by("event_date")

    if request.method == "POST":
        event_id = request.POST.get("event_id")
        event = get_object_or_404(SocialEvent, id=event_id)

        enrollment, created = SocialEventEnrollment.objects.get_or_create(
            user=request.user,
            event=event
        )
        if created:
            messages.success(request, f"Te has inscrito al evento '{event.name}'.")
        else:
            messages.warning(request, f"Ya estás inscrito en '{event.name}'.")
        # Redirige para limpiar cola de mensajes
        return redirect("social_projects:social_project_home")

    return render(request, "social_projects/social_project_home.html", {"events": events})


# 🧾 Vista para CADI: ver inscritos por evento
@login_required
def social_project_enrollments(request):
    # Verificar si el usuario es CADI
    if not is_cadi(request.user):
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect("homepageCADI:homepageCADI")
    
    events = SocialEvent.objects.select_related("project").prefetch_related("enrollments__user").all()
    return render(request, "social_projects/social_project_enrollments.html", {"events": events})


# 🆕 Vista para CADI: crear eventos
@login_required
def social_project_create(request):
    # Verificar si el usuario es CADI
    if not is_cadi(request.user):
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect("homepageCADI:homepageCADI")
    
    if request.method == "POST":
        form = SocialEventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento creado exitosamente.")
            # Redirige a la lista de eventos de CADI
            return redirect("social_projects:social_project_enrollments")
    else:
        form = SocialEventForm()

    return render(request, "social_projects/social_project_create.html", {"form": form})
