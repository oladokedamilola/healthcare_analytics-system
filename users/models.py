from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.base import ContentFile
import base64
from PIL import Image
from io import BytesIO

class CustomUser(AbstractUser):
    # No need for phone_number and profile_image here
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

