from django import forms
from .models import CustomUser, Doctor
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class DoctorRegistrationForm(forms.ModelForm):
    # Existing fields
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)  # Validates the password strength
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Ensure both passwords are entered and match
        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError("Passwords do not match.")
        else:
            raise ValidationError("Both password fields are required.")
        
        return cleaned_data

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if Doctor.objects.filter(user__first_name=first_name).exists():
            raise forms.ValidationError("This first name is already in use.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if Doctor.objects.filter(user__last_name=last_name).exists():
            raise forms.ValidationError("This last name is already in use.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        # Save CustomUser and Doctor instances
        user = CustomUser(
            username=self.cleaned_data['email'],  # Assuming email as username
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email']
        )
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()

        doctor = super().save(commit=False)
        doctor.user = user
        if commit:
            doctor.save()
        return doctor


class DoctorDetailsForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialty', 'license_number', 'phone_number', 'profile_image']

    def clean_license_number(self):
        license_number = self.cleaned_data.get('license_number')
        if Doctor.objects.filter(license_number=license_number).exists():
            raise forms.ValidationError("This license number is already in use.")
        return license_number

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone_number
