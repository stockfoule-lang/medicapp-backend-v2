# medicapp_pro_backend/users/models.py

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('pharmacien', 'Pharmacien'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='patient'
    )

    # 🔒 Version définitive sécurisée
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    is_validated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.role == 'patient':
            self.is_validated = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"