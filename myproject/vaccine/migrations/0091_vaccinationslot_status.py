# Generated by Django 4.2.5 on 2024-04-08 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0090_alter_vaccinationslot_slot'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaccinationslot',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('given', 'Given'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]
