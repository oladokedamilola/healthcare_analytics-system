from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, BloodPressureMeasurement
from .forms import PatientForm, BloodPressureMeasurementForm

def register_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients_list')
    else:
        form = PatientForm()
    return render(request, 'patients/register_patient.html', {'form': form})


def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    measurements = patient.bp_measurements.all()
    form = BloodPressureMeasurementForm()
    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'measurements': measurements,
        'form': form
    })


def add_bp_measurement(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = BloodPressureMeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.patient = patient
            measurement.save()
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = BloodPressureMeasurementForm()
    return render(request, 'patients/add_bp_measurement.html', {'form': form, 'patient': patient})


def patient_list(request):
    patients = Patient.objects.all().order_by('name') 
    return render(request, 'patients/patient_list.html', {'patients': patients})