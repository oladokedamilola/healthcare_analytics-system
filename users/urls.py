from django.urls import path
from .views import *

app_name ="users"

urlpatterns = [
    path('register/', register_doctor, name='register'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('complete-registration/<int:user_id>/', complete_doctor_registration, name='complete_doctor_registration'),
    path('login/', user_login, name='login'),
    path('otp-verification/', otp_verification, name='otp_verification'),
    path('logout/', user_logout, name='logout'),
]