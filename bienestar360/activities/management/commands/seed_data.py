from django.core.management.base import BaseCommand
from django.utils import timezone
from activities.models import Activity, Schedule, Enrollment, ActivityReview
from login.models import CustomUser
import datetime


class Command(BaseCommand):
    help = "🌱 Seed semester activities, schedules, and test enrollments with schedules"

    def handle(self, *args, **options):
        self.stdout.write("🌱 Starting semester seeding...")

        # ============================================================
        # 1️⃣ USERS
        # ============================================================
        users_data = [
            {"username": "mariaximena", "first_name": "María Ximena", "last_name": "Narvaez Olarte", "identification": "1112343789", "email": "maria@example.com", "gender":"F"},
            {"username": "carlosdaniel", "first_name": "Carlos Daniel", "last_name": "Pérez Solarte", "identification": "1445786392", "email": "carlos@example.com", "gender":"M"},
            {"username": "juanmontenegro", "first_name": "Juan", "last_name": "Montenegro", "identification": "1123456789", "email": "juan@example.com", "gender":"M"},
            {"username": "jaimevillalobos", "first_name": "Jaime", "last_name": "Villalobos", "identification": "1978463723", "email": "jaime@example.com", "gender":"M"},
            {"username": "oscartrivino", "first_name": "Óscar", "last_name": "Triviño", "identification": "1739593012", "email": "oscar@example.com", "gender":"M"},
            {"username": "camiloforero", "first_name": "Camilo", "last_name": "Forero", "identification": "1749303184", "email": "camilo@example.com", "gender":"M"},
            {"username": "mariosinisterra", "first_name": "Mario", "last_name": "Sinisterra", "identification": "1940385178", "email": "mario@example.com", "gender":"M"},
            {"username": "felipegomez", "first_name": "Felipe", "last_name": "Gómez", "identification": "1748234111", "email": "felipe@example.com", "gender":"M"},
        ]

        users = {}
        for data in users_data:
            user, created = CustomUser.objects.get_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                    "identification": data.get("identification"),
                    "gender": data.get("gender")
                }
            )
            if created:
                user.set_password("test1234")
                user.save()
            users[data["username"]] = user

        self.stdout.write("✅ Users created successfully.")

        # ============================================================
        # 2️⃣ ACTIVITIES & SCHEDULES
        # ============================================================
        activities_data = [
            {
                "name": "Arte Fantástico",
                "description": "Explora tu imaginación a través del arte y la fantasía.",
                "category": "Grupal",
                "location": "203I",
                "type": "Artística",
                "schedules": [
                    ("Lunes", datetime.time(11, 0), datetime.time(14, 0)),
                    ("Jueves", datetime.time(11, 0), datetime.time(14, 0)),
                    ("Viernes", datetime.time(12, 0), datetime.time(15, 0)),
                ]
            },
            {
                "name": "Judo",
                "description": "Aprende técnicas de defensa personal y disciplina física.",
                "category": "Grupal",
                "location": "Coliseo 2 Zona C",
                "type": "Deportiva",
                "schedules": [
                    ("Martes", datetime.time(9, 0), datetime.time(11, 0)),
                    ("Jueves", datetime.time(10, 0), datetime.time(12, 0)),
                ]
            },
            {
                "name": "Baloncesto (Nivel Formativo)",
                "description": "Entrena fundamentos del baloncesto con espíritu de equipo.",
                "category": "Grupal",
                "location": "Coliseo 1-MU1",
                "type": "Deportiva",
                "schedules": [
                    ("Martes", datetime.time(14, 0), datetime.time(16, 0)),
                    ("Jueves", datetime.time(14, 0), datetime.time(16, 0)),
                ]
            },
            {
                "name": "Grupo de Rock",
                "description": "Participa en el grupo musical universitario de rock.",
                "category": "Grupal",
                "location": "201I",
                "type": "Artística",
                "schedules": [
                    ("Lunes", datetime.time(17, 0), datetime.time(19, 0)),
                    ("Miércoles", datetime.time(17, 0), datetime.time(19, 0)),
                ]
            },
            {
                "name": "Torneo Interno de Tenis de Mesa",
                "description": "Competencia interna de tenis de mesa en el Coliseo 2.",
                "category": "Grupal",
                "location": "Coliseo 2",
                "type": "Deportiva",
                "schedules": [
                    ("Martes", datetime.time(9, 0), datetime.time(11, 0)),
                ]
            },
        ]

        activities = {}
        for data in activities_data:
            activity, _ = Activity.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "category": data["category"],
                    "location": data["location"],
                    "is_published": True,
                    "requires_registration": True,
                    "max_capacity": 30,
                    "type": data["type"],
                },
            )
            for day, start, end in data["schedules"]:
                Schedule.objects.get_or_create(activity=activity, day=day, start_time=start, end_time=end)
            activities[data["name"]] = activity

        self.stdout.write("✅ Activities and schedules created successfully.")

        # ============================================================
        # 3️⃣ ENROLLMENTS WITH SCHEDULES
        # ============================================================
        def get_schedule(activity_name, day):
            return Schedule.objects.filter(activity__name=activity_name, day=day).first()

        # María Ximena
        enrollment, _ = Enrollment.objects.get_or_create(
            user=users["mariaximena"],
            activity=activities["Arte Fantástico"],
            defaults={"schedule": get_schedule("Arte Fantástico", "Lunes")}
        )
        if not enrollment.schedule:
            enrollment.schedule = get_schedule("Arte Fantástico", "Lunes")
            enrollment.save()
        
        enrollment, _ = Enrollment.objects.get_or_create(
            user=users["mariaximena"],
            activity=activities["Judo"],
            defaults={"schedule": get_schedule("Judo", "Martes")}
        )
        if not enrollment.schedule:
            enrollment.schedule = get_schedule("Judo", "Martes")
            enrollment.save()
        
        enrollment, _ = Enrollment.objects.get_or_create(
            user=users["mariaximena"],
            activity=activities["Baloncesto (Nivel Formativo)"],
            defaults={"schedule": get_schedule("Baloncesto (Nivel Formativo)", "Jueves")}
        )
        if not enrollment.schedule:
            enrollment.schedule = get_schedule("Baloncesto (Nivel Formativo)", "Jueves")
            enrollment.save()

        # Carlos Daniel
        enrollment, _ = Enrollment.objects.get_or_create(
            user=users["carlosdaniel"],
            activity=activities["Grupo de Rock"],
            defaults={"schedule": get_schedule("Grupo de Rock", "Lunes")}
        )
        if not enrollment.schedule:
            enrollment.schedule = get_schedule("Grupo de Rock", "Lunes")
            enrollment.save()

        # Torneo de tenis de mesa
        for username in ["juanmontenegro", "jaimevillalobos", "oscartrivino", "camiloforero", "mariosinisterra", "felipegomez"]:
            enrollment, _ = Enrollment.objects.get_or_create(
                user=users[username],
                activity=activities["Torneo Interno de Tenis de Mesa"],
                defaults={"schedule": get_schedule("Torneo Interno de Tenis de Mesa", "Martes")}
            )
            if not enrollment.schedule:
                enrollment.schedule = get_schedule("Torneo Interno de Tenis de Mesa", "Martes")
                enrollment.save()

        self.stdout.write("✅ Enrollments with schedules created successfully.")

        # ============================================================
        # 4️⃣ REVIEWS
        # ============================================================
        reviews_data = [
            (activities["Arte Fantástico"], users["mariaximena"], 5, "Me encanta esta actividad, espero la exposición final."),
            (activities["Grupo de Rock"], users["carlosdaniel"], 5, "Listo para el concierto BU – Rock & Tambores."),
        ]
        for act, usr, rating, comment in reviews_data:
            ActivityReview.objects.get_or_create(activity=act, user=usr, rating=rating, comment=comment)

        self.stdout.write(self.style.SUCCESS("⭐ Reviews added successfully."))
        self.stdout.write(self.style.SUCCESS("🌱 Semester seeding completed successfully!"))
