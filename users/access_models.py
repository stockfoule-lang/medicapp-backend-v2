# medicapp_pro_backend/users/access_models.py

from django.db import models
from django.conf import settings
from django.utils import timezone


class AccessGrant(models.Model):

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_access_grants"
    )

    pharmacist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pharmacist_access_grants"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    is_confirmed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        return (
            self.is_active
            and self.is_confirmed
            and timezone.now() < self.expires_at
        )

    def __str__(self):
        return f"{self.pharmacist} -> {self.patient}"