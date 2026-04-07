from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Traitement

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "role")

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        role = validated_data["role"]

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            role=role
        )

        return user


class TraitementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traitement
        fields = "__all__"
