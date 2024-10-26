from django.shortcuts import render, redirect
from .models import Patient, HealthcareProvider, AnalyticsResult


def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'analytics/patient_list.html', {'patients': patients})

def provider_list(request):
    providers = HealthcareProvider.objects.all()
    return render(request, 'analytics/provider_list.html', {'providers': providers})

def analytics_results(request):
    results = AnalyticsResult.objects.all()
    return render(request, 'analytics/analytics_results.html', {'results': results})
