# delete_user.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Doctor  # Adjust import according to your project structure
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Delete a user by email address'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email of the user to delete')

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        User = get_user_model()
        
        try:
            # Get the user by email
            user = User.objects.get(email=email)
            
            # If the user is a doctor, delete the associated doctor profile
            try:
                doctor = Doctor.objects.get(user=user)
                doctor.delete()
                self.stdout.write(self.style.SUCCESS(f'Deleted doctor profile for {user.email}'))
            except ObjectDoesNotExist:
                self.stdout.write(self.style.WARNING(f'No doctor profile found for {user.email}'))
            
            # Delete the user
            user.delete()
            self.stdout.write(self.style.SUCCESS(f'User with email {email} has been deleted.'))
        
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with email {email} does not exist.'))

