from django.urls import path
from .views import get_appointments, create_appointment, delete_appointment

urlpatterns = [
    path('appointments/patient/<int:patient_id>/', get_appointments),
    path('appointments/create/', create_appointment),
    path('appointments/delete/<int:id>/', delete_appointment),
]