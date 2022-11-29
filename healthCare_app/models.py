from django.db import models


class User(models.Model):
    userID = models.TextField(max_length=100, default='')
    name = models.CharField(max_length=100)
    email = models.TextField(max_length=100)
    phone = models.CharField(max_length=100, default='')
    gender = models.CharField(max_length=100, default='')
    dob = models.TextField(max_length=100, default='')


class Doctor(models.Model):
    drID = models.CharField(max_length=20, default='')
    name = models.CharField(max_length=100)
    languages = models.TextField()
    gender = models.CharField(max_length=1)
    qualifications = models.TextField()
    specialty = models.CharField(max_length=10, default='')


class Appointment(models.Model):
    date = models.CharField(max_length=100, default='', null=True)
    reqDoctor = models.CharField(max_length=100, null=True)
    date_1 = models.CharField(max_length=100, null=True)
    date_2 = models.CharField(max_length=100, null=True)
    time_1 = models.CharField(max_length=100, null=True)
    time_2 = models.CharField(max_length=100, null=True)
    concern = models.TextField(max_length=1000,null=True)
    state = models.CharField(max_length=100, default='',null=True)
    confirmDate = models.CharField(max_length=100, default='',null=True)


class AppointmentAdmin(models.Model):
    apptID = models.CharField(max_length=100, default='')
    apptDate = models.CharField(max_length=100)
    apptStatus = models.CharField(max_length=100)
    reqDoctor = models.CharField(max_length=100)
    confirmDate = models.CharField(max_length=100, default='')
    date1 = models.CharField(max_length=100, default='')
    date2 = models.CharField(max_length=100, default='')
    patientName = models.CharField(max_length=100, default='')
    patientContact = models.CharField(max_length=100, default='')
    patientID = models.CharField(max_length=100, default='')

