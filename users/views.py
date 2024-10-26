from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import *
from .models import *
from django_ratelimit.decorators import ratelimit
from .utils import *
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


def register_doctor(request):
    print("Debug: register_doctor called with request method:", request.method)
    
    if request.method == 'POST':
        print("Debug: Processing POST request")
        form = DoctorRegistrationForm(request.POST)
        
        if form.is_valid():
            print("Debug: Form is valid, saving user...")
            user = CustomUser(
                username=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
            )
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # Deactivate until email verification
            user.save()
            print("Debug: User saved with email:", user.email)

            # Send verification email
            send_verification_email(request, user)
            print("Debug: Verification email sent to:", user.email)
            
            messages.success(request, 'Registration successful! Check your email to activate your account.')
            return redirect('account_activation_sent')
        else:
            print("Debug: Form is invalid. Errors:", form.errors)
            messages.error(request, 'Registration failed. Please check the form for errors.')
    else:
        print("Debug: Processing GET request for registration form")
        form = DoctorRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('users:complete_doctor_registration')
    else:
        messages.error(request, 'The activation link is invalid or has expired.')
        return redirect('register')


def complete_doctor_registration(request, user_id):
    print("Debug: complete_doctor_registration called for user ID:", user_id)
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = DoctorDetailsForm(request.POST, request.FILES)  # Include request.FILES for image upload
        if form.is_valid():
            doctor = Doctor(
                user=user,
                specialty=form.cleaned_data['specialty'],
                license_number=form.cleaned_data['license_number'],
                phone_number=form.cleaned_data['phone_number'],
                profile_image=form.cleaned_data['profile_image']
            )
            doctor.save()
            print("Debug: Doctor details saved. Specialty:", doctor.specialty)
            login(request, user)
            messages.success(request, 'Doctor registration completed successfully!')
            return redirect('home')  
        else:
            print("Debug: Form is invalid. Errors:", form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DoctorDetailsForm()

    return render(request, 'users/doctor_details.html', {'form': form, 'user': user})


# User Login
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Send OTP email
                send_otp_email(user)
                request.session['2fa_user'] = user.pk
                messages.info(request, 'An OTP has been sent to your email.')
                return redirect('otp_verification')  # Redirect to OTP entry page
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid login details. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def otp_verification(request):
    if request.method == 'POST':
        user_id = request.session.get('2fa_user')
        user = CustomUser.objects.get(pk=user_id)
        entered_otp = request.POST.get('otp')
        cached_otp = cache.get(f"{user.username}_otp")

        if cached_otp and str(entered_otp) == str(cached_otp):
            cache.delete(f"{user.username}_otp")
            login(request, user)
            del request.session['2fa_user']
            messages.success(request, 'You have successfully logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid or expired OTP. Please try again.')
            return redirect('otp_verification')
    return render(request, 'users/otp_verification.html')


# User Logout
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
