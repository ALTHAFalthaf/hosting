# Generated by Django 4.2.5 on 2024-04-14 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0100_alter_vaccinationslot_birth_details'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VaccinationSchedule',
        ),
        migrations.RemoveField(
            model_name='vaccinationslot',
            name='birth_details',
        ),
        migrations.AlterField(
            model_name='vaccinationslot',
            name='vaccine',
            field=models.CharField(max_length=100, null=True),
        ),
    ]