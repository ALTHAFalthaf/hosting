# Generated by Django 3.2 on 2024-02-11 09:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0005_auto_20240211_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_healthcare_provider',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='HealthcareProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(default='Healthcare Provider', max_length=100)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('professional_credentials', models.TextField(blank=True, null=True)),
                ('areas_of_specialization', models.TextField(blank=True, null=True)),
                ('availability', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='healthcare_provider_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
