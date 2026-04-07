from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls),

    path('api/', include('users.urls')),
    path('api/', include('medicaments.urls')),
    path('api/', include('treatments.urls')),
    path('api/', include('appointments.urls')),

]