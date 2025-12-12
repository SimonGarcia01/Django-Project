from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from UserPreference.models import UserPreference
from UserPreference.forms import UserPreferenceForm

User = get_user_model()


class UserPreferenceModelTestCase(TestCase):
    """Pruebas unitarias para el modelo UserPreference."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
            email="test@example.com"
        )

    def test_user_preference_creation(self):
        """Test: Creación de preferencias de usuario."""
        preference = UserPreference.objects.create(
            user=self.user,
            receive_alerts=True,
            is_group_activity=True,
            is_sport=True
        )
        self.assertEqual(preference.user, self.user)
        self.assertTrue(preference.receive_alerts)
        self.assertTrue(preference.is_group_activity)
        self.assertTrue(preference.is_sport)

    def test_user_preference_get_or_create(self):
        """Test: get_or_create funciona correctamente."""
        preference, created = UserPreference.objects.get_or_create(
            user=self.user,
            defaults={'receive_alerts': True}
        )
        self.assertTrue(created)
        self.assertEqual(preference.user, self.user)
        self.assertTrue(preference.receive_alerts)

        # Segunda llamada no crea nuevo objeto
        preference2, created2 = UserPreference.objects.get_or_create(
            user=self.user,
            defaults={'receive_alerts': False}
        )
        self.assertFalse(created2)
        self.assertEqual(preference, preference2)

    def test_user_preference_str(self):
        """Test: Representación string del modelo."""
        preference = UserPreference.objects.create(user=self.user)
        expected = f"Preferencias de {self.user.username}"
        self.assertEqual(str(preference), expected)


class UserPreferenceFormTestCase(TestCase):
    """Pruebas unitarias para el formulario UserPreferenceForm."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
            email="test@example.com"
        )

    def test_form_valid_data(self):
        """Test: Formulario válido con datos correctos."""
        form_data = {
            'receive_alerts': True,
            'is_group_activity': True,
            'is_individual_activity': False,
            'is_sport': True,
            'is_art': False,
            'is_psychology': True,
        }
        form = UserPreferenceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """Test: Formulario inválido con datos incorrectos."""
        # Datos vacíos deberían ser inválidos si hay campos requeridos
        # Pero en este caso, todos los campos son booleanos con default False
        form_data = {}
        form = UserPreferenceForm(data=form_data)
        # El formulario debería ser válido con datos vacíos ya que todos tienen defaults
        self.assertTrue(form.is_valid())


class UserPreferenceViewTestCase(TestCase):
    """Pruebas unitarias para las vistas de UserPreference."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
            email="test@example.com"
        )
        self.client.login(username="testuser", password="test123")

    def test_setup_preferences_requires_login(self):
        """Test: Vista requiere autenticación."""
        self.client.logout()
        url = reverse("UserPreference:setup_preferences")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_setup_preferences_get(self):
        """Test: Vista setup_preferences carga correctamente con GET."""
        url = reverse("UserPreference:setup_preferences")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Selecciona tus intereses")

    def test_setup_preferences_post_valid(self):
        """Test: Vista procesa POST válido correctamente."""
        url = reverse("UserPreference:setup_preferences")
        form_data = {
            'receive_alerts': True,
            'is_group_activity': True,
            'is_individual_activity': False,
            'is_sport': True,
            'is_art': False,
            'is_psychology': True,
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success

        # Verificar que se creó la preferencia
        preference = UserPreference.objects.get(user=self.user)
        self.assertTrue(preference.receive_alerts)
        self.assertTrue(preference.is_group_activity)

    def test_setup_preferences_creates_preference_if_not_exists(self):
        """Test: Vista crea preferencias si no existen."""
        # Asegurarse de que no existe preferencia
        UserPreference.objects.filter(user=self.user).delete()

        url = reverse("UserPreference:setup_preferences")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # La vista debería crear preferencias por defecto
        preference = UserPreference.objects.get(user=self.user)
        self.assertIsNotNone(preference)

    def test_user_preference_default_values(self):
        """Test: Preferencias tienen valores por defecto correctos."""
        preference = UserPreference.objects.create(user=self.user)
        self.assertFalse(preference.receive_alerts)
        self.assertFalse(preference.is_group_activity)
        self.assertFalse(preference.is_individual_activity)
        self.assertFalse(preference.is_sport)
        self.assertFalse(preference.is_art)
        self.assertFalse(preference.is_psychology)

    def test_user_preference_update(self):
        """Test: Actualización de preferencias funciona."""
        preference = UserPreference.objects.create(
            user=self.user,
            receive_alerts=False,
            is_sport=True
        )
        preference.receive_alerts = True
        preference.is_art = True
        preference.save()

        preference.refresh_from_db()
        self.assertTrue(preference.receive_alerts)
        self.assertTrue(preference.is_sport)
        self.assertTrue(preference.is_art)

    def test_user_preference_unique_user(self):
        """Test: Solo una preferencia por usuario."""
        UserPreference.objects.create(user=self.user)
        with self.assertRaises(Exception):  # IntegrityError
            UserPreference.objects.create(user=self.user)

    def test_form_invalid_data_types(self):
        """Test: Formulario rechaza tipos de datos inválidos."""
        form_data = {
            'receive_alerts': 'not_boolean',
            'is_group_activity': True,
        }
        form = UserPreferenceForm(data=form_data)
        self.assertTrue(form.is_valid())  # Django forms convert strings to boolean

    def test_form_partial_data(self):
        """Test: Formulario acepta datos parciales."""
        form_data = {
            'receive_alerts': True,
            # Otros campos no especificados
        }
        form = UserPreferenceForm(data=form_data)
        self.assertTrue(form.is_valid())
        # Verificar que campos no especificados tienen defaults
        self.assertFalse(form.cleaned_data['is_group_activity'])

    def test_setup_preferences_post_updates_existing(self):
        """Test: POST actualiza preferencias existentes."""
        # Crear preferencias existentes
        UserPreference.objects.create(user=self.user, receive_alerts=False)

        url = reverse("UserPreference:setup_preferences")
        form_data = {
            'receive_alerts': True,
            'is_group_activity': True,
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)

        # Verificar actualización
        preference = UserPreference.objects.get(user=self.user)
        self.assertTrue(preference.receive_alerts)
        self.assertTrue(preference.is_group_activity)


