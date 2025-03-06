import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    class RoleChoices(models.TextChoices):
        USER = 'user'
        LIBRARIAN = 'librarian'
        ADMIN = 'admin'

    user_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True, db_index=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=10, choices=RoleChoices.choices, default=RoleChoices.USER)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name']

    objects = UserManager()

    def __str__(self):
        return self.username