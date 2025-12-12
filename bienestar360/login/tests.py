from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from login.models import Faculty
from login.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class AuthTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.faculty, self.faculty_bool = Faculty.objects.get_or_create(name="Systems Engineering")

        # These groups come from signals
        Group.objects.get_or_create(name="basic user")
        Group.objects.get_or_create(name="admin")

        # Create a test basic role (if still needed)
        self.role_basic, self.basic_role_bool = Group.objects.get_or_create(name="basic user")

        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
            email="test@example.com",
            faculty=self.faculty,
        )
        self.user.groups.add(self.role_basic)

    def test_initial_app_setup(self):
        self.assertTrue(self.faculty_bool)

    def test_login_page_loads(self):
        response = self.client.get(reverse("login:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bienvenido")

    def test_login_valid_user(self):
        credentials = {"username": "testuser", "password": "test123"}
        response = self.client.post(reverse("login:login"), credentials)
        self.assertRedirects(response, reverse("homepageUser:homepageUser"))

    def test_login_invalid_user(self):
        wrong_credentials = {"username": "wrong", "password": "wrongpass"}
        response = self.client.post(reverse("login:login"), wrong_credentials)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "usuario y contraseña correctos")

    def test_registration_page_loads(self):
        response = self.client.get(reverse("login:registration"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Crear cuenta")

    def test_register_new_user(self):
        new_user_data = {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "new@example.com",
            "faculty": self.faculty.id,
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        }

        response = self.client.post(reverse("login:registration"), new_user_data)

        self.assertRedirects(response, reverse("login:login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_password_mismatch(self):
        bad_user_data = {
            "username": "baduser",
            "first_name": "Bad",
            "last_name": "User",
            "email": "bad@example.com",
            "faculty": self.faculty.id,
            "password1": "pass1234",
            "password2": "pass5678",
        }

        response = self.client.post(reverse("login:registration"), bad_user_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "no coinciden")
        self.assertFalse(User.objects.filter(username="baduser").exists())

    def test_admin_login(self):
        # Admin created by signals
        admin_info = {
            "username": "adminuser",
            "password": "adminpass"
        }
        response = self.client.post(reverse("login:login"), admin_info)
        self.assertRedirects(response, reverse("homepageCADI:homepageCADI"))

    def test_login_user_without_group_redirects_back(self):
        user = User.objects.create_user(
            username="nogroup",
            password="12345",
            email="no@group.com"
        )
        response = self.client.post(reverse("login:login"),
                                    {"username": "nogroup", "password": "12345"})
        self.assertRedirects(response, reverse("login:login"))


    def test_signals_initial_data_created(self):
        # Faculties
        self.assertTrue(Faculty.objects.filter(name="CADI").exists())
        self.assertTrue(Faculty.objects.filter(name="Ingeniería de Sistemas").exists())

        # Groups
        self.assertTrue(Group.objects.filter(name="admin").exists())
        self.assertTrue(Group.objects.filter(name="basic user").exists())

        # Default users
        self.assertTrue(User.objects.filter(username="adminuser").exists())
        self.assertTrue(User.objects.filter(username="basicuser").exists())


    def test_model_str_representation(self):
        u = User.objects.create_user(
            username="stringtest",
            first_name="String",
            last_name="Test",
            password="123",
            faculty=self.faculty,
        )
        self.assertEqual(str(u), "String Test (stringtest)")

    def test_model_permission_and_group_helpers(self):
        group = Group.objects.create(name="tempgroup")
        content_type = ContentType.objects.get_for_model(User)

        perm = Permission.objects.create(
            codename="temp_perm",
            name="Temporary Permission",
            content_type=content_type,
        )

        user = User.objects.create_user(
            username="helperuser",
            password="123",
            faculty=self.faculty,
        )

        self.assertFalse(user.does_belong_group("tempgroup"))
        user.groups.add(group)
        self.assertTrue(user.does_belong_group("tempgroup"))

        self.assertFalse(user.has_permission("login.temp_perm"))

        user.user_permissions.add(perm)

        user = User.objects.get(pk=user.pk)

        self.assertTrue(user.has_permission("login.temp_perm"))


    def test_registration_form_valid(self):
        form = CustomUserCreationForm(data={
            "username": "formuser",
            "first_name": "Fname",
            "last_name": "Lname",
            "email": "form@example.com",
            "faculty": self.faculty.id,
            "password1": "StrongPass12345",
            "password2": "StrongPass12345",
        })
        self.assertTrue(form.is_valid())

    def test_registration_form_mismatch(self):
        form = CustomUserCreationForm(data={
            "username": "formbad",
            "first_name": "Bad",
            "last_name": "User",
            "email": "badform@example.com",
            "faculty": self.faculty.id,
            "password1": "abc123",
            "password2": "xyz789",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_auth_form_labels(self):
        form = CustomAuthenticationForm()
        self.assertEqual(form.fields["username"].label, "Usuario")
        self.assertEqual(form.fields["password"].label, "Contraseña")
