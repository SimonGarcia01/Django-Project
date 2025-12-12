from django.core.management.base import BaseCommand
from django.utils import timezone
from social_projects.models import SocialProject, SocialEvent, SocialEventEnrollment
from login.models import CustomUser
from datetime import date, datetime

class Command(BaseCommand):
    help = "Carga datos iniciales para proyectos sociales y eventos."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("🌱 Iniciando carga de datos de proyectos sociales..."))

        # ============================================================
        # 1️⃣ PROYECTO SOCIAL
        # ============================================================
        project, created = SocialProject.objects.get_or_create(
            name="Proyectos Sociales Universitarios",
            defaults={
                "description": "Proyectos de impacto social y comunitario de la universidad.",
                "is_published": True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Proyecto creado: {project.name}"))
        else:
            self.stdout.write(f"ℹ Proyecto ya existente: {project.name}")

        # ============================================================
        # 2️⃣ EVENTOS SOCIALES
        # ============================================================
        # Obtener el año actual (o el año siguiente si ya pasaron las fechas)
        today = date.today()
        current_year = today.year
        
        # Si ya pasó la fecha más temprana (12 de octubre), usar el año siguiente
        # para asegurar que ambos eventos estén en el futuro
        if today > date(current_year, 10, 12):
            current_year += 1

        eventos_data = [
            {
                "name": "Icesi Verde",
                "description": "Únete a nuestra iniciativa de sostenibilidad ambiental. Realizaremos actividades de limpieza, reciclaje y concientización sobre el cuidado del medio ambiente. Inscríbete y participa en este evento que busca hacer de nuestra universidad un lugar más sostenible.",
                "location": "Campus Universitario",
                "event_date": date(2025, 11, 9),
                "time": "10:00 AM",  # Hora incluida en la descripción
            },
            {
                "name": "Samaritanos en la Calle",
                "description": "Participa en nuestra jornada de solidaridad donde llevaremos ayuda y apoyo a las personas en situación de calle. Compartiremos alimentos, ropa y momentos de compañía. Tu participación puede hacer la diferencia en la vida de quienes más lo necesitan.",
                "location": "Centro de Cali",
                "event_date": date(2025, 10, 11),
                "time": "2:00 PM",  # Hora incluida en la descripción
            },
        ]

        eventos_creados = {}
        for evento_data in eventos_data:
            # Incluir la hora en la descripción
            description_with_time = f"{evento_data['description']}\n\nHorario: {evento_data['time']}"
            
            evento, created = SocialEvent.objects.get_or_create(
                project=project,
                name=evento_data["name"],
                defaults={
                    "description": description_with_time,
                    "location": evento_data["location"],
                    "event_date": evento_data["event_date"],
                }
            )
            eventos_creados[evento_data["name"]] = evento
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Evento creado: {evento.name} - {evento.event_date}"))
            else:
                # Si ya existe, actualizar la información
                evento.description = description_with_time
                evento.location = evento_data["location"]
                evento.event_date = evento_data["event_date"]
                evento.save()
                self.stdout.write(f"ℹ Evento actualizado: {evento.name}")

        self.stdout.write(self.style.SUCCESS("\n✅ Datos iniciales cargados exitosamente."))
        self.stdout.write(self.style.SUCCESS(f"\n📊 Resumen:"))
        self.stdout.write(f"   - Proyectos: {SocialProject.objects.count()}")
        self.stdout.write(f"   - Eventos: {SocialEvent.objects.count()}")
        self.stdout.write(f"   - Inscripciones: {SocialEventEnrollment.objects.count()}")

