# Generated by Django 3.2.5 on 2022-11-29 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthCare_app', '0012_appointment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='state',
            field=models.CharField(default='', max_length=100),
        ),
    ]
