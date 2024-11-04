from django import forms
from .models import Patient, BloodPressureMeasurement

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'date_of_birth', 'address', 'phone_number', 'email', 'emergency_contact_name', 'emergency_contact_number', 'allergies', 'blood_type', 'medical_conditions', 'medications']

class BloodPressureMeasurementForm(forms.ModelForm):
    class Meta:
        model = BloodPressureMeasurement
        fields = ['systolic', 'diastolic', 'heart_rate', 'notes']
