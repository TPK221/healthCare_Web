# Generated by Django 3.2.5 on 2022-11-28 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthCare_app', '0011_rename_cconcern_appointment_concern'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='date',
            field=models.CharField(default='', max_length=100),
        ),
    ]
