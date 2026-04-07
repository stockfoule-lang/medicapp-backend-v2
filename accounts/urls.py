from django.urls import path
from .views import login_view, search_patients, register

urlpatterns = [
    path('login/', login_view),
    path('patients/', search_patients),
    path('register/', register),
]