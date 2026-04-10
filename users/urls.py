from django.urls import path
from .views import login_view, register, search_patients, save_fcm_token

urlpatterns = [
    path('login/', login_view),
    path('register/', register),
    path('patients/', search_patients),
    path('save-fcm-token/', save_fcm_token),
]