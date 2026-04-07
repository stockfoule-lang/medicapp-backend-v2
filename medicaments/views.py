from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
import os


@api_view(['GET'])
@permission_classes([AllowAny])  # ✅ REND PUBLIC
def search_medicament(request):

    query = request.GET.get('search', '').lower().strip()

    if not query:
        return Response([])

    file_path = os.path.join(settings.BASE_DIR, "CIS_bdpm.txt")

    if not os.path.exists(file_path):
        return Response({"error": "Fichier BDPM introuvable"}, status=500)

    results = []

    with open(file_path, encoding="latin-1") as file:
        for line in file:

            if "|" in line:
                parts = line.strip().split("|")
            else:
                parts = line.strip().split("\t")

            if len(parts) < 2:
                continue

            cis = parts[0] if len(parts) > 0 else ""
            nom = parts[1] if len(parts) > 1 else ""
            laboratoire = parts[5] if len(parts) > 5 else ""
            forme = parts[7] if len(parts) > 7 else ""

            if query in nom.lower():
                results.append({
                    "nom": nom,
                    "cis": cis,
                    "forme_pharmaceutique": forme,
                    "laboratoire": laboratoire,
                })

            if len(results) >= 20:
                break

    return Response(results)