from django.contrib import admin
from .models import Treatment


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):

    list_display = (
        "patient",
        "medicament_name",
        "forme",
        "dosage",
        "matin",
        "midi",
        "soir",
        "semaine",
        "duree",
        "created_at",
    )

    search_fields = (
        "patient__username",
        "medicament_name",
    )