# patient_records/models.py

from django.db import models

from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Medical history and health information
    allergies = models.TextField(blank=True, null=True)
    blood_type = models.CharField(max_length=3, blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)

    # Date of record creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.age} years old)"

class BloodPressureMeasurement(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='bp_measurements')
    systolic = models.PositiveIntegerField()
    diastolic = models.PositiveIntegerField()
    heart_rate = models.PositiveIntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)  # Automatically record the timestamp

    def __str__(self):
        return f"BP: {self.systolic}/{self.diastolic} for {self.patient.name} on {self.recorded_at.date()}"


class PatientRecord(models.Model):
    FILE_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('docx', 'Word Document'),
        ('csv', 'CSV'),
        ('other', 'Other'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='records')
    file = models.FileField(upload_to='patient_records/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, default='other')
    description = models.CharField(max_length=255, blank=True, null=True)  # Optional description
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record for {self.patient.name} - {self.file_type} ({self.uploaded_at.date()})"
