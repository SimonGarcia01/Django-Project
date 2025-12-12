from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

def create_initial_data(sender, **kwargs):
    from .models import Faculty, CustomUser

    with transaction.atomic():  # ensures it runs safely

        # Create faculties
        admin_faculty, _ = Faculty.objects.get_or_create(name="CADI")
        basic_faculty, _ = Faculty.objects.get_or_create(name="Ingeniería de Sistemas")

        # Create groups (roles)
        admin_group, _ = Group.objects.get_or_create(name="admin")
        basic_group, _ = Group.objects.get_or_create(name="basic user")

        ####### TEMPORARY PERMISSIONS ########
        # TEMPORARY permissions (created manually)
        permission_names = [
            "CRUD activities",
            "CRUD tournaments",
            "make reports",
            "see feedback",
            "leave feedback",
            "attend activity",
            "CRUD team",
            "join team",
            "see activities",
            "admin_homepage",
        ]

        # Create permissions under "login" app label temporarily
        content_type, _ = ContentType.objects.get_or_create(
            app_label="login",
            model="customuser"
        )

        for perm_name in permission_names:
            Permission.objects.get_or_create(
                codename=perm_name.replace(" ", "_"),
                name=perm_name,
                content_type=content_type
            )

        # Assign permissions to groups
        all_permissions = Permission.objects.filter(content_type=content_type)

        admin_group.permissions.set(all_permissions)
        basic_group.permissions.set(
            all_permissions.filter(
                codename__in=[
                    "leave_feedback",
                    "attend_activity",
                    "join_team",
                    "see_activities",
                ]
            )
        )
        ###################################

        ####### FINAL PERMISSIONS ########
        # Assign permissions to groups
        # admin_perms = Permission.objects.all()

        # basic_perms = Permission.objects.filter(
        #     codename__in=[
        #         "leave_feedback",
        #         "attend_activity",
        #         "join_team",
        #         "see_activities",
        #     ]
        # )

        # #Assign the permissions to the groups
        # admin_group.permissions.set(admin_perms)
        # basic_group.permissions.set(basic_perms)
        ###################################

        # Create basic user
        if not CustomUser.objects.filter(username="basicuser").exists():
            basicuser = CustomUser.objects.create_user(
                identification="123456789",
                username="basicuser",
                first_name="Test",
                last_name="User",
                email="ssimonggarciazz@gmail.com",
                faculty=basic_faculty,
                password="password123",
                gender="O"
            )
            basicuser.groups.add(basic_group)

        # Create admin user
        if not CustomUser.objects.filter(username="adminuser").exists():
            adminuser = CustomUser.objects.create_user(
                identification="987654321",
                username="adminuser",
                first_name="Admin",
                last_name="User",
                email="admin@example.com",
                faculty=admin_faculty,
                password="adminpass",
                gender="O",
                is_staff=True,
                is_superuser=True
            )
            adminuser.groups.add(admin_group)
