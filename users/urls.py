from django.urls import path
from .views import login_view, search_patients

urlpatterns = [
    path('login/', login_view),
    path('patients/', search_patients),
]