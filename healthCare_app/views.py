from django.shortcuts import render
from django.contrib import auth
from pyparsing import identbodychars
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .models import Doctor
from .models import Appointment
from .models import AppointmentAdmin
import time
from datetime import datetime
import json

firebaseConfig = {
    'apiKey': "AIzaSyDShsoeNeZsQg2ZxdNp33v1QtrjSjalZPg",
    'authDomain': "health-care-web-212e0.firebaseapp.com",
    'databaseURL': "https://health-care-web-212e0-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "health-care-web-212e0",
    'storageBucket': "health-care-web-212e0.appspot.com",
    'messagingSenderId': "229559686647",
    'appId': "1:229559686647:web:a93fd4e466a9f2adb80af2",
    'measurementId': "G-WM3FSPBPDV",
    'serviceAccount': "C:\\Users\\tript\\Desktop\\University Year 2 Sem 6\\Semester 6 Sept 2022\\Internet & Web Development\\healthCare_Web-master\\healthCare_Web-master\\health-care-web-212e0-firebase-adminsdk-nyf5g-9ba2dd4249.json"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
authenticate = firebase.auth()
database = firebase.database()

userDetail = User()
apptDetail = Appointment()


def index(request):
    context = {'usrDetail': userDetail}
    return render(request, "index.html", context)


def register(request):
    context = {'usrDetail': userDetail}
    return render(request, "register.html", context)


def login(request):
    context = {'usrDetail': userDetail}
    return render(request, "login.html", context)


def findadoctor(request):
    # Retrieve stored specialties in database
    specialties = database.child('specialties').shallow().get().val()

    # Store retrieved specialties id to an array variable
    lis_specialties = []
    for i in specialties:
        i = int(i)
        lis_specialties.append(i)
    lis_specialties.sort()

    # Retrieve specialty title stored in database based on id
    specialty = []
    for i in lis_specialties:
        specialty_title = database.child(
            'specialties').child(i).child('title').get().val()
        specialty.append(specialty_title)

    # Retrieve specialty img URL stored in database based on id
    imageUrl = []
    for i in lis_specialties:
        specialty_imgUrl = database.child(
            'specialties').child(i).child('imgUrl').get().val()
        imageUrl.append(specialty_imgUrl)

    # Combine imgUrl and Title
    combine_list = zip(lis_specialties, specialty, imageUrl)
    combine_list_2 = zip(lis_specialties, specialty, imageUrl)

    # Retrieve all doctors from database
    doctors = database.child('doctors').shallow().get().val()

    # Retrieved doctor ID
    lis_doctor = []
    for i in doctors:
        lis_doctor.append(i)

    # Retrieve doctor name & specialty ID
    allDoctor = []
    specialtyID = []
    for i in lis_doctor:
        doctorName = database.child('doctors').child(
            i).child('name').get().val()
        doctorSpecialty = database.child('doctors').child(
            i).child('specialty').get().val()
        allDoctor.append(doctorName)
        specialtyID.append(doctorSpecialty)

    allDoctorList = json.dumps(allDoctor)

    context = {'combineList': combine_list, 'combineList_2': combine_list_2,
               'allDoctor': allDoctorList, 'doctorID': lis_doctor, 'specialtyID': specialtyID, 'usrDetail': userDetail}

    return render(request, "find-a-doctor.html", context)


def specialty(request):
    specialty = request.GET.get('specialtyId')
    doctors = []

    # Get doctor id from db
    doctorID = database.child('specialties').child(
        specialty).child('drId').get().val()
    doctorID = doctorID.split(', ')

    # Get Specialty Title from db
    title = database.child('specialties').child(
        specialty).child('title').get().val()

    # Find doctor details based on drID
    for id in doctorID:
        doctor = Doctor()
        doctor.drID = id
        doctor.name = database.child('doctors').child(
            id).child('name').get().val()
        doctor.languages = database.child('doctors').child(
            id).child('languages').get().val()
        gender = database.child('doctors').child(
            id).child('gender').get().val()
        if (gender == '1'):
            gender = "Male"
        else:
            gender = "Female"
        doctor.gender = gender

        doctor.qualifications = database.child('doctors').child(
            id).child('qualifications').get().val()
        doctors.append(doctor)

    context = {'title': title, 'doctor': doctors, 'usrDetail': userDetail}
    return render(request, "specialty.html", context)


def healthcareblog(request):
    context = {'usrDetail': userDetail}
    return render(request, "healthcare-blog.html", context)


def ourservices(request):
    context = {'usrDetail': userDetail}
    return render(request, "our-services.html", context)


def aboutus(request):
    context = {'usrDetail': userDetail}
    return render(request, "about-us.html", context)


def enquiry(request):
    sendMail = request.GET.get('sendMail')
    fullName = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    message = request.POST.get('message')

    if (sendMail == '1'):
        msg = "[User Detail]\n" \
            + "Name : " + fullName + "\n" \
            + "Email: " + email + "\n" \
            + "Phone Number: " + phone + "\n\n" \
            + "[Enquiry]\n" \
            + message

        # Send User Enquiry Email to TYK Medical
        send_mail(
            "[Enquiry] from " + fullName,  # Subject
            msg,  # Message
            "settings.EMAIL_HOST_USER",  # From Email
            [settings.EMAIL_HOST_USER],  # To Email
            fail_silently=False
        )
        print("Email Sent to TYK")
        context = {'usrDetail': userDetail}
        return render(request, "enquiry.html", context)

    context = {'usrDetail': userDetail}
    return render(request, "enquiry.html", context)


def doctorsInformation(request):
    doctorID = request.GET.get('drID')

    # Get doctor information from databse based on id
    doctor = Doctor()
    doctor.drID = id
    doctor.name = database.child('doctors').child(
        doctorID).child('name').get().val()
    doctor.languages = database.child('doctors').child(
        doctorID).child('languages').get().val()
    gender = database.child('doctors').child(
        doctorID).child('gender').get().val()
    if (gender == '1'):
        gender = "Male"
    else:
        gender = "Female"
    doctor.gender = gender

    doctor.qualifications = database.child('doctors').child(
        doctorID).child('qualifications').get().val()
    specialty = database.child('doctors').child(
        doctorID).child('specialty').get().val()
    doctor.specialty = assignSpecialty(specialty)

    doctor.save()

    context = {'usrDetail': userDetail, 'doctor': doctor}
    return render(request, "doctors-information.html", context)


def assignSpecialty(id):
    if id == '1':
        return "Anaesthesiology & Critical Care"
    elif id == '2':
        return "Cardiology"
    elif id == '3':
        return "Ear, Nose & Throat"
    elif id == '4':
        return "Endocrinology & Diabetes"
    elif id == '5':
        return "Gastroenterology & Hepatology"
    elif id == '6':
        return "Geriatrics"
    elif id == '7':
        return "Gynaecology"
    elif id == '8':
        return "Haematology"
    elif id == '9':
        return "Intensive Care"
    elif id == '10':
        return "Neurology"
    elif id == '11':
        return "Obstetrics & Gynaecology"
    elif id == '12':
        return "Orthopaedic & Trauma Surgery"
    elif id == '13':
        return "Paediatrics"
    elif id == '14':
        return "Radiology"
    elif id == '15':
        return "Rehabilitation Medicine"
    elif id == '16':
        return "Urology"


def makeAppointment(request):
    selectDoctor = request.GET.get('dr')
    sendMail = request.GET.get('sendMail')
    dr = request.POST.get('doctors')
    date_1 = str(request.POST.get('date_1'))
    date_2 = str(request.POST.get('date_2'))
    time_1 = str(request.POST.get('time_1'))
    time_2 = str(request.POST.get('time_2'))
    fullName = request.POST.get('name')
    email = request.POST.get('email')
    concern = request.POST.get('message')
    currentTimeStamp = time.time()

    if (sendMail == '1'):
        # Store appointment details under patient to database
        apptData = {"state": 1, "date": currentTimeStamp, "reqDoctor": dr, "date_1": date_1,
                    "date_2": date_2, "time_1": time_1, "time_2": time_2, "medicalConcerns": concern, "userID": str(userDetail.userID), "confirmDate": "no"}
        database.child("patients").child(str(userDetail.userID)
                                         ).child("appointment").set(apptData)

        # Store under main appointment database
        database.child("allAppointments").push(apptData)
   
        # Send Confirmation Email to User
        message = "Dear " + fullName + ",\n\n" + "Thank you for scheduling your appointment with TYK Medical Centre. You appointment request has been received. We hope to make sure your visit goes smoothly.\n\n" + "Appointment Request Details: \n" + "Requested Doctor: Dr. " + dr + \
            "\nDate Option 1: " + date_1 + "\t" + time_1 + "\n" + "Date Option 2: " + date_2 + "\t" + time_2 + "\n\n" + "If you require any further information, feel free to email us at tykmedicalcentre@gmail.com.\n\n" + "Sincerely,\n" + "TYK Medical Centre."

        send_mail(
            "[TYK Medical Centre] Received Your Appointment Request",  # Subject
            message,  # Message
            "settings.EMAIL_HOST_USER",  # From Email
            [email],  # To Email
            fail_silently=False
        )
        print("Email Sent")
        context = {'usrDetail': userDetail, 'sentMail': 1}
        return render(request, "make-appointment.html", context)

    # Retrieve all doctors in database
    doctors = database.child('doctors').shallow().get().val()

    # Store retrieved doctors id to an array variable
    lis_doctors = []
    for i in doctors:
        lis_doctors.append(i)

    # Retrieve doctors name stored in database based on id
    doctorName = []
    for i in lis_doctors:
        drName = database.child('doctors').child(i).child('name').get().val()
        doctorName.append(drName)

    # Combine Doctor ID and Doctor Name
    doctor_list = zip(lis_doctors, doctorName)

    context = {'doctorList': doctor_list,
               'usrDetail': userDetail, 'selectDoctor': selectDoctor, 'apptDetail': apptDetail}

    return render(request, "make-appointment.html", context)


def postRegister(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    phoneNum = request.POST.get('number')
    confirmPsw = request.POST.get('confirmPsw')
    gender = request.POST.get('genderSelect')
    dob = request.POST.get('dob')

    # Register user in firebase using email & password
    try:
        user = authenticate.create_user_with_email_and_password(
            email, confirmPsw)
    except:
        message = "fail"
        return render(request, "register.html", {"msg": message})

    # Retrieve User Unique ID after successfully registered user
    uid = user['localId']

    userData = {"name": name, "email": email,
                "phoneNum": phoneNum, "gender": gender, "dob": dob}

    database.child("patients").child(uid).child("details").set(userData)
    message = "success"

    context = {"msg": message}
    return render(request, "register.html", context)


def postLogin(request):
    email = request.POST.get('email')
    password = request.POST.get('psw')

    # Login
    try:
        user = authenticate.sign_in_with_email_and_password(email, password)
    except:
        message = "inputError"
        return render(request, "register.html", {"msg": message})

    # Get user id and store as session id, request session while user login
    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    # Retrieve Data from Firebase
    idtoken = request.session['uid']
    usrAuth = authenticate.get_account_info(idtoken)
    usr_id = usrAuth
    usr_id = usr_id['users']
    usr_id = usr_id[0]
    usr_id = usr_id['localId']

    # Store user data to User Class
    userDetail.userID = usr_id
    userDetail.name = database.child('patients').child(
        usr_id).child('details').child('name').get(idtoken).val()
    userDetail.email = database.child('patients').child(
        usr_id).child('details').child('email').get(idtoken).val()
    userDetail.phone = database.child('patients').child(
        usr_id).child('details').child('phoneNum').get(idtoken).val()

    userDetail.gender = database.child('patients').child(
        usr_id).child('details').child('gender').get(idtoken).val()

    userDetail.dob = database.child('patients').child(
        usr_id).child('details').child('dob').get(idtoken).val()
    userDetail.save()

    context = {'usrDetail': userDetail}
    return render(request, "index.html", context)


def logout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    return render(request, "index.html")


def patientsProfile(request):
    uid = str(userDetail.userID)
    cancelAppt = request.GET.get('cancel')

    if (str(userDetail.gender) == '1'):
        gender = "Male"
    else:
        gender = "Female"

    context = {'usrDetail': userDetail, "patientGender": gender}

    if (cancelAppt == '1'):
        target = ""
        timeStamp = str(database.child("patients").child(uid).child('appointment').child('date').get().val())
        tstamp = database.child('allAppointments').shallow().get().val()
        lis_stamp = []
        for j in tstamp:
            lis_stamp.append(j)
        for k in lis_stamp:
            keyID = str(database.child("allAppointments").child(k).child('date').get().val())
            if (keyID == timeStamp):
                target = k
        database.child("patients").child(uid).child('appointment').remove()
        database.child("allAppointments").child(target).remove()

        apptDetail.delete()
        context = {'usrDetail': userDetail, "patientGender": gender}
        return render(request, "patients-profile.html", context)
    else:
        # Store user appointment details to Appointment Class
        if database.child('patients').child(uid).child('appointment').shallow().get().val():
            date = database.child('patients').child(uid).child(
                'appointment').child('date').get().val()
            convertDate = datetime.fromtimestamp(
                date).strftime('%Y-%m-%d, %I:%M %p')
            apptDetail.date = str(convertDate)

            state = database.child('patients').child(
                uid).child('appointment').child('state').get().val()
            if (state == 1):
                apptDetail.state = "Pending Confirmation"
            elif (state == 2):
                apptDetail.state = "Appointment Confirmed"
            else:
                apptDetail.state = "Appointment Declined"

            apptDetail.reqDoctor = database.child('patients').child(
                uid).child('appointment').child('reqDoctor').get().val()
            apptDetail.date_1 = database.child('patients').child(
                uid).child('appointment').child('date_1').get().val()
            apptDetail.date_2 = database.child('patients').child(
                uid).child('appointment').child('date_2').get().val()
            apptDetail.time_1 = database.child('patients').child(
                uid).child('appointment').child('time_1').get().val()
            apptDetail.time_2 = database.child('patients').child(
                uid).child('appointment').child('time_2').get().val()
            apptDetail.concern = database.child('patients').child(uid).child(
                'appointment').child('medicalConcerns').get().val()
            apptDetail.confirmDate = database.child('patients').child(uid).child(
                'appointment').child('confirmDate').get().val()
            apptDetail.save()
            context = {'usrDetail': userDetail, 'apptDetail': apptDetail, "patientGender": gender}

    return render(request, "patients-profile.html", context)


def adminPage(request):
    context = {}
    patientID = request.GET.get('patientID')

    state = request.GET.get('state')
    apptID = request.GET.get('apptID')
    confirmDate = request.GET.get('confirmDate')
    if (str(state) == '2'):
        database.child("allAppointments").child(apptID).update({"state": 2, "confirmDate": confirmDate})
        
        timeStamp = str(database.child("allAppointments").child(apptID).child('date').get().val())
        tstamp = database.child('patients').shallow().get().val()
        lis_patient = []
        for j in tstamp:
            lis_patient.append(j)
        for k in lis_patient:
            keyID = str(database.child("patients").child(k).child('appointment').child('date').get().val())
            if (keyID == timeStamp):
                database.child("patients").child(k).child('appointment').update({"state": 2, "confirmDate": confirmDate})
                

    # Retrieve all appointment requests from database
    if database.child('allAppointments').shallow().get().val():

        appointments = database.child('allAppointments').shallow().get().val()

        # Store retrieved appt id to an array variable
        lis_appt = []
        for i in appointments:
            lis_appt.append(i)

        # Retrieve appt detail from database
        appt = []
        for i in lis_appt:
            apptAll = AppointmentAdmin()

            apptAll.apptID = i

            patientID = database.child('allAppointments').child(i).child('userID').get().val()
            apptAll.patientID = patientID
    

            timeStamp = str(database.child("patients").child(patientID).child('appointment').child('date').get().val())
            tstamp = database.child('allAppointments').shallow().get().val()
            lis_stamp = []
            for j in tstamp:
                lis_stamp.append(j)
            for k in lis_stamp:
                keyID = str(database.child("allAppointments").child(k).child('date').get().val())
                if (keyID == timeStamp):
                    target = k


            date = database.child('allAppointments').child(
                i).child('date').get().val()
            convertDate = datetime.fromtimestamp(
                date).strftime('%Y-%m-%d, %I:%M %p')
            apptAll.apptDate = str(convertDate)

            state = database.child('allAppointments').child(
                i).child('state').get().val()
            if (str(state) == '1'):
                apptAll.apptStatus = "Pending Confirmation"
            elif (str(state) == '2'):
                apptAll.apptStatus = "Appointment Confirmed"

            apptAll.reqDoctor = database.child('allAppointments').child(
                i).child('reqDoctor').get().val()

            date1 = str(database.child('allAppointments').child(i).child('date_1').get().val(
            )) + ", " + str(database.child('allAppointments').child(i).child('time_1').get().val())
            date2 = str(database.child('allAppointments').child(i).child('date_2').get().val(
            )) + ", " + str(database.child('allAppointments').child(i).child('time_2').get().val())
            apptAll.date1 = date1
            apptAll.date2 = date2

            apptAll.patientName = database.child('patients').child(patientID).child('details').child('name').get().val()
            apptAll.patientContact = database.child('patients').child(patientID).child('details').child('phoneNum').get().val()

            apptAll.save()
            appt.append(apptAll)
        context = {'appt': appt}
    
    return render(request, "adminPage.html", context)


def adminPageDetail(request):
    apptDetail = AppointmentAdmin()
    apptID = request.GET.get('apptID')
    apptDetail.apptID = apptID
    patientID = database.child('allAppointments').child(apptID).child('userID').get().val()

    date = database.child('allAppointments').child(apptID).child('date').get().val()
    convertDate = datetime.fromtimestamp(date).strftime('%Y-%m-%d, %I:%M %p')
    apptDetail.apptDate = str(convertDate)

    state = database.child('allAppointments').child(apptID).child('state').get().val()
    if (str(state) == '1'):
        apptDetail.apptStatus = "Pending Confirmation"
    elif (str(state) == '2'):
        apptDetail.apptStatus = "Appointment Confirmed"

    apptDetail.reqDoctor = database.child('allAppointments').child(apptID).child('reqDoctor').get().val()
    apptDetail.confirmDate = database.child('allAppointments').child(apptID).child('confirmDate').get().val()

    date1 = str(database.child('allAppointments').child(apptID).child('date_1').get().val()) + ", " + str(database.child('allAppointments').child(apptID).child('time_1').get().val())
    date2 = str(database.child('allAppointments').child(apptID).child('date_2').get().val()) + ", " + str(database.child('allAppointments').child(apptID).child('time_2').get().val())
    apptDetail.date1 = date1
    apptDetail.date2 = date2

    apptDetail.patientName = database.child('patients').child(patientID).child('details').child('name').get().val()
    apptDetail.patientContact = database.child('patients').child(patientID).child('details').child('phoneNum').get().val()

    apptDetail.save()

    context = {'appt': apptDetail, "patientID": patientID}

    return render(request, "adminPage-detail.html", context)
