from django.urls import path
from .views import * 

urlpatterns = [
    path('patients/', patient_list, name='patient_list'),  # List of patients
    path('providers/', provider_list, name='provider_list'),  # List of healthcare providers
    path('analytics/results/', analytics_results, name='analytics_results'),  # View for analytics results
]
