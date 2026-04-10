from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

import json

User = get_user_model()


# =========================
# REGISTER
# =========================
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return Response({"error": "JSON invalide"}, status=400)

    username = data.get("username")
    password = data.get("password")
    email = data.get("email", "")

    if not username or not password:
        return Response({"error": "Champs manquants"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Utilisateur existe déjà"}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    user.role = data.get("role", "patient")
    user.first_name = data.get("first_name", "")
    user.last_name = data.get("last_name", "")
    user.save()

    return Response({"message": "OK"})


# =========================
# LOGIN
# =========================
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return Response({"detail": "JSON invalide"}, status=400)

    username = data.get("username")
    password = data.get("password")

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"detail": "Identifiants invalides"}, status=401)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
    })


# =========================
# SAVE FCM TOKEN 🔥
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_fcm_token(request):

    user = request.user
    token = request.data.get("fcm_token")

    if not token:
        return Response({"error": "Token manquant"}, status=400)

    user.fcm_token = token
    user.save()

    print("🔥 TOKEN SAUVEGARDÉ :", token)

    return Response({"message": "Token enregistré"})


# =========================
# SEARCH PATIENTS
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_patients(request):

    query = request.GET.get("search", "")

    patients = User.objects.filter(role="patient")

    if query:
        patients = patients.filter(username__icontains=query)

    data = [
        {
            "id": p.id,
            "username": p.username,
            "first_name": p.first_name,
            "last_name": p.last_name,
        }
        for p in patients
    ]

    return Response(data)