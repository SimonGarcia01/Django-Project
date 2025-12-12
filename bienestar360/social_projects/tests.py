from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from social_projects.models import SocialProject, SocialEvent, SocialEventEnrollment
from login.models import Faculty
from datetime import date, timedelta

User = get_user_model()


class SocialProjectsViewsTestCase(TestCase):
    """Pruebas para las vistas de proyectos sociales."""

    def setUp(self):
        self.client = Client()
        
        # Crear facultad CADI
        self.cadi_faculty, _ = Faculty.objects.get_or_create(name="CADI")
        
        # Crear facultad regular
        self.regular_faculty, _ = Faculty.objects.get_or_create(name="Systems Engineering")
        
        # Crear usuario CADI
        self.cadi_user = User.objects.create_user(
            username="cadi_user",
            password="test123",
            email="cadi@example.com",
            faculty=self.cadi_faculty,
        )
        
        # Crear usuario regular
        self.regular_user = User.objects.create_user(
            username="regular_user",
            password="test123",
            email="regular@example.com",
            faculty=self.regular_faculty,
        )
        
        # Crear grupo admin (si no existe)
        Group.objects.get_or_create(name="admin")
        
        # Agregar usuario CADI al grupo admin
        admin_group = Group.objects.get(name="admin")
        self.cadi_user.groups.add(admin_group)
        
        # Crear proyecto social
        self.project = SocialProject.objects.create(
            name="Proyecto Test",
            description="Descripción del proyecto",
            is_published=True,
        )
        
        # Crear evento social
        self.event = SocialEvent.objects.create(
            project=self.project,
            name="Evento Test",
            description="Descripción del evento",
            location="Ubicación Test",
            event_date=date.today() + timedelta(days=30),
        )

    def test_social_project_home_get(self):
        """Test: Vista principal carga correctamente para usuario autenticado."""
        self.client.login(username="regular_user", password="test123")
        url = reverse("social_projects:social_project_home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Evento Test")

    def test_social_project_home_requires_login(self):
        """Test: Vista requiere autenticación."""
        url = reverse("social_projects:social_project_home")
        response = self.client.get(url)
        self.assertRedirects(response, f"/login/?next={url}")

    def test_social_project_home_post_enroll(self):
        """Test: Usuario puede inscribirse a un evento."""
        self.client.login(username="regular_user", password="test123")
        url = reverse("social_projects:social_project_home")
        
        # Verificar que no está inscrito
        self.assertFalse(
            SocialEventEnrollment.objects.filter(
                user=self.regular_user, event=self.event
            ).exists()
        )
        
        # Inscribirse
        response = self.client.post(url, {"event_id": self.event.id})
        
        # Verificar redirección
        self.assertRedirects(response, url)
        
        # Verificar que se creó la inscripción
        self.assertTrue(
            SocialEventEnrollment.objects.filter(
                user=self.regular_user, event=self.event
            ).exists()
        )

    def test_social_project_home_post_enroll_duplicate(self):
        """Test: Usuario no puede inscribirse dos veces al mismo evento."""
        self.client.login(username="regular_user", password="test123")
        url = reverse("social_projects:social_project_home")
        
        # Primera inscripción
        SocialEventEnrollment.objects.create(
            user=self.regular_user, event=self.event
        )
        
        # Intentar inscribirse de nuevo
        response = self.client.post(url, {"event_id": self.event.id})
        
        # Verificar redirección
        self.assertRedirects(response, url)
        
        # Verificar que solo hay una inscripción
        count = SocialEventEnrollment.objects.filter(
            user=self.regular_user, event=self.event
        ).count()
        self.assertEqual(count, 1)

    def test_social_project_enrollments_cadi_access(self):
        """Test: Usuario CADI puede acceder a la vista de inscripciones."""
        self.client.login(username="cadi_user", password="test123")
        url = reverse("social_projects:social_project_enrollments")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_social_project_enrollments_regular_user_denied(self):
        """Test: Usuario regular no puede acceder a la vista de inscripciones."""
        self.client.login(username="regular_user", password="test123")
        url = reverse("social_projects:social_project_enrollments")
        response = self.client.get(url)
        # Debería redirigir o dar 403
        self.assertIn(response.status_code, [302, 403])

    def test_social_project_enrollments_shows_enrollments(self):
        """Test: Vista de inscripciones muestra los usuarios inscritos."""
        self.client.login(username="cadi_user", password="test123")
        
        # Crear inscripción
        SocialEventEnrollment.objects.create(
            user=self.regular_user, event=self.event
        )
        
        url = reverse("social_projects:social_project_enrollments")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.name)

    def test_social_project_create_get(self):
        """Test: Vista de creación carga el formulario para CADI."""
        self.client.login(username="cadi_user", password="test123")
        url = reverse("social_projects:social_project_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")

    def test_social_project_create_post_valid(self):
        """Test: CADI puede crear un nuevo evento."""
        self.client.login(username="cadi_user", password="test123")
        url = reverse("social_projects:social_project_create")

        # Usar el proyecto por defecto que crea el formulario
        default_project, _ = SocialProject.objects.get_or_create(
            name="Proyecto Social Universitario",
            defaults={
                'description': 'Proyecto social de la universidad',
                'is_published': True
            }
        )

        event_data = {
            "name": "Nuevo Evento",
            "description": "Descripción del nuevo evento",
            "location": "Nueva Ubicación",
            "event_date": (date.today() + timedelta(days=60)).isoformat(),
            "project": default_project.id,
        }

        response = self.client.post(url, event_data)

        # Verificar redirección
        self.assertRedirects(response, reverse("social_projects:social_project_enrollments"))

        # Verificar que se creó el evento
        self.assertTrue(
            SocialEvent.objects.filter(name="Nuevo Evento").exists()
        )

    def test_social_project_create_regular_user_denied(self):
        """Test: Usuario regular no puede crear eventos."""
        self.client.login(username="regular_user", password="test123")
        url = reverse("social_projects:social_project_create")
        response = self.client.get(url)
        # Debería redirigir o dar 403
        self.assertIn(response.status_code, [302, 403])

    def test_is_cadi_function(self):
        """Test: Función is_cadi funciona correctamente."""
        from social_projects.views import is_cadi
        
        # Usuario CADI
        self.assertTrue(is_cadi(self.cadi_user))
        
        # Usuario regular
        self.assertFalse(is_cadi(self.regular_user))
        
        # Superusuario
        superuser = User.objects.create_superuser(
            username="superuser",
            password="test123",
            email="super@example.com"
        )
        self.assertTrue(is_cadi(superuser))


