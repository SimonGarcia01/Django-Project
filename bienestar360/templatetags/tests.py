from django.test import TestCase
from django.template import Template, Context
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group 
from templatetags.custom_tags import has_group, is_admin

User = get_user_model()


class TemplateTagsTestCase(TestCase):
    """Pruebas para los template tags personalizados."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
            email="test@example.com"
        )

    def test_has_group_filter(self):
        """Test: Filtro has_group funciona correctamente."""
        # Usuario sin grupo
        result = has_group(self.user, 'admin')
        self.assertFalse(result)

        # Usuario con grupo admin
        from django.contrib.auth.models import Group
        admin_group, _ = Group.objects.get_or_create(name="admin")
        self.user.groups.add(admin_group)

        result = has_group(self.user, 'admin')
        self.assertTrue(result)

    def test_is_admin_filter(self):
        """Test: Filtro is_admin funciona correctamente."""
        # Usuario regular
        result = is_admin(self.user)
        self.assertFalse(result)

        # Usuario superuser
        self.user.is_superuser = True
        self.user.save()

        result = is_admin(self.user)
        self.assertTrue(result)

        # Usuario con grupo admin
        self.user.is_superuser = False
        self.user.save()
        from django.contrib.auth.models import Group
        admin_group, _ = Group.objects.get_or_create(name="admin")
        self.user.groups.add(admin_group)

        result = is_admin(self.user)
        self.assertTrue(result)

    def test_has_group_filter_no_group(self):
        """Test: has_group con usuario sin grupo."""
        result = has_group(self.user, 'nonexistent')
        self.assertFalse(result)

    def test_has_group_filter_multiple_groups(self):
        """Test: has_group con usuario en múltiples grupos."""
        admin_group, _ = Group.objects.get_or_create(name="admin")
        other_group, _ = Group.objects.get_or_create(name="other")
        self.user.groups.add(admin_group, other_group)

        self.assertTrue(has_group(self.user, 'admin'))
        self.assertTrue(has_group(self.user, 'other'))
        self.assertFalse(has_group(self.user, 'basic user'))

    def test_has_group_filter_case_sensitive(self):
        """Test: has_group es case sensitive."""
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        self.user.groups.add(admin_group)

        self.assertTrue(has_group(self.user, 'Admin'))
        self.assertFalse(has_group(self.user, 'admin'))

    def test_is_admin_filter_staff_user(self):
        """Test: is_admin con usuario staff pero no superuser."""
        self.user.is_staff = True
        self.user.save()

        result = is_admin(self.user)
        self.assertTrue(result)  # Staff is considered admin

    def test_is_admin_filter_superuser_with_group(self):
        """Test: is_admin con superuser que también tiene grupo admin."""
        self.user.is_superuser = True
        admin_group, _ = Group.objects.get_or_create(name="admin")
        self.user.groups.add(admin_group)
        self.user.save()

        result = is_admin(self.user)
        self.assertTrue(result)

    def test_template_tags_import(self):
        """Test: Template tags se importan correctamente."""
        from templatetags.custom_tags import has_group, is_admin 
        self.assertTrue(callable(has_group)) 
        self.assertTrue(callable(is_admin))

    def test_has_group_filter_with_none_user(self):
        """Test: has_group maneja usuario None."""
        result = has_group(None, 'admin')
        self.assertFalse(result)

    def test_is_admin_filter_with_none_user(self):
        """Test: is_admin maneja usuario None."""
        result = is_admin(None)
        self.assertFalse(result)

    def test_has_group_filter_empty_string(self):
        """Test: has_group with empty string group name."""
        result = has_group(self.user, '')
        self.assertFalse(result)

    def test_has_group_filter_special_characters(self):
        """Test: has_group with group name containing special characters."""
        special_group, _ = Group.objects.get_or_create(name="group-with-dashes")
        self.user.groups.add(special_group)
        result = has_group(self.user, 'group-with-dashes')
        self.assertTrue(result)

    def test_is_admin_filter_inactive_user(self):
        """Test: is_admin with inactive user."""
        self.user.is_active = False
        self.user.save()
        result = is_admin(self.user)
        self.assertFalse(result)  # Inactive users should not be admin

    def test_is_admin_filter_superuser_with_group(self):
        """Test: is_admin with superuser who also has admin group."""
        self.user.is_superuser = True
        admin_group, _ = Group.objects.get_or_create(name="admin")
        self.user.groups.add(admin_group)
        self.user.save()
        result = is_admin(self.user)
        self.assertTrue(result)

    def test_has_group_filter_user_with_multiple_groups(self):
        """Test: has_group with user in multiple groups."""
        admin_group, _ = Group.objects.get_or_create(name="admin")
        other_group, _ = Group.objects.get_or_create(name="other")
        another_group, _ = Group.objects.get_or_create(name="another")
        self.user.groups.add(admin_group, other_group, another_group)
        self.assertTrue(has_group(self.user, 'admin'))
        self.assertTrue(has_group(self.user, 'other'))
        self.assertTrue(has_group(self.user, 'another'))
        self.assertFalse(has_group(self.user, 'nonexistent'))

    def test_has_group_filter_case_insensitive(self):
        """Test: has_group is case sensitive (confirming behavior)."""
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        self.user.groups.add(admin_group)
        self.assertTrue(has_group(self.user, 'Admin'))
        self.assertFalse(has_group(self.user, 'admin'))

    def test_template_tags_in_template_rendering(self):
        """Test: Template tags work in actual template rendering."""
        from django.template import Template, Context
        template = Template("{% load templatetags %}{% if user|has_group:'admin' %}Admin{% else %}Not Admin{% endif %}")
        context = Context({'user': self.user})
        rendered = template.render(context)
        self.assertEqual(rendered, 'Not Admin')

        # Add to admin group
        admin_group, _ = Group.objects.get_or_create(name="admin")
        self.user.groups.add(admin_group)
        context = Context({'user': self.user})
        rendered = template.render(context)
        self.assertEqual(rendered, 'Admin')
