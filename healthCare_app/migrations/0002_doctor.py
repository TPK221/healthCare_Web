# Generated by Django 3.2.5 on 2022-11-16 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthCare_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('languages', models.TextField()),
                ('gender', models.CharField(max_length=1)),
                ('qualifications', models.TextField()),
            ],
        ),
    ]
