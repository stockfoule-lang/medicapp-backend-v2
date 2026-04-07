from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Appointment(models.Model):

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    title = models.CharField(max_length=255)

    date = models.DateField()

    time = models.TimeField()

    instructions = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.date} {self.time}"