from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


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
            "role": user.role,
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