from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST'])
def login_view(request):

    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "username et password requis"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"error": "Identifiants invalides"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # récupération du rôle utilisateur
    role = getattr(user, "role", "patient")

    # normalisation pour Flutter
    role = role.lower()

    return Response({
        "id": user.id,
        "username": user.username,
        "role": role
    })


@api_view(['POST'])
def register(request):

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    role = request.data.get("role", "patient")

    if not username or not password:
        return Response(
            {"error": "username et password requis"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Utilisateur déjà existant"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    # rôle utilisateur (patient ou pharmacien)
    if hasattr(user, "role"):
        user.role = role
        user.save()

    return Response({
        "message": "Compte créé",
        "id": user.id
    })


@api_view(['GET'])
def search_patients(request):

    query = request.GET.get("search", "")

    if not query:
        return Response([])

    patients = User.objects.filter(
        username__icontains=query,
        role__iexact="patient"
    )

    data = []

    for p in patients:
        data.append({
            "id": p.id,
            "first_name": p.first_name,
            "last_name": p.last_name,
            "username": p.username,
            "public_id": getattr(p, "public_id", "")
        })

    return Response(data)