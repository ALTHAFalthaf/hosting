# Generated by Django 3.2 on 2024-02-29 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0027_auto_20240229_1230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vaccinepurchase',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='vaccinepurchase',
            name='vaccine',
        ),
        migrations.DeleteModel(
            name='Vaccine',
        ),
        migrations.DeleteModel(
            name='VaccinePurchase',
        ),
    ]
