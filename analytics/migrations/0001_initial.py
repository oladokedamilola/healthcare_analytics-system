# Generated by Django 5.1.2 on 2024-10-25 19:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HealthcareProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('specialization', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('medical_history', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnalyticsResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analysis_date', models.DateField()),
                ('result_data', models.JSONField()),
                ('healthcare_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analytics.healthcareprovider')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analytics.patient')),
            ],
        ),
    ]
