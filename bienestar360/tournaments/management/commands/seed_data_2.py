from django.core.management.base import BaseCommand
from django.utils import timezone
from tournaments.models import Tournament, Schedule, Team, Participant, TournamentGame
from datetime import timedelta, time, date

class Command(BaseCommand):
    help = "Carga datos iniciales para torneos, equipos, participantes y partidos."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Iniciando carga de datos de torneos..."))

        # === 1️⃣ TORNEO DE TENIS DE MESA (Individual) ===
        today = date.today()
        
        # Torneo de Tenis de Mesa - En progreso
        tenis_mesa, created = Tournament.objects.get_or_create(
            name="Torneo Interno de Tenis de Mesa",
            defaults={
                "sport": "Tenis de Mesa",
                "gender": "M",
                "modality": "I",
                "start_date": today - timedelta(days=7),  # Empezó hace una semana
                "max_participants": 6,
                "current_participants": 0,  # Se actualizará después de crear participantes
                "status": "I",  # En progreso
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Torneo creado: {tenis_mesa.name}"))
        else:
            # Si el torneo ya existe, solo actualizar el status si es necesario
            if tenis_mesa.status != "I":
                tenis_mesa.status = "I"
                tenis_mesa.save()
            self.stdout.write(f"ℹ Torneo ya existente: {tenis_mesa.name}")

        # Participantes del torneo de tenis de mesa
        participantes_tenis_mesa = [
            {"name": "Juan Montenegro", "cc": "1123456789"},
            {"name": "Jaime Villalobos", "cc": "1978463723"},
            {"name": "Óscar Triviño", "cc": "1739593012"},
            {"name": "Camilo Forero", "cc": "1749303184"},
            {"name": "Mario Sinisterra", "cc": "1940385178"},
            {"name": "Felipe Gómez", "cc": "1748234111"},
        ]

        participantes_objs = {}
        for pdata in participantes_tenis_mesa:
            # Incluir CC en el nombre para referencia
            name_with_cc = f"{pdata['name']} CC {pdata['cc']}"
            p, created = Participant.objects.get_or_create(
                name=name_with_cc,
                tournament=tenis_mesa,
                defaults={
                    "points": 0,
                    "goals_scored": 0,
                    "goals_conceded": 0,
                }
            )
            participantes_objs[pdata['name']] = p
            if created:
                tenis_mesa.register_participant()  # Actualizar current_participants
                self.stdout.write(self.style.SUCCESS(f"✅ Participante creado: {p.name}"))
        
        # Sincronizar current_participants con el número real de participantes
        # (por si algunos ya existían y no se crearon nuevos)
        actual_count = Participant.objects.filter(tournament=tenis_mesa).count()
        tenis_mesa.current_participants = actual_count
        tenis_mesa.save()
        self.stdout.write(f"ℹ Sincronizado: {tenis_mesa.name} tiene {actual_count} participantes")

        # Crear horarios para los partidos
        schedule1, _ = Schedule.objects.get_or_create(
            date=today - timedelta(days=5),
            start_time=time(14, 0),
            end_time=time(15, 0),
            space="Sala de Tenis de Mesa",
            defaults={"capacity": 1}
        )

        schedule2, _ = Schedule.objects.get_or_create(
            date=today - timedelta(days=5),
            start_time=time(15, 0),
            end_time=time(16, 0),
            space="Sala de Tenis de Mesa",
            defaults={"capacity": 1}
        )

        schedule3, _ = Schedule.objects.get_or_create(
            date=today - timedelta(days=5),
            start_time=time(16, 0),
            end_time=time(17, 0),
            space="Sala de Tenis de Mesa",
            defaults={"capacity": 1}
        )

        schedule4, _ = Schedule.objects.get_or_create(
            date=today - timedelta(days=4),
            start_time=time(14, 0),
            end_time=time(15, 0),
            space="Sala de Tenis de Mesa",
            defaults={"capacity": 1}
        )

        schedule5, _ = Schedule.objects.get_or_create(
            date=today - timedelta(days=4),
            start_time=time(15, 0),
            end_time=time(16, 0),
            space="Sala de Tenis de Mesa",
            defaults={"capacity": 1}
        )

        schedule6, _ = Schedule.objects.get_or_create(
            date=today - timedelta(days=4),
            start_time=time(16, 0),
            end_time=time(17, 0),
            space="Sala de Tenis de Mesa",
            defaults={"capacity": 1}
        )

        # Resultados de la primera fecha
        # Juan (2) vs Camilo (1)
        game1, created = TournamentGame.objects.get_or_create(
            tournament=tenis_mesa,
            schedule=schedule1,
            home_player=participantes_objs["Juan Montenegro"],
            guest_player=participantes_objs["Camilo Forero"],
            defaults={"homeScore": 2, "guestScore": 1, "played": True}
        )
        if created:
            self._update_player_stats(participantes_objs["Juan Montenegro"], 2, 1, True)
            self._update_player_stats(participantes_objs["Camilo Forero"], 1, 2, False)
            self.stdout.write(self.style.SUCCESS("✅ Partido creado: Juan (2) vs Camilo (1)"))

        # Jaime (2) vs Óscar (0)
        game2, created = TournamentGame.objects.get_or_create(
            tournament=tenis_mesa,
            schedule=schedule2,
            home_player=participantes_objs["Jaime Villalobos"],
            guest_player=participantes_objs["Óscar Triviño"],
            defaults={"homeScore": 2, "guestScore": 0, "played": True}
        )
        if created:
            self._update_player_stats(participantes_objs["Jaime Villalobos"], 2, 0, True)
            self._update_player_stats(participantes_objs["Óscar Triviño"], 0, 2, False)
            self.stdout.write(self.style.SUCCESS("✅ Partido creado: Jaime (2) vs Óscar (0)"))

        # Mario (1) vs Felipe (2)
        game3, created = TournamentGame.objects.get_or_create(
            tournament=tenis_mesa,
            schedule=schedule3,
            home_player=participantes_objs["Mario Sinisterra"],
            guest_player=participantes_objs["Felipe Gómez"],
            defaults={"homeScore": 1, "guestScore": 2, "played": True}
        )
        if created:
            self._update_player_stats(participantes_objs["Mario Sinisterra"], 1, 2, False)
            self._update_player_stats(participantes_objs["Felipe Gómez"], 2, 1, True)
            self.stdout.write(self.style.SUCCESS("✅ Partido creado: Mario (1) vs Felipe (2)"))

        # Juan (1) vs Óscar (2)
        game4, created = TournamentGame.objects.get_or_create(
            tournament=tenis_mesa,
            schedule=schedule4,
            home_player=participantes_objs["Juan Montenegro"],
            guest_player=participantes_objs["Óscar Triviño"],
            defaults={"homeScore": 1, "guestScore": 2, "played": True}
        )
        if created:
            self._update_player_stats(participantes_objs["Juan Montenegro"], 1, 2, False)
            self._update_player_stats(participantes_objs["Óscar Triviño"], 2, 1, True)
            self.stdout.write(self.style.SUCCESS("✅ Partido creado: Juan (1) vs Óscar (2)"))

        # Camilo (1) vs Mario (2)
        game5, created = TournamentGame.objects.get_or_create(
            tournament=tenis_mesa,
            schedule=schedule5,
            home_player=participantes_objs["Camilo Forero"],
            guest_player=participantes_objs["Mario Sinisterra"],
            defaults={"homeScore": 1, "guestScore": 2, "played": True}
        )
        if created:
            self._update_player_stats(participantes_objs["Camilo Forero"], 1, 2, False)
            self._update_player_stats(participantes_objs["Mario Sinisterra"], 2, 1, True)
            self.stdout.write(self.style.SUCCESS("✅ Partido creado: Camilo (1) vs Mario (2)"))

        # Jaime (2) vs Felipe (1)
        game6, created = TournamentGame.objects.get_or_create(
            tournament=tenis_mesa,
            schedule=schedule6,
            home_player=participantes_objs["Jaime Villalobos"],
            guest_player=participantes_objs["Felipe Gómez"],
            defaults={"homeScore": 2, "guestScore": 1, "played": True}
        )
        if created:
            self._update_player_stats(participantes_objs["Jaime Villalobos"], 2, 1, True)
            self._update_player_stats(participantes_objs["Felipe Gómez"], 1, 2, False)
            self.stdout.write(self.style.SUCCESS("✅ Partido creado: Jaime (2) vs Felipe (1)"))

        # === 2️⃣ TORNEO DE FÚTBOL (Equipos) ===
        futbol, created = Tournament.objects.get_or_create(
            name="Torneo de Fútbol Mixto",
            defaults={
                "sport": "Fútbol",
                "gender": "X",
                "modality": "E",
                "start_date": today + timedelta(days=3),
                "max_participants": 8,
                "current_participants": 0,
                "status": "P",
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Torneo creado: {futbol.name}"))
        else:
            self.stdout.write(f"ℹ Torneo ya existente: {futbol.name}")

        # Equipos de fútbol
        equipos_futbol = [
            {"name": "Los Tigres", "members": "Carlos Ramírez, Andrés López, Diego Martínez, María González"},
            {"name": "Las Panteras", "members": "Laura Sánchez, Sofía Rodríguez, Marta Pérez, Juan Torres"},
        ]

        equipos_objs = []
        for equipo_data in equipos_futbol:
            equipo, created = Team.objects.get_or_create(
                name=equipo_data["name"],
                tournament=futbol,
                defaults={"members": equipo_data["members"]},
            )
            equipos_objs.append(equipo)
            if created:
                futbol.register_participant()
                self.stdout.write(self.style.SUCCESS(f"✅ Equipo creado: {equipo.name}"))
        
        # Sincronizar current_participants con el número real de equipos
        actual_count = Team.objects.filter(tournament=futbol).count()
        futbol.current_participants = actual_count
        futbol.save()
        self.stdout.write(f"ℹ Sincronizado: {futbol.name} tiene {actual_count} equipos")

        # Horario para partido de fútbol
        schedule_futbol, _ = Schedule.objects.get_or_create(
            date=today + timedelta(days=5),
            start_time=time(16, 0),
            end_time=time(17, 30),
            space="Cancha Principal",
            defaults={"capacity": 1}
        )

        # Partido de fútbol programado (sin jugar aún)
        if len(equipos_objs) >= 2:
            game_futbol, created = TournamentGame.objects.get_or_create(
                tournament=futbol,
                schedule=schedule_futbol,
                home_team=equipos_objs[0],
                guest_team=equipos_objs[1],
                defaults={"homeScore": 0, "guestScore": 0, "played": False}
            )
            if created:
                self.stdout.write(self.style.SUCCESS("⚽ Partido de fútbol programado."))

        # === 3️⃣ TORNEO DE BALONCESTO (Equipos) ===
        baloncesto, created = Tournament.objects.get_or_create(
            name="Torneo de Baloncesto Femenino",
            defaults={
                "sport": "Baloncesto",
                "gender": "F",
                "modality": "E",
                "start_date": today + timedelta(days=10),
                "max_participants": 6,
                "current_participants": 0,
                "status": "P",
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Torneo creado: {baloncesto.name}"))
        else:
            self.stdout.write(f"ℹ Torneo ya existente: {baloncesto.name}")

        # Equipos de baloncesto
        equipos_baloncesto = [
            {"name": "Las Estrellas", "members": "Ana García, Carmen López, Diana Martínez"},
            {"name": "Las Águilas", "members": "Elena Sánchez, Fernanda Torres, Gabriela Ruiz"},
        ]

        for equipo_data in equipos_baloncesto:
            equipo, created = Team.objects.get_or_create(
                name=equipo_data["name"],
                tournament=baloncesto,
                defaults={"members": equipo_data["members"]},
            )
            if created:
                baloncesto.register_participant()
                self.stdout.write(self.style.SUCCESS(f"✅ Equipo creado: {equipo.name}"))
        
        # Sincronizar current_participants con el número real de equipos
        actual_count = Team.objects.filter(tournament=baloncesto).count()
        baloncesto.current_participants = actual_count
        baloncesto.save()
        self.stdout.write(f"ℹ Sincronizado: {baloncesto.name} tiene {actual_count} equipos")

        self.stdout.write(self.style.SUCCESS("\n✅ Datos iniciales cargados exitosamente."))
        self.stdout.write(self.style.SUCCESS(f"\n📊 Resumen:"))
        self.stdout.write(f"   - Torneos: {Tournament.objects.count()}")
        self.stdout.write(f"   - Participantes: {Participant.objects.count()}")
        self.stdout.write(f"   - Equipos: {Team.objects.count()}")
        self.stdout.write(f"   - Partidos: {TournamentGame.objects.count()}")

    def _update_player_stats(self, player, goals_scored, goals_conceded, won):
        """Actualiza las estadísticas de un jugador después de un partido."""
        player.goals_scored += goals_scored
        player.goals_conceded += goals_conceded
        if won:
            player.points += 3  # Victoria = 3 puntos
        else:
            player.points += 0  # Derrota = 0 puntos
        player.save()
