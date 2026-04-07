from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Treatment(models.Model):

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="treatments"
    )

    medicament_name = models.CharField(max_length=255)

    forme = models.CharField(max_length=100)

    dosage = models.IntegerField()

    matin = models.BooleanField(default=False)
    midi = models.BooleanField(default=False)
    soir = models.BooleanField(default=False)
    semaine = models.BooleanField(default=False)

    duree = models.IntegerField()

    # NOUVEAU CHAMP
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicament_name} - {self.patient}"