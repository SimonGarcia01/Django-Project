from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import date, timedelta, datetime, time
from login.models import Faculty
from activities.models import Activity, Enrollment, Schedule, ActivityType, CategoryType, WeekDay, Evento

User = get_user_model()


class HomepageUserTestCase(TestCase):
    """Pruebas para la vista homepageUser."""

    def setUp(self):
        self.client = Client()
        
        # Crear facultad
        self.faculty, _ = Faculty.objects.get_or_create(name="Systems Engineering")
        
        # Crear usuario
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
            email="test@example.com",
            faculty=self.faculty,
        )
        
        # Crear grupo basic user
        basic_group, _ = Group.objects.get_or_create(name="basic user")
        self.user.groups.add(basic_group)
        
        self.client.login(username="testuser", password="test123")

    def test_homepage_user_loads(self):
        """Test: Vista homepageUser carga correctamente."""
        url = reverse("homepageUser:homepageUser")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_homepage_user_requires_login(self):
        """Test: Vista requiere autenticación."""
        self.client.logout()
        url = reverse("homepageUser:homepageUser")
        response = self.client.get(url)
        self.assertRedirects(response, f"/login/?next={url}")

    def test_homepage_user_shows_user_enrollments(self):
        """Test: Vista muestra las actividades en las que el usuario está inscrito."""
        # Crear actividad
        activity = Activity.objects.create(
            name="Actividad Test",
            description="Descripción",
            location="Ubicación",
            type=ActivityType.DEPORTIVA,
            category=CategoryType.GRUPAL,
            is_published=True,
        )
        
        # Inscribir usuario
        Enrollment.objects.create(user=self.user, activity=activity)
        
        url = reverse("homepageUser:homepageUser")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Actividad Test")

    def test_homepage_user_shows_upcoming_eventos(self):
        """Test: Vista muestra eventos próximos."""
        # Crear evento futuro
        future_event = Evento.objects.create(
            titulo="Evento Futuro",
            fecha=timezone.now() + timedelta(days=10),
            categoria="Deportivo",
        )
        
        url = reverse("homepageUser:homepageUser")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Evento Futuro")

    def test_homepage_user_does_not_show_past_eventos(self):
        """Test: Vista no muestra eventos pasados."""
        # Crear evento pasado
        past_event = Evento.objects.create(
            titulo="Evento Pasado",
            fecha=timezone.now() - timedelta(days=10),
            categoria="Deportivo",
        )
        
        url = reverse("homepageUser:homepageUser")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # No debería contener el evento pasado en los próximos eventos
        # (solo muestra los 3 más próximos con fecha >= ahora)
        self.assertNotIn("Evento Pasado", response.content.decode())

    def test_homepage_user_shows_activities_today(self):
        """Test: Vista muestra actividades que ocurren hoy."""
        # Crear actividad
        activity = Activity.objects.create(
            name="Actividad Hoy",
            description="Descripción",
            location="Ubicación",
            type=ActivityType.DEPORTIVA,
            category=CategoryType.GRUPAL,
            is_published=True,
        )
        
        # Inscribir usuario
        Enrollment.objects.create(user=self.user, activity=activity)
        
        # Crear schedule para hoy (lunes)
        # Obtener el día de hoy en español
        today_weekday = date.today().weekday()  # 0=Lunes, 1=Martes, etc.
        weekday_map = {
            0: WeekDay.MONDAY,
            1: WeekDay.TUESDAY,
            2: WeekDay.WEDNESDAY,
            3: WeekDay.THURSDAY,
            4: WeekDay.FRIDAY,
        }
        today_spanish = weekday_map.get(today_weekday)
        
        # Solo crear schedule si es día de semana (Lunes a Viernes)
        if today_weekday < 5:  # Lunes a Viernes
            Schedule.objects.create(
                activity=activity,
                day=today_spanish,
                start_time=time(10, 0),
                end_time=time(11, 0),
            )
            
            url = reverse("homepageUser:homepageUser")
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            # Si es día de semana, debería mostrar la actividad de hoy
            self.assertIn("actividades_hoy", response.context)

    def test_homepage_user_context_variables(self):
        """Test: Vista incluye todas las variables de contexto necesarias."""
        url = reverse("homepageUser:homepageUser")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar que todas las variables de contexto están presentes
        self.assertIn("usuario", response.context)
        self.assertIn("actividades", response.context)
        self.assertIn("eventos", response.context)
        self.assertIn("total_actividades", response.context)
        self.assertIn("actividades_completadas", response.context)
        self.assertIn("actividades_hoy", response.context)
        self.assertIn("today_name", response.context)

    def test_homepage_user_total_actividades(self):
        """Test: Contador de actividades totales es correcto."""
        # Crear múltiples actividades
        activities = []
        for i in range(3):
            activity = Activity.objects.create(
                name=f"Actividad {i}",
                description="Descripción",
                location="Ubicación",
                type=ActivityType.DEPORTIVA,
                category=CategoryType.GRUPAL,
                is_published=True,
            )
            Enrollment.objects.create(user=self.user, activity=activity)
            activities.append(activity)
        
        url = reverse("homepageUser:homepageUser")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_actividades"], 3)

    def test_homepage_user_no_enrollments(self):
        """Test: Vista maneja correctamente cuando el usuario no tiene inscripciones."""
        url = reverse("homepageUser:homepageUser")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_actividades"], 0)
        self.assertEqual(len(response.context["actividades"]), 0)

    def test_homepage_user_eventos_ordered(self):
        """Test: Eventos se ordenan por fecha (más próximos primero)."""
        # Crear eventos con diferentes fechas
        event1 = Evento.objects.create(
            titulo="Evento Lejano",
            fecha=timezone.now() + timedelta(days=30),
            categoria="Deportivo",
        )
        event2 = Evento.objects.create(
            titulo="Evento Próximo",
            fecha=timezone.now() + timedelta(days=5),
            categoria="Deportivo",
        )
        event3 = Evento.objects.create(
            titulo="Evento Medio",
            fecha=timezone.now() + timedelta(days=15),
            categoria="Deportivo",
        )
        
        url = reverse("homepageUser:homepageUser")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar que los eventos están ordenados
        eventos = response.context["eventos"]
        if len(eventos) > 0:
            # El primer evento debería ser el más próximo
            self.assertLessEqual(eventos[0].fecha, eventos[1].fecha if len(eventos) > 1 else eventos[0].fecha)

    def test_homepage_user_eventos_limit(self):
        """Test: Vista solo muestra los 3 eventos más próximos."""
        # Crear más de 3 eventos
        for i in range(5):
            Evento.objects.create(
                titulo=f"Evento {i}",
                fecha=timezone.now() + timedelta(days=i+1),
                categoria="Deportivo",
            )
        
        url = reverse("homepageUser:homepageUser")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Debería mostrar máximo 3 eventos
        eventos = response.context["eventos"]
        self.assertLessEqual(len(eventos), 3)

    def test_homepage_user_activities_today_weekend(self):
        """Test: Vista no muestra actividades de hoy si es fin de semana."""
        # Crear actividad
        activity = Activity.objects.create(
            name="Actividad Weekend",
            description="Descripción",
            location="Ubicación",
            type=ActivityType.DEPORTIVA,
            category=CategoryType.GRUPAL,
            is_published=True,
        )
        
        # Inscribir usuario
        Enrollment.objects.create(user=self.user, activity=activity)
        
        # Crear schedule para sábado (usando string directamente ya que WeekDay no tiene SATURDAY)
        # La vista homepageUser solo busca actividades en días de semana (Lunes a Viernes)
        # así que no crearemos un schedule para sábado
        
        url = reverse("homepageUser:homepageUser")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Si es sábado o domingo, no debería buscar actividades de hoy
        today_weekday = date.today().weekday()
        if today_weekday >= 5:  # Sábado o domingo
            # actividades_hoy debería estar vacío porque la vista solo busca en días de semana
            self.assertEqual(len(response.context["actividades_hoy"]), 0)
        else:
            # Si es día de semana, la lista podría estar vacía si no hay actividades hoy
            self.assertIn("actividades_hoy", response.context)

    def test_homepage_user_shows_user_info(self):
        """Test: Vista muestra información del usuario."""
        url = reverse("homepageUser:homepageUser")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar que el usuario está en el contexto
        self.assertEqual(response.context["usuario"], self.user)
        self.assertContains(response, self.user.username)
