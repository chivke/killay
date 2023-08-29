from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from killay.users.lib.constants import UserConstants


class User(AbstractUser):
    """
    Default user killay.
    """

    created_at = models.DateTimeField(
        UserConstants.NAME_CREATED_AT, auto_now_add=True, null=True, blank=True
    )
    updated_at = models.DateTimeField(
        UserConstants.NAME_UPDATED_AT, auto_now=True, null=True, blank=True
    )

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["username"]

    objects = UserManager()

    def __str__(self):
        is_admin = " (admin)" if self.is_superuser else ""
        return f"{self.username}{is_admin}"
