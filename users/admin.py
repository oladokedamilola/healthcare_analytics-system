from django.contrib import admin
from .models import CustomUser, Doctor

admin.site.register(CustomUser)
admin.site.register(Doctor)
