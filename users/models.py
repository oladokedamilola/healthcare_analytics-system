from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.base import ContentFile
import base64
from PIL import Image
from io import BytesIO
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    # New fields for tracking resend attempts
    resend_attempts = models.PositiveIntegerField(default=0)
    last_resend_attempt = models.DateTimeField(null=True, blank=True)
    reset_token = models.CharField(max_length=255, null=True, blank=True)

    def can_resend_activation_link(self):
        if self.resend_attempts >= 3:
            if self.last_resend_attempt and timezone.now() < self.last_resend_attempt + timedelta(hours=1):
                return False
        return True

    def reset_resend_attempts(self):
        self.resend_attempts = 0
        self.last_resend_attempt = None
        self.save()    
        
    def __str__(self):
        return self.username

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=50)
    license_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.specialty}"

    def generate_default_image(self):
        """Generate a default image based on the user's initials."""
        initials = ''.join(part[0] for part in self.user.email.split('@')[0].split('.'))  # Get initials from email
        image = Image.new('RGB', (100, 100), color=(255, 255, 255))  # White background
        return self.save_image(image, initials)

    def save_image(self, image, initials):
        """Save the image with initials."""
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        image_data = ContentFile(base64.b64decode(image_str), name=f"{initials}_default.png")
        self.profile_image.save(f"{initials}_default.png", image_data, save=False)

class Widget(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # Add any other fields relevant to the widget (e.g., type of metric)

    def __str__(self):
        return self.title

class UserDashboardSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    selected_widgets = models.ManyToManyField(Widget)

    def __str__(self):
        return f"{self.user.username}'s Dashboard Settings"
