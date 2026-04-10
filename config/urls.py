from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔐 USERS
    path('api/', include('users.urls')),

    # 📅 APPOINTMENTS
    path('api/', include('appointments.urls')),

    # 💊 (si utilisé)
    path('api/', include('medicaments.urls')),
    path('api/', include('treatments.urls')),
]