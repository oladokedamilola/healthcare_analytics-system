from django.urls import path
from . import views

app_name ="patients"

urlpatterns = [
    path('register/', views.register_patient, name='register_patient'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:patient_id>/add-measurement/', views.add_bp_measurement, name='add_bp_measurement'),
    path('patients/', views.patient_list, name='patient_list'),  # URL for the patient list

]
