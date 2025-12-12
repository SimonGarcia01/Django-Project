from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from activities.models import Activity, Enrollment
from login.models import Faculty
from datetime import date, datetime

User = get_user_model()


class ReportsAndStatsViewTestCase(TestCase):
    """Pruebas para vistas de reportsAndStats."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com",
            gender="M" # Add gender for testing purposes
        )
        self.client.login(username="testuser", password="testpass123")

        # Crear datos de prueba
        self.faculty = Faculty.objects.create(name="Ingeniería")
        self.activity = Activity.objects.create(
            name="Actividad de Prueba",
            type="D",
            category="Deportiva"
        )

    def test_reports_and_stats_view_requires_login(self):
        """Test: Vista requiere autenticación."""
        self.client.logout()
        url = reverse("reportsAndStats:general_reports")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_reports_and_stats_view_loads(self):
        """Test: Vista carga correctamente."""
        url = reverse("reportsAndStats:general_reports")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reportes y Estadísticas")

    def test_filtered_reports_view_no_filter(self):
        """Test: Vista filtrada sin filtro."""
        url = reverse("reportsAndStats:filtered_reports")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_filtered_reports_view_with_filter(self):
        """Test: Vista filtrada con filtro válido."""
        url = reverse("reportsAndStats:filtered_reports")
        response = self.client.get(url, {"filter": "actividad"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "data-table")

    def test_filtered_reports_view_invalid_filter(self):
        """Test: Vista filtrada con filtro inválido."""
        url = reverse("reportsAndStats:filtered_reports")
        response = self.client.get(url, {"filter": "invalid"})
        self.assertEqual(response.status_code, 200)
        # Debería mostrar mensaje de error o datos vacíos

    def test_filtered_reports_view_with_data(self):
        """Test: Vista muestra datos cuando existen."""
        # Crear inscripción
        Enrollment.objects.create(user=self.user, activity=self.activity)

        url = reverse("reportsAndStats:filtered_reports")
        response = self.client.get(url, {"filter": "actividad"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.activity.name)

    def test_filtered_reports_view_empty_data(self):
        """Test: Vista maneja datos vacíos."""
        url = reverse("reportsAndStats:filtered_reports")
        response = self.client.get(url, {"filter": "actividad"})
        self.assertEqual(response.status_code, 200)
        # Debería mostrar "No hay datos" o tabla vacía

    def test_reports_context_variables(self):
        """Test: Vista incluye variables de contexto necesarias."""
        url = reverse("reportsAndStats:general_reports")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Verificar que el contexto tiene las variables esperadas
        self.assertIn("total_users", response.context)

    def test_filtered_reports_context_variables(self):
        """Test: Vista filtrada incluye variables de contexto."""
        url = reverse("reportsAndStats:filtered_reports")
        response = self.client.get(url, {"filter": "actividad"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.context)
        self.assertIn("selected_filter", response.context)

    def test_reports_and_stats_view_with_user_data(self):
        """Test: Vista muestra datos específicos del usuario."""
        # Crear más datos
        activity2 = Activity.objects.create(
            name="Otra Actividad",
            type="A",
            category="Artística"
        )
        Enrollment.objects.create(user=self.user, activity=activity2)

        url = reverse("reportsAndStats:general_reports")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Otra Actividad")

    def test_filtered_reports_view_faculty_filter(self):
        """Test: Vista filtrada por facultad."""
        # Crear otra facultad y usuario
        faculty2 = Faculty.objects.create(name="Medicina")
        user2 = User.objects.create_user(
            username="testuser2",
            password="testpass123",
            email="test2@example.com",
            faculty=faculty2
        )

        # Crear actividades e inscripciones
        activity2 = Activity.objects.create(
            name="Actividad Médica",
            type="M",
            category="Médica"
        )
        Enrollment.objects.create(user=self.user, activity=self.activity)
        Enrollment.objects.create(user=user2, activity=activity2)

        url = reverse("reportsAndStats:filtered_reports")
        response = self.client.get(url, {"filter": "facultad"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.context)
        # Verificar que ambas facultades aparecen en los datos
        data = response.context["data"]
        self.assertIn("Ingeniería", data)
        self.assertIn("Medicina", data)

    def test_filtered_reports_view_gender_filter(self):
        """Test: Vista filtrada por género."""
        # Crear usuarios con diferentes géneros
        user_female = User.objects.create_user(
            username="testuser_f",
            password="testpass123",
            email="testf@example.com",
            gender="F",
            faculty=self.faculty
        )
        user_male = User.objects.create_user(
            username="testuser_m",
            password="testpass123",
            email="testm@example.com",
            gender="M",
            faculty=self.faculty
        )

        # Crear inscripciones
        Enrollment.objects.create(user=user_female, activity=self.activity)
        Enrollment.objects.create(user=user_male, activity=self.activity)

        url = reverse("reportsAndStats:filtered_reports")
        response = self.client.get(url, {"filter": "genero"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.context)
        data = response.context["data"]
        # Verificar que aparecen los géneros en los datos
        self.assertTrue(any("Masculino" in key or "Femenino" in key for key in data.keys()))

    def test_filtered_reports_view_activity_filter_content(self):
        """Test: Vista filtrada por actividad muestra el contenido correcto."""
        Enrollment.objects.create(user=self.user, activity=self.activity)
        url = reverse("reportsAndStats:filtered_reports")
        response = self.client.get(url, {"filter": "actividad"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.activity.name)
        self.assertContains(response, "Deportiva")

    def test_filtered_reports_view_faculty_filter_content(self):
        """Test: Vista filtrada por facultad muestra el contenido correcto."""
        Enrollment.objects.create(user=self.user, activity=self.activity)
        url = reverse("reportsAndStats:filtered_reports")
        response = self.client.get(url, {"filter": "facultad"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.faculty.name)
        self.assertContains(response, "Ingeniería")

    def test_filtered_reports_view_gender_filter_content(self):
        """Test: Vista filtrada por género muestra el contenido correcto."""
        user_female = User.objects.create_user(
            username="testuser_f2",
            password="testpass123",
            email="testf2@example.com",
            gender="F",
            faculty=self.faculty
        )
        Enrollment.objects.create(user=user_female, activity=self.activity)
        url = reverse("reportsAndStats:filtered_reports")
        response = self.client.get(url, {"filter": "genero"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Femenino")
        self.assertContains(response, "Masculino") # Assuming there's a male user from setUp
