from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
#Users table
class CustomUser(AbstractUser):
    #Attributes

    #I was asked to add Gender
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False, blank=True)

    #Saw that there was an identification field in the seed data
    identification = models.CharField(max_length=20, null=False, blank=True, unique=False)


    #Abstract user already has: username, password, first_name, last_name, email, etc
    #So we only add the relations

    #Relations
    faculty = models.ForeignKey(
        'Faculty',
        on_delete=models.CASCADE,
        related_name="users",
        null=True
    )

    #Deleted role to use Django groups

    # How its represented
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    #Useful methods for groups (roles) and permissions (privileges)
    #Boolean that checks if the user belogns to a specific group(role)
    def does_belong_group(self, *role_names):
        return self.groups.filter(name__in=role_names).exists()

    #Boolean that checks if the user has a specific privilege
    def has_permission(self, codename):
        return self.has_perm(codename)

#Faculties table
class Faculty(models.Model):
    #Attributes
    name = models.CharField(null=False, max_length=30,unique=True)

    #How its represented
    def __str__(self):
        return self.name

#Deleted Role table to use Django groups
#Deleted Privilege table to use Django permissions