from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import date, timedelta, datetime
from login.models import Faculty
from activities.models import Activity, Schedule, Participation, ActivityType, CategoryType, WeekDay
from tournaments.models import Tournament

User = get_user_model()


class HomepageCADITestCase(TestCase):
    """Pruebas para la vista homepageCADI."""

    def setUp(self):
        self.client = Client()
        
        # Clear existing data to ensure test isolation
        Activity.objects.all().delete()
        Tournament.objects.all().delete()
        Participation.objects.all().delete()
        Schedule.objects.all().delete()
        User.objects.all().delete()
        Group.objects.all().delete()
        Faculty.objects.all().delete()

        # Crear facultad CADI
        self.cadi_faculty, _ = Faculty.objects.get_or_create(name="CADI")
        
        # Crear usuario CADI
        self.cadi_user = User.objects.create_user(
            username="cadi_user",
            password="test123",
            email="cadi@example.com",
            faculty=self.cadi_faculty,
            gender="M" # Add gender for testing purposes
        )
        
        # Crear grupo admin
        admin_group, _ = Group.objects.get_or_create(name="admin")
        self.cadi_user.groups.add(admin_group)
        
        self.client.login(username="cadi_user", password="test123")

    def test_homepage_cadi_loads(self):
        """Test: Vista homepageCADI carga correctamente."""
        url = reverse("homepageCADI:homepageCADI")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_homepage_cadi_requires_login(self):
        """Test: Vista requiere autenticación."""
        self.client.logout()
        url = reverse("homepageCADI:homepageCADI")
        response = self.client.get(url)
        self.assertRedirects(response, f"/login/?next={url}")

    
    
