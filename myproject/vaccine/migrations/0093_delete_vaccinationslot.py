# Generated by Django 4.2.5 on 2024-04-12 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0092_alter_vaccinationslot_vaccine'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VaccinationSlot',
        ),
    ]