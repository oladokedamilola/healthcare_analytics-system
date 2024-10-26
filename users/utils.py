from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from .models import CustomUser  # Ensure this import is included for type hinting

def send_verification_email(request, user: CustomUser):
    """
    Send an account activation email to the newly registered user.

    Args:
        request (HttpRequest): The request object.
        user (CustomUser): The user instance for whom the email is sent.
    """
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    
    # Generate activation details
    uidb64, token = generate_activation_details(user)

    # Construct the activation link
    activation_link = f"{request.scheme}://{current_site.domain}/accounts/activate/{uidb64}/{token}/"

    # Construct the message
    message = (
        f"Welcome, {user.first_name}!\n\n"
        "Thank you for registering with our Healthcare Data Analytics Platform. "
        "To complete your registration, please activate your account by clicking the link below:\n\n"
        f"{activation_link}\n\n"
        "If you didn't create an account, please ignore this email.\n\n"
        "Best regards,\nYour Healthcare Team"
    )

    # Send the email
    send_mail(subject, message, 'noreply@example.com', [user.email])


def generate_activation_details(user: CustomUser):
    """
    Generate UID and token for account activation.

    Args:
        user (CustomUser): The user instance for which to generate the activation details.

    Returns:
        tuple: A tuple containing the encoded UID and the activation token.
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    return uidb64, token



# utils.py
import random
from django.core.cache import cache
from django.core.mail import send_mail

def generate_otp():
    """Generate a 6-digit OTP."""
    return random.randint(100000, 999999)

def send_otp_email(user):
    """Generate OTP, store it in cache, and send it via email."""
    otp = generate_otp()
    cache.set(f"{user.username}_otp", otp, timeout=300)  # OTP valid for 5 minutes
    send_mail(
        'Your Login OTP',
        f'Use this OTP to complete your login: {otp}',
        'noreply@example.com',
        [user.email],
    )
    return otp

from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site

def send_password_reset_email(request, user: CustomUser):
    """
    Send a password reset email to the user.

    Args:
        request (HttpRequest): The request object.
        user (CustomUser): The user instance for whom the email is sent.
    """
    current_site = get_current_site(request)
    token = user.reset_token  # Assuming the token has been generated and saved
    reset_link = f"{request.scheme}://{current_site.domain}/accounts/reset-password/{token}/"

    subject = 'Reset Your Password'
    message = (
        f"Hi {user.first_name},\n\n"
        "You requested a password reset. Click the link below to reset your password:\n\n"
        f"{reset_link}\n\n"
        "If you didn't request this, please ignore this email.\n\n"
        "Best regards,\nYour Healthcare Team"
    )

    send_mail(subject, message, 'noreply@example.com', [user.email])
