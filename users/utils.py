# utils.py
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token

def send_verification_email(request, user):
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    message = render_to_string('users/activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    send_mail(subject, message, 'noreply@example.com', [user.email])


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
