from django.urls import path
from .views import login_view, search_patients, register

urlpatterns = [
    path('login/', login_view),
    path('register/', register),  # 🔥 AJOUT IMPORTANT
    path('patients/', search_patients),
]