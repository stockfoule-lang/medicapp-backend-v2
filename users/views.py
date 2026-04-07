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

    # 🔥 support JSON + fallback PowerShell / Render
    try:
        data = request.data
        if not data:
            data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return Response({"error": "JSON invalide"}, status=400)

    username = data.get("username")
    password = data.get("password")
    email = data.get("email", "")

    # 🔒 Validation
    if not username or not password:
        return Response(
            {"error": "Champs manquants"},
            status=400
        )

    # 🔒 Vérifie si utilisateur existe
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Utilisateur existe déjà"},
            status=400
        )

    # 👤 Création utilisateur
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    # 🔥 Gestion rôle si présent
    if hasattr(user, "role"):
        user.role = "patient"
        user.save()

    return Response({
        "message": "Utilisateur créé avec succès"
    }, status=201)


# =========================
# LOGIN
# =========================
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):

    # 🔥 même protection JSON
    try:
        data = request.data
        if not data:
            data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return Response({"detail": "JSON invalide"}, status=400)

    username = data.get("username")
    password = data.get("password")

    # 🔒 Validation
    if not username or not password:
        return Response(
            {"detail": "Champs manquants"},
            status=400
        )

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": getattr(user, "role", "patient"),
        })

    return Response(
        {"detail": "Identifiants invalides"},
        status=401
    )


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