class SocialProjectsModelsTestCase(TestCase):
    """Pruebas para los modelos de proyectos sociales."""

    def setUp(self):
        self.project = SocialProject.objects.create(
            name="Proyecto Test",
            description="Descripción del proyecto",
            is_published=True,
        )
        
        self.event = SocialEvent.objects.create(
            project=self.project,
            name="Evento Test",
            description="Descripción del evento",
            location="Ubicación Test",
            event_date=date.today() + timedelta(days=30),
        )

    def test_social_project_str(self):
        """Test: Representación string del proyecto."""
        self.assertEqual(str(self.project), "Proyecto Test")

    def test_social_project_id_property(self):
        """Test: Propiedad id del proyecto."""
        self.assertEqual(self.project.id, self.project.projectId)

    def test_social_project_total_events_count(self):
        """Test: Contador de eventos del proyecto."""
        self.assertEqual(self.project.total_events_count, 1)
        
        # Crear otro evento
        SocialEvent.objects.create(
            project=self.project,
            name="Evento 2",
            description="Descripción",
            location="Ubicación",
            event_date=date.today() + timedelta(days=60),
        )
        self.assertEqual(self.project.total_events_count, 2)

    def test_social_project_total_participants_count(self):
        """Test: Contador de participantes del proyecto."""
        self.assertEqual(self.project.total_participants_count, 0)
        
        # Crear usuario e inscripción
        user = User.objects.create_user(
            username="testuser",
            password="test123",
            email="test@example.com"
        )
        SocialEventEnrollment.objects.create(user=user, event=self.event)
        
        self.assertEqual(self.project.total_participants_count, 1)

    def test_social_event_str(self):
        """Test: Representación string del evento."""
        expected = f"Evento Test - {self.event.event_date}"
        self.assertEqual(str(self.event), expected)

    def test_social_event_attendance_count(self):
        """Test: Contador de asistencia del evento."""
        self.assertEqual(self.event.attendance_count, 0)
        
        # Crear usuario e inscripción
        user = User.objects.create_user(
            username="testuser",
            password="test123",
            email="test@example.com"
        )
        SocialEventEnrollment.objects.create(user=user, event=self.event)
        
        self.assertEqual(self.event.attendance_count, 1)

    def test_social_event_enrollment_str(self):
        """Test: Representación string de la inscripción."""
        user = User.objects.create_user(
            username="testuser",
            password="test123",
            email="test@example.com"
        )
        enrollment = SocialEventEnrollment.objects.create(user=user, event=self.event)
        expected = f"testuser → Evento Test"
        self.assertEqual(str(enrollment), expected)

    def test_social_event_enrollment_unique_together(self):
        """Test: Un usuario no puede inscribirse dos veces al mismo evento."""
        user = User.objects.create_user(
            username="testuser",
            password="test123",
            email="test@example.com"
        )
        
        # Primera inscripción
        SocialEventEnrollment.objects.create(user=user, event=self.event)
        
        # Intentar segunda inscripción debería fallar
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            SocialEventEnrollment.objects.create(user=user, event=self.event)
