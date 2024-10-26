# Generated by Django 5.1.2 on 2024-10-26 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='doctor',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='profile_image',
            field=models.ImageField(default='profile_images/default.png', upload_to='profile_images/'),
        ),
    ]