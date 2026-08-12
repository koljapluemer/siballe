from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model so AUTH_USER_MODEL is never locked to Django's default.

    Swapping AUTH_USER_MODEL after the first migration is a painful, hard-to-change
    operation, so this thin subclass exists from migration 0001 even though it adds
    no fields yet.
    """

    email = models.EmailField("email address", blank=True, unique=True)
