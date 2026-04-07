from django.urls import path
from .views import search_medicament

urlpatterns = [
    path('medicaments/', search_medicament),
]