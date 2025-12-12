from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter
def has_group(user, group_name):
    """Verifica si un usuario pertenece a un grupo específico."""
    if user and user.is_authenticated:
        return user.groups.filter(name=group_name).exists()
    return False

@register.filter
def is_admin(user):
    """Verifica si un usuario es administrador (superuser, staff o pertenece al grupo 'admin')."""
    if not user or not user.is_authenticated:
        return False

    # Superuser o staff
    if user.is_superuser or user.is_staff:
        return True

    # Pertenece al grupo 'admin'
    return user.groups.filter(name='admin').exists()