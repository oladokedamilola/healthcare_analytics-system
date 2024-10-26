from django.contrib import admin
from .models import Patient, HealthcareProvider, AnalyticsResult

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'gender', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('gender', 'date_of_birth')
    ordering = ('last_name', 'first_name')
    list_per_page = 20

@admin.register(HealthcareProvider)
class HealthcareProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'email', 'phone_number')
    search_fields = ('name', 'specialization', 'email')
    list_filter = ('specialization',)
    ordering = ('name',)
    list_per_page = 20

@admin.register(AnalyticsResult)
class AnalyticsResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'healthcare_provider', 'analysis_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'healthcare_provider__name', 'analysis_date')
    list_filter = ('analysis_date', 'healthcare_provider')
    ordering = ('-analysis_date',)
    list_per_page = 20

