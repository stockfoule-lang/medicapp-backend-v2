from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# =========================
# REGISTER 🔥 (NOUVEAU)
# =========================
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email", "")

    if not username or not password:
        return Response(
            {"error": "Champs manquants"},
            status=400
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Utilisateur existe déjà"},
            status=400
        )

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    # 🔥 IMPORTANT → si ton modèle a un role
    if hasattr(user, "role"):
        user.role = "patient"
        user.save()

    return Response({
        "message": "Utilisateur créé"
    })


# =========================
# LOGIN
# =========================
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

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

    return Response({"detail": "Identifiants invalides"}, status=401)


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