from django.contrib import admin
from .models import Activity, Schedule, Evento

class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1  # Cuántos horarios adicionales se muestran por defecto
    min_num = 1  # Al menos un horario
    fields = ('day', 'start_time', 'end_time')
    autocomplete_fields = []
    show_change_link = True

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "type", "category", "is_published")
    list_filter = ("type", "category", "is_published")
    search_fields = ("name", "location")
    inlines = [ScheduleInline]  # <-- Aquí agregamos el inline

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "fecha", "categoria")
    list_filter = ("categoria", "fecha")
    search_fields = ("titulo", "categoria")
    date_hierarchy = "fecha"
    # Campo categoria se usa para almacenar el lugar del evento
