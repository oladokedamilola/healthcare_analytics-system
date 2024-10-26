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
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        
        if form.is_valid():
            user = CustomUser(
                username=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # Deactivate until email verification
            user.save()

            # Generate activation details and send email
            uidb64, token = generate_activation_details(user)
            try:
                send_verification_email(request, user)
            except Exception as e:
                messages.error(request, 'There was an error sending the verification email. Please try again.')

            # Store the user ID in session to access it in `activation_notification`
            request.session['user_id'] = user.id
            request.session['registration_incomplete'] = True
            messages.success(request, 'Registration successful! Check your email to activate your account.')
            return redirect('users:activation_notification')
        else:
            messages.error(request, 'Registration failed. Please check the form for errors.')
    else:
        form = DoctorRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})



def activation_notification(request, user=None):
    # Ensure the session variable for registration is set
    if not request.session.get('registration_incomplete', False):
        return redirect('users:login')  # Redirect if the session variable is not set

    # Use the passed user if provided; otherwise, get from session
    if not user:
        user_id = request.session.get('user_id')
        if user_id:
            user = get_object_or_404(CustomUser, id=user_id)
        else:
            return redirect('users:login')  # Redirect if no user ID is found in the session

    # Clear the session variable since we're displaying the notification now
    request.session.pop('registration_incomplete', None)

    return render(request, 'users/activation_notification.html', {'user': user})

def activate(request, uidb64, token):
    print("Debug: activate called with uidb64:", uidb64, "and token:", token)
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        print("Debug: User found for activation:", user.email)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
        print("Debug: User not found or error decoding uid.")

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated successfully!')
        print("Debug: User account activated. Redirecting to complete registration.")
        return redirect('users:complete_doctor_registration', user_id=user.id)
    else:
        messages.error(request, 'The activation link is invalid or has expired.')
        print("Debug: Activation link invalid. Rendering activation notification template.")
        
        # Set session variable and user_id for activation notification if needed
        request.session['registration_incomplete'] = True
        request.session['user_id'] = user.id if user else None
        return activation_notification(request)


def resend_activation_link(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        if user.can_resend_activation_link():
            # Send the verification email
            send_verification_email(request, user)
            user.resend_attempts += 1
            user.last_resend_attempt = timezone.now()
            user.save()
            return JsonResponse({'message': 'Verification email has been resent. Please check your email.'})
        else:
            return JsonResponse({'error': 'You can only resend the activation link 3 times. Please try again in one hour.'}, status=429)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)


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
            print("Debug: Redirecting to home after successful registration.")
            return redirect('home')  
        else:
            print("Debug: Form is invalid. Errors:", form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DoctorDetailsForm()

    return render(request, 'users/doctor_details.html', {'form': form, 'user': user})


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def user_login(request):
    print("Debug: user_login called.")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Debug: Attempting to log in user with email: {email}")

        # Get the user model
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)  # Find the user by email
            print(f"Debug: User found: {user.email}")
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            print("Debug: User does not exist.")
            return render(request, 'users/login.html')

        # Authenticate using username (or email) and password
        user = authenticate(username=user.username, password=password)
        
        if user is not None:
            if not user.is_active:  # Check if the account is active
                messages.error(request, 'Your account is not activated. Please check your email.')
                print("Debug: Account is not activated.")
                return render(request, 'users/login.html')

            # Send OTP email
            send_otp_email(user)
            request.session['2fa_user'] = user.pk
            messages.info(request, 'An OTP has been sent to your email.')
            print("Debug: OTP sent to email.")
            return redirect('users:otp_verification')  # Redirect to OTP entry page
        else:
            messages.error(request, 'Invalid email or password.')
            print("Debug: Authentication failed. Invalid credentials.")
    else:
        print("Debug: GET request to user_login.")
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


def otp_verification(request):
    print("Debug: otp_verification called.")
    if request.method == 'POST':
        user_id = request.session.get('2fa_user')
        if user_id is None:
            messages.error(request, 'Session expired. Please log in again.')
            print("Debug: Session expired. No user ID found.")
            return redirect('users:login')

        user = CustomUser.objects.get(pk=user_id)
        entered_otp = request.POST.get('otp')
        cached_otp = cache.get(f"{user.username}_otp")
        print(f"Debug: Cached OTP: {cached_otp}, Entered OTP: {entered_otp}")

        if cached_otp and str(entered_otp) == str(cached_otp):
            cache.delete(f"{user.username}_otp")
            login(request, user)
            del request.session['2fa_user']
            messages.success(request, 'You have successfully logged in!')
            print("Debug: User successfully logged in.")
            return redirect('home')
        else:
            messages.error(request, 'Invalid or expired OTP. Please try again.')
            print("Debug: Invalid or expired OTP. Redirecting back to verification.")
            return redirect('users:otp_verification')  # Redirect back to OTP verification
    return render(request, 'users/otp_verification.html')

from django.utils.crypto import get_random_string

@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def forgot_password(request):
    print("Debug: forgot_password called.")
    if request.method == 'POST':
        email = request.POST.get('email')
        print(f"Debug: Password reset requested for email: {email}")

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            print(f"Debug: User found: {user.email}")

            # Generate a unique password reset token
            token = get_random_string(length=32)
            user.reset_token = token  # Save the token to the database
            user.save()

            # Send the password reset email using the utility function
            send_password_reset_email(request, user)

            messages.success(request, 'If your email is registered, you will receive a password reset link.')
            return redirect('users:login')  # Redirect back to the login page
        except User.DoesNotExist:
            messages.error(request, 'If this email is registered, you will receive a reset link.')
            print("Debug: User does not exist.")
            return redirect('users:login')  # Redirect regardless of user existence

    return render(request, 'users/forgot_password.html')


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def reset_password(request, token):
    print("Debug: reset_password called with token:", token)
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            print("Debug: Passwords do not match.")
            return render(request, 'users/reset_password.html', {'token': token})

        try:
            user = CustomUser.objects.get(reset_token=token)  # Use CustomUser here

            user.set_password(new_password)
            user.reset_token = None  # Clear the token after use
            user.save()
            messages.success(request, 'Your password has been reset successfully. You can now log in.')
            return redirect('users:login')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid or expired token.')
            print("Debug: Invalid or expired token.")
    return render(request, 'users/reset_password.html', {'token': token})


# User Logout
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('users:login')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    settings, _ = UserDashboardSettings.objects.get_or_create(user=request.user)
    available_widgets = Widget.objects.all()
    return render(request, 'dashboard.html', {
        'selected_widgets': settings.selected_widgets.all(),
        'available_widgets': available_widgets,
    })

@login_required
def update_dashboard_settings(request):
    if request.method == 'POST':
        settings, _ = UserDashboardSettings.objects.get_or_create(user=request.user)
        selected_widget_ids = request.POST.getlist('widgets')  # Get selected widget IDs
        settings.selected_widgets.set(selected_widget_ids)  # Update selected widgets
        settings.save()
        return redirect('dashboard')  # Redirect to the dashboard
