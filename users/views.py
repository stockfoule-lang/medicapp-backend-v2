from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# =========================
# REGISTER
# =========================
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    data = request.data

    username = data.get("username")
    password = data.get("password")
    email = data.get("email", "")

    if not username or not password:
        return Response({"error": "Champs manquants"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Utilisateur existe déjà"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    # 🔥 Par défaut patient
    if hasattr(user, "role"):
        user.role = "patient"
        user.save()

    return Response({"message": "OK"}, status=status.HTTP_201_CREATED)


# =========================
# LOGIN
# =========================
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):

    data = request.data

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return Response({"detail": "Champs manquants"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)

        print("✅ LOGIN OK :", user.username)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": getattr(user, "role", "patient"),
        })

    print("❌ LOGIN FAILED :", username)

    return Response({"detail": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)


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


# =========================
# SAVE FCM TOKEN (VERSION FINALE)
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_fcm_token(request):

    try:
        user = request.user
        token = request.data.get("fcm_token")

        print("🔥 TOKEN REÇU BACKEND :", token)
        print("👤 USER :", user.username)

        if not token:
            return Response(
                {"error": "fcm_token requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔥 Sauvegarde sur le bon user
        user.fcm_token = token
        user.save()

        print("💾 TOKEN SAUVEGARDÉ EN DB POUR :", user.username)

        return Response({"message": "Token enregistré"}, status=status.HTTP_200_OK)

    except Exception as e:
        print("❌ ERREUR SAVE TOKEN :", str(e))
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )