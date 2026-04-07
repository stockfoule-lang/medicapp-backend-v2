from django.urls import path
from .views import get_treatments, add_treatment, update_treatment, delete_treatment

urlpatterns = [

    # récupérer traitements d'un patient
    path('treatments/patient/<int:patient_id>/', get_treatments),

    # ajouter traitement
    path('treatments/add/', add_treatment),

    # modifier traitement
    path('treatments/update/<int:id>/', update_treatment),

    # supprimer traitement
    path('treatments/delete/<int:id>/', delete_treatment),

]