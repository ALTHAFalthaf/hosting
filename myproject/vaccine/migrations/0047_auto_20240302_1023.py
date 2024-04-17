# Generated by Django 3.2 on 2024-03-02 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0046_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vaccine.company'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Child', 'Child'), ('Doctor', 'Doctor'), ('HealthcareProvider', 'HealthcareProvider'), ('Company', 'Company')], default='Child', max_length=50),
        ),
    ]