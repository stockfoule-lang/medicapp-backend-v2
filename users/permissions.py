from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPharmacienOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        # Lecture autorisée pour utilisateur connecté
        if request.method in SAFE_METHODS:
            return True

        # Écriture uniquement pour pharmacien
        return request.user.role == "pharmacien"
