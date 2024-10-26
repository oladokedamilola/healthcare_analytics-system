from django.urls import path
from .views import *

app_name ="users"

urlpatterns = [
    #Registration
    path('register/', register_doctor, name='register'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('activation-notification/', activation_notification, name='activation_notification'),  # New route
    path('resend-activation-link/<int:user_id>/', resend_activation_link, name='resend_activation_link'),
    path('complete-registration/<int:user_id>/', complete_doctor_registration, name='complete_doctor_registration'),


    #Login & Log out
    path('login/', user_login, name='login'),
    path('otp-verification/', otp_verification, name='otp_verification'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', reset_password, name='reset_password'),
    path('logout/', user_logout, name='logout'),

    #Dashboard
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/update/', update_dashboard_settings, name='update_dashboard_settings'),
]