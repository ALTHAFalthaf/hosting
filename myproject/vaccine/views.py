
# from datetime import datetime
# from django.shortcuts import render, redirect
# from django.contrib.auth.hashers import make_password
# from .models import Usertable



# # Create your views here.
# def index(request):
#     return render(request, "index.html")

# def about(request):
#     return render(request, "about.html")

# def contact(request):
#     return render(request, "contact.html")

# def signup(request):
#     if request.method == 'POST':
#         role = request.POST['role']
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         password = request.POST['password']
#         hashed_password = make_password(password)
#         user = Usertable(role=role, fname=fname, lname=lname,phone=phone, email=email, password=hashed_password)
#         user.save()
#         return redirect('login')
#     return render(request, "signup.html")

# def login(request):
#     return render(request, "login.html")

# def signin(request):
#     return render(request, "signin.html")





from django.contrib import admin
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login, get_user_model
from django.contrib.auth import logout as auth_logout 
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist 
from .models import Appointment
from .models import Doctor
from .models import HealthcareProvider


# from .helpers import send_forget_password_mail
# from .forms import PatientProfileForm

# Create your views here.
def index(request):
    return render(request,'index.html')

 #@login_required
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def homepage(request):
    if 'email' in request.session:
        response = render(request, 'homepage.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('login')


def about(request):
    return render(request, 'about.html')  


def contact(request):
    return render(request, 'contact.html')  





def doctor_added(request):
    return render(request, 'doctor_added.html')  # Display the success page





def view_doctor(request):
    return render(request, 'view_doctor.html')  # Display the success page


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def company_home(request):
    return render(request, 'company_home.html')


def doctor_list(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'doctor_list.html', context)





def myprofile(request):
    return render(request, 'myprofile.html')


def editprofile(request):
    if request.method == "POST":
        user = CustomUser.objects.get(id=request.user.id)

        # Update user data with form data
        user.first_name = request.POST.get("fname")
        user.last_name = request.POST.get("lname")
        user.phone = request.POST.get("phone")
        user.save()

        # Display a success message using Django's messages framework
        messages.success(request, "Profile updated successfully!")

        # Redirect to the My Profile page
        return redirect('myprofile')

    return render(request, 'editprofile.html')



def loginn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Try to retrieve the user by email
            user = authenticate(request, email=email, password=password)
            
            
            if user is not None:
                if user.is_active:
                    if user.is_superuser:
                        request.session['email'] = email
                        auth_login(request, user)
                        return redirect('adminreg')
                    elif user.role == 'Company':
                        # Company login
                        request.session['email'] = email
                        auth_login(request, user)
                        return redirect('company_home')
                    elif user.role == 'HealthcareProvider':
                        # Company login
                        request.session['email'] = email
                        auth_login(request, user)
                        return redirect('healthcareprovider_home') 
                    else:
                        request.session['email'] = email
                        auth_login(request, user)
                        # Check if the user is a doctor
                        if user.role == 'Doctor':
                            return redirect('doctor_home')
                        else:
                            return redirect('homepage')
                        
                else:
                    error_message = "Invalid credentials"
                    messages.error(request, error_message)
            else:
                error_message = "Incorrect username or Password"
                messages.error(request, error_message)

        except ObjectDoesNotExist:
            # User with the given email does not exist
            error_message = "User with this email does not exist. Please sign up."
            messages.error(request, error_message)

    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response
    # return render(request,'login.html')

@login_required
def signup(request):
    if request.method == "POST":
        firstname=request.POST.get('fname') 
        lastname = request.POST.get('lname')
        email = request.POST.get('email')
        phone=request.POST.get('phone')
        dob=request.POST.get('dob')
        gender=request.POST.get('gender')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
      
        

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            user = CustomUser(first_name=firstname,last_name=lastname,email=email,phone=phone,dob=dob,gender=gender,role='CHILD')  # Change role as needed
            user.set_password(password)
            user.save()
            messages.success(request, "Registered successfully")
            return redirect("login")
    return render(request,'signup.html')



@cache_control(no_cache=True,must_revalidate=True,no_store=True)

@login_required
def user_logout(request):
    try:
        del request.session['email']
    except:
        return redirect('login')
    return redirect('login')



    



from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.conf import settings

def deactivate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
         # Send deactivation email
        subject = 'Account Deactivation'
        message = 'Your account has been deactivated by the admin.'
        from_email = 'kiddoguard12@gmail.com'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('deactivation_email.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        messages.success(request, f"User '{user.email}' has been deactivated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.email}' is already deactivated.")
    return redirect('adminreg')

def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()
        subject = 'Account activated'
        message = 'Your account has been activated.'
        from_email = 'kiddoguard12@gmail.com'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_email.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    else:
        messages.warning(request, f"User '{user.username}' is already active.")
    return redirect('adminreg')



from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from .models import Doctor
from .models import Appointment 
from .models import Company

def send_registration_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        registration_link = request.build_absolute_uri(reverse('doctor_registration'))
        subject = 'Doctor Registration Link'
        message = render_to_string('registration_email.html', {'name': name, 'registration_link': registration_link})
        from_email = 'kiddoguard12@gmail.com'  # Replace with your email address
        send_mail(subject, message, from_email, [email])
        messages.success(request, f'Registration email sent to {email}')
        return redirect('adminreg')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def adminreg(request):
    User = get_user_model()
    
    if request.method == 'POST':
        if 'send_email' in request.POST:
            doctor_email = request.POST.get('doctor_email')
            message = "Your message goes here."  # Customize the email message
            send_mail('Subject', message, 'kiddoguard12@gmail.com', [doctor_email])
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if 'email' in request.session:
        email = request.session['email']
        try:
            user = User.objects.get(email=email)
            if user.role == 'Admin':
                user_profiles = User.objects.all()

                # Filter doctors based on the 'approved' field
                doctors = Doctor.objects.filter(approved=False)
                approved_doctors = Doctor.objects.filter(approved=True)
                appointments = Appointment.objects.all()
                providers = HealthcareProvider.objects.all()
                birth_details = BirthDetails.objects.all()
                companies = Company.objects.all()

                context = {'user_profiles': user_profiles, 'doctors': doctors, 'approved_doctors': approved_doctors,'appointments': appointments,'providers': providers,'birth_details': birth_details,'companies':companies}
                return render(request, 'adminreg.html', context)
            else:
                messages.error(request, "You don't have permission to access this page.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "Login failed. Please check your credentials.")
        return redirect('login')

def doctor_registration(request):
    if request.method == 'POST':
        # Get data from the submitted form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth')
        specialty = request.POST.get('specialty')
        license_number = request.POST.get('license_number')
        certification = request.POST.get('certification')
        resume = request.FILES.get('resume')
        license_copy = request.FILES.get('license_copy')
        photo = request.FILES['photo']

        # Try to create a new Doctor object and handle IntegrityError
        try:
            doctor = Doctor(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                date_of_birth=date_of_birth,
                specialty=specialty,
                license_number=license_number,
                certification=certification,
                resume=resume,
                license_copy=license_copy,
                photo=photo,
                approved=False  # Set approved status to False by default
            )
            doctor.save()

            messages.success(request, 'Doctor registration successful. Waiting for approval.')
            return redirect('adminreg')
        except IntegrityError as e:
            # Handle the IntegrityError
            if 'UNIQUE constraint' in str(e):
                messages.error(request, 'A doctor with this email already exists.')
            else:
                messages.error(request, 'An error occurred during registration.')

    return render(request, 'doctor_registration.html')

    
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Doctor

User = get_user_model()

def approve_doctor(request, doctor_id):
    if request.method == 'POST':
        # Retrieve the doctor from the database
        doctor = Doctor.objects.get(id=doctor_id)

        # Check if the phone number is unique
        try:
            user = User.objects.get(phone=doctor.phone)
            messages.error(request, 'Phone number already in use by another user.')
        except User.DoesNotExist:
            # Create a new user (doctor) with the doctor's details
            user = User(
                first_name=doctor.first_name,
                last_name=doctor.last_name,
                email=doctor.email,
                phone=doctor.phone,
                role='Doctor',  # Make sure to set the appropriate role
            )

            # Generate a password (replace with your password generation logic)
            password = 'Aqwer12@'
            user.set_password(password)
            user.save()
            
            # Update the 'approved' status for the doctor
            doctor.approved = True
            doctor.save()

            # Send an email with the generated password
            subject = 'Your Doctor Homepage Password'
            message = render_to_string('password_email.html', {'password': password})
            from_email = 'kiddoguard12@gmail.com'  # Replace with your email address
            recipient_list = [doctor.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            messages.success(request, 'Doctor approved and password set.')

    return redirect('adminreg')







import random
import string

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password





from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Appointment, Doctor, BirthDetails
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def book_appointment(request, doctor_id):
    try:
        # Assuming that the doctor_id is passed in the URL
        doctor = Doctor.objects.get(id=doctor_id)

        if request.method == 'POST':
            child_id = request.POST.get('child')
            appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')
            description = request.POST.get('description')
            comments = request.POST.get('comments')


            if not child_id or not appointment_date or not appointment_time:
                return JsonResponse({'message': 'All fields are required.'})

            try:
                child = BirthDetails.objects.get(pk=child_id)
            except BirthDetails.DoesNotExist:
                return JsonResponse({'message': 'Invalid child selected.'})

            # Assuming the user is the patient making the appointment
            user = request.user

            # Create an Appointment object
            appointment = Appointment.objects.create(
                user=user,
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                description=description,
                comments=comments
            )

            # Add any additional logic here (e.g., send confirmation email)

            return redirect('appointment_confirmation', appointment_id=appointment.id) 


        else:
            children = BirthDetails.objects.all()
            
             # You can redirect to a success page or any other page

        return render(request, 'book_appointment.html', {'doctor': doctor, 'children': children})

    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor not found.')
        return redirect('appointment-error')  # You can redirect to an error page or any other page


from django.shortcuts import render
from .models import Appointment
import razorpay
from django.views.decorators.csrf import csrf_exempt

@login_required
def appointment_confirmation(request, appointment_id):
    amount_in_paise = int(500 * 100)
    
    DATA = {
        "amount": amount_in_paise,
        "currency":"INR",
        "receipt":"receipt1",
        "notes":{
            "key1": "value3",
            "key2": "value2",
        }
    }

    client = razorpay.Client(auth=("rzp_test_EZL2rQubxJwxrv","RhRefR6hrzAdlzxNVUm6s4Ja"))
    payment = client.order.create(data=DATA)

     # Assuming you have a variable indicating payment success
    payment_success = True  # Adjust this based on your payment logic

    context = {
        'amount': amount_in_paise,
        'payment': payment,
        
        
        
    }

    try:
        # Assuming the appointment_id is passed in the URL
        appointment = Appointment.objects.get(id=appointment_id)
        context['appointment'] = appointment
        return render(request, 'appointment_confirmation.html', context)

    except Appointment.DoesNotExist:
        # Handle the case where the appointment does not exist
        return render(request, 'appointment-error.html')




# views.py

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Appointment

@require_POST
def check_time_availability(request):
    appointment_time = request.POST.get('appointment_time')
    appointment_date = request.POST.get('appointment_date')

    # Check if there is an existing appointment for the chosen time slot
    existing_appointment = Appointment.objects.filter(
        appointment_date=appointment_date,
        appointment_time=appointment_time
    ).exists()

    return JsonResponse({'available': not existing_appointment})




# views.py

from django.shortcuts import render
from .models import Doctor
from .models import Appointment
from django.contrib.auth.decorators import login_required


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def doctor_home(request):
    return render (request,'doctor_home.html')


@login_required
def doctor_appointments(request):
    doctor = request.user.doctor  # Assuming the doctor is associated with the user
    appointments = Appointment.objects.filter(doctor=doctor)

    for appointment in appointments:
        prescription_exists = VaccinePrescription.objects.filter(appointment=appointment).exists()
        appointment.prescription_exists = prescription_exists  # Add a new attribute to the appointment object
    
    return render(request, 'doctor_appointments.html', {'doctor': doctor, 'appointments': appointments})

def clear_appointments(request):
    if request.method == 'POST':
        # Clear all appointments
        Appointment.objects.all().delete()
    return redirect('doctor_appointments')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Appointment, VaccinePrescription, Vaccine

@login_required
def prescribe_vaccines(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        vaccines = Vaccine.objects.all()  # Fetch all vaccines

        if request.method == 'POST':
            vaccine_id = request.POST.get('vaccine')
            doses = request.POST.get('doses')
            comments = request.POST.get('comments')

            # Assuming you have proper validation for vaccine and doses
            vaccine_prescription = VaccinePrescription.objects.create(
                appointment=appointment,
                doctor=request.user.doctor,
                vaccine_id=vaccine_id,
                doses=doses,
                comments=comments
            )
            
            # Return a success response
            return JsonResponse({'success': True, 'message': 'Vaccine prescribed successfully.'})

        return render(request, 'prescribe_vaccines.html', {'appointment': appointment, 'vaccines': vaccines})

    except Appointment.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Appointment not found.'})


from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os
from xhtml2pdf import pisa
from .models import Appointment, VaccinePrescription

def generate_prescription_pdf(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        prescription = VaccinePrescription.objects.get(appointment=appointment)

        # Render prescription template with dynamic data
        template_path = 'prescription_report.html'
        template = get_template(template_path)
        html = template.render({'appointment': appointment, 'prescription': prescription})

        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="prescription.pdf"'

        # Generate PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('PDF generation error')

        return response

    except (Appointment.DoesNotExist, VaccinePrescription.DoesNotExist):
        return HttpResponse('Appointment or Prescription not found')



    

        
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Doctor

User = get_user_model()

@login_required
def doctor_profile(request):
    doctor = request.user.doctor
    profile_updated = False  # Initialize the variable

    if request.method == 'POST':
        # Handle profile update
        doctor.first_name = request.POST.get('first_name', '')
        doctor.last_name = request.POST.get('last_name', '')
        doctor.email = request.POST.get('email', '')
        doctor.phone = request.POST.get('phone', '')

        # Handle photo upload
        photo = request.FILES.get('photo')
        if photo:
            # If a new photo is provided, save it and update the doctor's photo field
            photo_name = default_storage.save(f'doctor/photos/{user.doctor.id}/{photo.name}', photo)
            doctor.photo = photo_name
        doctor.save()

        # Fetch the updated data from the database
        doctor = Doctor.objects.get(id=doctor.id)

        profile_updated = True

    return render(request, 'doctor_profile.html', {'doctor': doctor, 'profile_updated': profile_updated})



@login_required
def change_password(request):
    password_updated = False  # Initialize the variable

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            password_updated = True
            update_session_auth_hash(request, user)  # Important to maintain the session
            

        else:
            messages.error(request, 'Error changing password. Please correct the errors.')
    else:
        form = PasswordChangeForm(request.user)


    return render(request, 'change_password.html', {'form': form,  'password_updated': password_updated})



 










#Vaccintion views
from django.shortcuts import render
from .models import BirthDetails

def vaccination_home(request):
    # Assuming you retrieve the child ID from the database or any other source
    child_id = 1  # Replace 1 with the actual child ID
    return render(request, 'vaccination_home.html', {'child_id': child_id})









#payment

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def payment_success(request):

    messages.success(request,'payment successfull')
    return redirect('homepage')




from django.shortcuts import render
from .models import Appointment

def appointment_history(request):
    # Retrieve all appointments and sort them by date
    appointments = Appointment.objects.all().order_by('appointment_date')

    # Pass the sorted appointments to the template
    return render(request, 'appointment_history.html', {'appointments': appointments})

from django.shortcuts import redirect, get_object_or_404
from .models import Appointment

def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        # Delete the appointment
        appointment.delete()
        # Redirect to appointment history page or any other page
        return redirect('appointment_history')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import HealthcareProvider

def signup_healthcare_provider(request):
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        license_number = request.POST.get('license_number')
        certification = request.POST.get('certification')
        resume = request.FILES.get('resume')
        license_copy = request.FILES.get('license_copy')
        photo = request.FILES.get('photo')

        try:
            # Create and save the HealthcareProvider instance
            provider = HealthcareProvider.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,  # Assuming 'phone' is the field name in the model
                license_number=license_number,
                certification=certification,
                resume=resume,
                license_copy=license_copy,
                photo=photo
            )
            messages.success(request, 'Healthcare provider added successfully.')
            return redirect('adminreg')  # Redirect to success page
        except Exception as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'signup_healthcare_provider.html')  # Replace 'your_template.html' with your actual template name



# views.py

from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import HealthcareProvider

User = get_user_model()

def generate_password_provider(request, provider_id):
    if request.method == 'POST':
        # Retrieve the healthcare provider from the database
        provider = HealthcareProvider.objects.get(id=provider_id)

        # Check if the email is unique
        try:
            user = User.objects.get(email=provider.email)
            messages.error(request, 'Email already in use by another user.')
        except User.DoesNotExist:
            # Create a new user (healthcare provider) with the provider's details
            user = User(
                first_name=provider.first_name,
                last_name=provider.last_name,
                email=provider.email,
                phone=provider.phone,
                role='Healthcare Provider',  # Make sure to set the appropriate role
            )

            # Generate a password (replace with your password generation logic)
            password = 'Qwer123@'
            user.set_password(password)
            user.save()
            
            # Update the 'is_verified' status for the healthcare provider
            provider.is_verified = True
            provider.save()

            # Send an email with the generated password
            subject = 'Your Healthcare Provider Account Password'
            message = render_to_string('password_email.html', {'password': password})
            from_email = 'kiddoguard12@gmail.com'  # Replace with your email address
            recipient_list = [provider.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            messages.success(request, 'Healthcare provider approved and password set.')

    return redirect('adminreg')



def healthcareprovider_home(request):
    return render(request,'healthcareprovider_home.html')

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Company

def approve_company(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    company.is_verified = True
    company.status = 'Approved'  # Assuming 'status' is the field representing the status
    company.save()
    messages.success(request, 'Company approved successfully.')
    return redirect('adminreg')  # Redirect to wherever you want


def deactivate_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        # Deactivate the company
        company.status = 'Deactivated'
        company.save()
        # Optionally, perform additional actions like notifying users or logging the deactivation
        return redirect('adminreg')  # Replace 'your_redirect_url' with the appropriate URL




from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import BirthDetails, VaccinationSlot

@login_required
def upload_birth_details(request):
    if request.method == 'POST':
        # Extract form data
        child_id = request.POST.get('child_id') 
        child_fname = request.POST.get('child_fname')
        child_lname = request.POST.get('child_lname')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        place_of_birth = request.POST.get('place_of_birth')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        regno = request.POST.get('regno')
        rchid = request.POST.get('rchid')
        

        # Get the current authenticated user
        # Check if the birth details already exist for the user
        existing_details = BirthDetails.objects.filter(regno=regno)
        if existing_details.exists():
            messages.error(request, "Birth details already exist for this registration number.")
            return redirect('vaccination_home') 

        # Save data into database
        birth_details = BirthDetails(
            child_id=child_id, 
            child_fname=child_fname,
            child_lname=child_lname,
            date_of_birth=date_of_birth,
            gender=gender,
            age=age,
            place_of_birth=place_of_birth,
            weight=weight,
            height=height,
            regno=regno,
            rchid=rchid
        )
        birth_details.save()

        request.session['child_id'] = birth_details.child_id

        return redirect('schedule_vaccination', child_id=birth_details.child_id)  

        # Optionally, you can return a JsonResponse to indicate success
        return JsonResponse({'success': True, 'message': 'Data saved successfully'})

    else:
        child_id = request.session.get('child_id')
        child = BirthDetails.objects.get(id=child_id)

        # Render the template with the child object and child_id
        return render(request, 'upload_birth_details.html', {'child': child, 'child_id': child_id})






# from django.shortcuts import render, get_object_or_404
# from .models import BirthDetails, CustomUser

# def view_birth_details(request, user_id):
#     user_profile = get_object_or_404(CustomUser, id=user_id)
#     birth_details = BirthDetails.objects.filter(user=user_profile)
#     return render(request, 'birth_details.html', {'user_profile': user_profile, 'birth_details': birth_details})






    
    
# from django.shortcuts import render

# def birth_details_list(request):
#      return render(request, 'birth_details_list.html')

# import csv
# from django.http import HttpResponse
# from .models import BirthDetails

# def download_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="birth_details.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['Child Name', 'Date of Birth', 'Gender','age','Place of Birth', 'Weight', 'Height', 'Registration No', 'RCH ID'])

#     birth_details = BirthDetails.objects.all()
#     for detail in birth_details:
#          writer.writerow([detail.user.first_name, detail.user.dob, detail.user.gender,detail.user.age, detail.place_of_birth, detail.weight, detail.height, detail.regno, detail.rchid])

#     return response





def vaccine_record(request):
    return render(request , 'vaccine_record.html')









from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Vaccine
import pandas as pd
from django.contrib import messages
from django.conf import settings

def upload_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']

        # Check if the data has already been loaded
        if not settings.VACCINES_DATA_LOADED:
            try:
                # Read the Excel file into a pandas DataFrame
                excel_data = pd.read_excel(excel_file)
                
                # Iterate over DataFrame rows and create Vaccine instances
                for index, row in excel_data.iterrows():
                    vaccine = Vaccine(
                        name=row['Vaccine name'],
                        edition_date=row['Edition Date'],
                        edition_status=row['Edition Status'],
                        last_updated_date=row['Last Updated Date'],
                        price=row['price']  # Modify this according to your Excel column name
                    )
                    vaccine.save()

                # Set the flag to indicate that the data has been loaded
                settings.VACCINES_DATA_LOADED = True
               
                message = "Vaccines loaded successfully."
                return render(request, 'upload_excel.html', {'message': message, 'alert_type': 'success'})
            except Exception as e:
                message = "An error occurred: " + str(e)
                return render(request, 'upload_excel.html', {'message': message, 'alert_type': 'danger'})
        else:
            message = "Vaccines already loaded."
            return render(request, 'upload_excel.html', {'message': message, 'alert_type': 'warning'})
    else:
        return render(request, 'upload_excel.html')



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from .models import Vaccine, Company, CartItem


@login_required
def view_available_vaccines(request):
    user = request.user
    if user.is_admin:  # Assuming you have a field 'is_admin' in your CustomUser model
        # Admin can view all available vaccines
        vaccines = Vaccine.objects.all()
        return render(request, 'view_available_vaccines.html', {'vaccines': vaccines})
    elif user.company:
        # Users associated with a company can view available vaccines
        vaccines = Vaccine.objects.all()
        return render(request, 'view_available_vaccines.html', {'vaccines': vaccines})
    else:
        # Users not associated with any company are not authorized to view vaccines
        messages.error(request, 'You are not associated with a licensed company.')
        return redirect('home')  # Redirect to home page or any other appropriate page



def view_vaccine(request):
    user = request.user
    if user.is_admin:  # Assuming you have a field 'is_admin' in your CustomUser model
        # Admin can view all available vaccines
        vaccines = Vaccine.objects.all()
        return render(request, 'view_vaccine.html', {'vaccines': vaccines})
    else:
        return redirect('home') 
    return render(request , 'view_vaccine.html')




def add_to_cart(request, vaccine_id):
    vaccine = get_object_or_404(Vaccine, pk=vaccine_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        user = request.user
        # Create or update the cart item for the user and vaccine
        cart_item, created = CartItem.objects.get_or_create(user=user, vaccine=vaccine)
        cart_item.quantity += quantity
        cart_item.save()
        return redirect('view_cart')
    return render(request, 'add_to_cart.html', {'vaccine': vaccine})
 


def update_cart(request):
    if request.method == 'POST':
        vaccine_id = request.POST.get('vaccine_id')
        action = request.POST.get('action')

        # Retrieve the cart item from the database
        cart_item = get_object_or_404(CartItem, vaccine__id=vaccine_id, user=request.user)

        # Update the quantity based on the action
        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                # If quantity is already 1, delete the cart item
                cart_item.delete()

        # Save the updated cart item
        cart_item.save()

    return redirect('view_cart')

def remove_from_cart(request):
    if request.method == 'POST':
        # Retrieve the vaccine ID from the form data
        vaccine_id = request.POST.get('vaccine_id')

        # Retrieve the corresponding cart item from the database
        cart_item = get_object_or_404(CartItem, vaccine_id=vaccine_id, user=request.user)

        # Remove the cart item from the cart
        cart_item.delete()

        messages.success(request, "Item removed from the cart successfully.")
        return redirect('view_cart')  # Redirect back to the cart page
    else:
        # If the request method is not POST, redirect to a suitable page
        return redirect('view_cart')  # Redirect to the cart page or another page as needed


def delete_vaccine(request, vaccine_id):
    # Retrieve the vaccine object
    vaccine = get_object_or_404(Vaccine, pk=vaccine_id)
    
    # Check if the requesting user is a company user
    if request.user.company:
        # Delete the vaccine
        vaccine.delete()
        messages.success(request, 'Vaccine deleted successfully.')
    else:
        # If the user is not a company user, display an error message
        messages.error(request, 'You are not authorized to delete vaccines.')
    
    # Redirect back to the view_available_vaccine page or any other appropriate page
    return redirect('view_available_vaccines')




def view_cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    total_price = Decimal(0)  # Initialize total price as Decimal
    for cart_item in cart_items:
        total_price += cart_item.subtotal
    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vaccine, Checkout, CartItem, CheckoutItem
from decimal import Decimal
import razorpay

@login_required
def checkout(request):
    if request.method == 'POST':
        # Retrieve the user's cart items
        cart_items = CartItem.objects.filter(user=request.user)
        
        # Calculate total price
        total_price = sum(item.subtotal for item in cart_items)

        # Extract shipping information from the form
        full_name = request.POST.get('full_name')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2', '')  # Optional field
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin_code = request.POST.get('pin_code')
        phone_number = request.POST.get('phone_number')

        # Save checkout information
        checkout = Checkout.objects.create(
            user=request.user,
            full_name=full_name,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            pin_code=pin_code,
            phone_number=phone_number
        )

        for item in cart_items:
            CheckoutItem.objects.create(
                checkout=checkout,
                vaccine=item.vaccine,
                quantity=item.quantity,
                subtotal=item.subtotal
            )

        # Clear the user's cart after checkout
        cart_items.delete()

        # Redirect to a thank you page or order summary page
        return redirect('order_confirm', checkout_id=checkout.id)  # Replace 'order_summary' with your actual view name
    else:
        # If the request method is GET, retrieve cart items and calculate total price
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.subtotal for item in cart_items)

        # Pass cart items and total price to the template
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }

        return render(request, 'checkout.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Checkout, CheckoutItem

def order_confirm(request, checkout_id):
    try:
        # Retrieve the checkout information using the provided checkout_id
        checkout = get_object_or_404(Checkout, pk=checkout_id)

        # Retrieve checkout items associated with the checkout
        checkout_items = checkout.items.all()

        # Calculate total price from checkout items
        total_price = sum(item.subtotal for item in checkout_items)

        context = {
            'checkout': checkout,
            'checkout_items': checkout_items,
            'total_price': total_price,
        }
        return render(request, 'order_confirm.html', context)
    except Checkout.DoesNotExist:
        messages.error(request, "No checkout information found. Please complete the checkout process first.")
        return redirect('view_cart')  # Redirect to the cart page
        

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vaccine, Payment
from .forms import PaymentForm  # Import PaymentForm if you have one
from decimal import Decimal
import razorpay

@login_required
def process_payment(request):
    if request.method == 'POST':
        # Retrieve the user's cart items
        cart_items = CartItem.objects.filter(user=request.user)
        
        # Calculate total price
        total_price = sum(item.subtotal for item in cart_items)

        # Ensure total price is at least 1.00 INR
        if total_price < Decimal('1.00'):
            messages.error(request, "Total amount must be at least INR 1.00.")
            return redirect('view_cart')

        # Initialize Razorpay client
        client = razorpay.Client(auth=("rzp_test_EZL2rQubxJwxrv", "RhRefR6hrzAdlzxNVUm6s4Ja")) 

        # Convert total price to paise
        amount_in_paise = int(total_price * 100)

        # Create payment order
        data = {
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": "vaccine_order",
            "notes": {
                "description": "Payment for vaccine purchase"
            }
        }

        try:
            payment = client.order.create(data=data)

            # Save payment details in the database
            Payment.objects.create(user=request.user, amount=total_price, vaccine=None)  # Assuming no specific vaccine is being purchased

            # Render the checkout page with payment details
            return render(request, 'process_payment.html', {'amount': amount_in_paise, 'payment': payment})

        except Exception as e:
            # Handle payment processing errors
            messages.error(request, f"Payment processing error: {str(e)}")
            return redirect('view_cart')

    else:
        # If request method is not POST, redirect to the cart
        return redirect('view_cart')



    







def purchase_success(request):
    return render(request, 'purchase_success.html')



# views.py
from django.shortcuts import render, redirect
from .models import Company

def register_company(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        license_number = request.POST.get('license_number')
        address = request.POST.get('address')
        contact_email = request.POST.get('contact_email')
        contact_phone = request.POST.get('contact_phone')
        Company.objects.create(
            name=name,
            license_number=license_number,
            address=address,
            contact_email=contact_email,
            contact_phone=contact_phone
        )
        return redirect('adminreg')
    return render(request, 'register_company.html')

# def company_list(request):
#     companies = Company.objects.all()
#     return render(request, 'company_list.html', {'companies': companies})


from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Company  # Import the Company model

User = get_user_model()

def generate_password_company(request, company_id):
    if request.method == 'POST':
        # Retrieve the company from the database
        company = Company.objects.get(id=company_id)

        # Check if the email is unique
        try:
            user = User.objects.get(email=company.contact_email)
            messages.error(request, 'Email already in use by another user.')
        except User.DoesNotExist:
            # Create a new user (company) with the company's details
            user = User(
                first_name=company.name,  # Use company name as first name
                email=company.contact_email,
                phone=company.contact_phone,
                role='Company',  # Make sure to set the appropriate role
            )

            # Generate a password (replace with your password generation logic)
            password = 'Qwer123@'
            user.set_password(password)
            user.save()

            # Send an email with the generated password
            subject = 'Your Company Account Password'
            message = render_to_string('password_email.html', {'password': password})
            from_email = 'kiddoguard12@gmail.com'  # Replace with your email address
            recipient_list = [company.contact_email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            messages.success(request, 'Company approved and password set.')

    return redirect('adminreg')



# def upload_excel(request):
#     return render(request, 'upload_excel.html')


# from django.shortcuts import render
# from .models import Company

# def company_details(request):
#     # Assuming each user is associated with a company, get the company for the logged-in user
#     user_company = request.user.company  # Assuming user has a ForeignKey to Company model

#     # Pass the company details to the template context
#     context = {
#         'user_company': user_company
#     }

#     return render(request, 'company_details.html', context)

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .models import Company

@login_required
def company_profile(request):
    company = request.user.company
    profile_updated = False  # Initialize the variable

    if request.method == 'POST':
        # Handle profile update
        company.name = request.POST.get('name', '')
        company.email = request.POST.get('email', '')
        company.phone = request.POST.get('phone', '')
        company.address = request.POST.get('address', '')

        # Handle logo upload
        logo = request.FILES.get('logo')
        if logo:
            # If a new logo is provided, save it and update the company's logo field
            logo_name = default_storage.save(f'company/logos/{request.user.company.id}/{logo.name}', logo)
            company.logo = logo_name
        company.save()

        # Fetch the updated data from the database
        company = Company.objects.get(id=company.id)

        profile_updated = True

    return render(request, 'company_profile.html', {'company': company, 'profile_updated': profile_updated})

from django.views.decorators.cache import cache_control
from .models import VaccineSchedule
import pandas as pd
from django.conf import settings

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required
def load_vaccine_schedule(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']

        # Check if the data has already been loaded
        if not settings.VACCINES_LOADED:
            try:
                # Read the Excel file into a pandas DataFrame
                excel_data = pd.read_excel(excel_file)
                
                # Iterate over DataFrame rows and create VaccineSchedule instances
                for index, row in excel_data.iterrows():
                    vaccine_schedule = VaccineSchedule(
                        age=row['Age'],
                        vaccine_name=row['vaccine_name']  # Modify this according to your Excel column name
                    )
                    vaccine_schedule.save()

                # Set the flag to indicate that the data has been loaded
                settings.VACCINES_LOADED = True
               
                message = "Vaccine schedule loaded successfully."
                return render(request, 'load_vaccine_schedule.html', {'message': message, 'alert_type': 'success'})
            except Exception as e:
                message = "An error occurred: " + str(e)
                return render(request, 'load_vaccine_schedule.html', {'message': message, 'alert_type': 'danger'})
        else:
            message = "Vaccine schedule already loaded."
            return render(request, 'load_vaccine_schedule.html', {'message': message, 'alert_type': 'warning'})
    else:
        return render(request, 'load_vaccine_schedule.html')




from twilio.rest import Client

def send_sms_message(from_number,to_number, message):
    # Twilio credentials
    account_sid = 'AC7d7c9edfde803bcd999874095eb3f336'
    auth_token = '6b891fa2ed585cfa969166bec347172c'
    

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    try:
        # Send WhatsApp message
        message = client.messages.create(
            body=message,
            from_=from_number,  # Your Twilio phone number
            to=to_number  # Recipient's phone number
        )
        return True, message.sid
    except Exception as e:
        print(f"Failed to send  message: {e}")
        return False, None
        

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import BirthDetails, VaccinationSlot
from datetime import date
from . import utils

@login_required
def schedule_vaccination(request, child_id):
    vaccines = []

    if request.method == 'POST':
        # Extract form data
        booking_date = request.POST.get('booking_date')
        slot = request.POST.get('slot')
        recipient_phone = request.POST.get('recipient_phone')
        pass
    
        if not child_id or not booking_date or not slot or not recipient_phone:
            return JsonResponse({'message': 'All fields are required.'})

        try:
            child = BirthDetails.objects.get(id=child_id)
            age = utils.calculate_age(child.date_of_birth)
            vaccines = utils.get_vaccines_for_age(age)
        except BirthDetails.DoesNotExist:
            return JsonResponse({'message': 'Invalid child selected.'})

        # Check if the slot is available
        if VaccinationSlot.objects.filter(booking_date=booking_date, slot=slot).exists():
            return JsonResponse({'message': 'Slot is already booked. Please choose a different slot.'})


        # Book the slot
        slot_obj = VaccinationSlot(child=child, booking_date=booking_date, slot=slot, recipient_phone=recipient_phone)
        slot_obj.save()

        # Send SMS reminder
        from_number = '+19382533475'
        success, message_id = send_sms_message(from_number, recipient_phone, 'Your vaccination slot has been booked successfully.')

        if success:
            return JsonResponse({'success': True, 'message': 'Vaccination slot booked successfully.', 'message_id': message_id})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to send  message.'})
    
    else:
        if not child_id:
            return JsonResponse({'message': 'Child ID not provided.'})

        try:
            child = BirthDetails.objects.get(id=child_id)
            age = utils.calculate_age(child.date_of_birth)
            vaccines = utils.get_vaccines_for_age(age)
        except BirthDetails.DoesNotExist:
            return JsonResponse({'message': 'Invalid child selected.'})

        current_date = date.today().strftime('%Y-%m-%d')
        

        return render(request, 'schedule_vaccination.html', {'child': child, 'vaccines': vaccines, 'current_date': current_date, 'child_id': child_id})




def view_booking(request, slot_id):
    try:
        booking = VaccinationSlot.objects.get(pk=slot_id)
    except VaccinationSlot.DoesNotExist:
        # Handle case where booking does not exist
        return JsonResponse({'message': 'Invalid booking ID.'}, status=404)

    return render(request, 'view_booking.html', {'booking': booking})



def cancel_vaccination_slot(request, slot_id):
    try:
        slot = VaccinationSlot.objects.get(pk=slot_id)
        slot.delete()
        return JsonResponse({ 'message': 'Vaccination slot Cancelled successfully.'})
    except VaccinationSlot.DoesNotExist:
        messages.error(request, "Invalid slot ID.")

    return redirect('view_booking', slot_id=slot_id)


def reschedule_vaccination_slot(request, slot_id):
    if request.method == 'POST':
        new_date = request.POST.get('new_date')
        new_slot = request.POST.get('new_slot')

        try:
            slot = VaccinationSlot.objects.get(pk=slot_id)
            slot.slot.date = new_date
            slot.slot.slot_time = new_slot
            slot.slot.save()
            return JsonResponse({ 'message': 'Vaccination slot rescheduled successfully.'})
        except VaccinationSlot.DoesNotExist:
            messages.error(request, "Invalid slot ID.")

        return redirect('view_booking', slot_id=slot_id)
    else:
        current_date = datetime.now().strftime('%Y-%m-%d')  # Get current date in 'YYYY-MM-DD' format
        return render(request, 'reschedule_vaccination_slot.html', {'slot_id': slot_id, 'current_date': current_date})


from django.shortcuts import render
from .models import VaccinationSlot

def view_vaccination_slots(request):
    # Fetch all booked vaccination slots
    vaccination_slots = VaccinationSlot.objects.all()
    return render(request, 'view_vaccination_slots.html', {'vaccination_slots': vaccination_slots})

def update_vaccine_status(request, slot_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        try:
            slot = VaccinationSlot.objects.get(pk=slot_id)
            slot.status = status
            slot.save()
            return JsonResponse({'success': True, 'message': 'Vaccine status updated successfully.'})
        except VaccinationSlot.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Vaccination slot not found.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def view_slot_status(request, slot_id):
    slot = get_object_or_404(VaccinationSlot, pk=slot_id)
    return render(request, 'view_slot_status.html', {'slot': slot})





# from django.shortcuts import render
# from django.http import HttpResponse
# from .utils import calculate_bmi,calculate_weight_status, calculate_z_score, calculate_weight_gain_rate
# from sklearn.ensemble import RandomForestClassifier

# from .utils import y_train, X_train

# rf_model = RandomForestClassifier(random_state=42)
# rf_model.fit(X_train, y_train)


# def homes(request):
#     return render(request, 'ml_predictor/indexes.html')

# def predict(request):
#     if request.method == 'POST':
#         # Get form data
#         bmdstats = float(request.POST.get('bmdstats'))
#         riagendr = float(request.POST.get('riagendr'))
#         ridageyr = float(request.POST.get('ridageyr'))
#         bmxwt = float(request.POST.get('bmxwt'))
#         bhxht = float(request.POST.get('bhxht'))
#         bmxleg = float(request.POST.get('bmxleg'))
#         boxarml = float(request.POST.get('boxarml'))
#         bmxarmc = float(request.POST.get('bmxarmc'))
#         bmxwaist = float(request.POST.get('bmxwaist'))
#         bmxhip = float(request.POST.get('bmxhip'))

#         features = [bmdstats, riagendr, ridageyr, bmxwt, bhxht, bmxleg, boxarml, bmxarmc, bmxwaist, bmxhip]

#         # Make prediction using the trained model
#         prediction = rf_model.predict([features])[0]

#         bmi = calculate_bmi(bmxwt, bhxht)

#         weight_status = calculate_weight_status(bmi, ridageyr, riagendr)

#         # Calculate z-score (assuming parameters for z-score calculation)
#         z_score = calculate_z_score(bmdstats, mean=50, std_dev=5)

#         # Calculate weight gain rate (assuming parameters for weight gain rate calculation)
#         weight_initial = 10  # Initial weight measurement (e.g., at birth)
#         weight_final = bmxwt  # Final weight measurement
#         time_period = 1  # Time period in months
#         weight_gain_rate = calculate_weight_gain_rate(weight_initial, weight_final, time_period)


#         # Render result template with prediction and other calculated values
#         return render(request, 'ml_predictor/result.html', {'prediction': prediction, 'bmi': bmi,'weight_status': weight_status, 'z_score': z_score, 'weight_gain_rate': weight_gain_rate})

#     else:
#         return HttpResponse("Method not allowed")




























#@login_required
#def approve_doctor(request, doctor_id):
#    doctor = Doctor.objects.get(id=doctor_id)
 #   doctor.user = CustomUser.objects.create(
 #       email=doctor.email,
 #       role='Doctor',
 #       is_active=False  # Inactive until approved
 #   )
 #   doctor.user.set_unusable_password()  # Set an unusable password
 #   doctor.user.save()
  #  doctor.approved = True
  #  doctor.save() 

    # Send a registration link to the doctor
   # current_site = get_current_site(request)
    #subject = 'Doctor Registration Link'
    #message = 'Your doctor registration has been approved. Please complete your registration by clicking the link below.'
    #from_email = 'kiddoguard12@gmail.com'  # Replace with your email
   # recipient_list = [doctor.email] 
    #html_message = render_to_string('registration_link_email.html', {
      #  'user': doctor.user,
      ##  'domain': current_site.domain,
      #  'uid': urlsafe_base64_encode(force_bytes(doctor.user.pk)),
      #  'token': default_token_generator.make_token(doctor.user),
   # })

   # send_mail(subject, message, from_email, recipient_list, html_message=html_message)

   # messages.success(request, "Doctor registration approved. Registration link sent to the doctor's email.")
   # return redirect('adminreg')

#from django.contrib.auth.tokens import default_token_generator
#from django.contrib.auth import get_user_model, login
#from django.contrib.auth.decorators import login_required
#from django.contrib.sites.shortcuts import get_current_site
#from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
#from django.shortcuts import render, redirect
#from django.contrib import messages

# ... (other imports)

#def doctor_registration_complete(request, uidb64, token):
  #  User = get_user_model()
  #  try:
 #       uid = force_text(urlsafe_base64_decode(uidb64))
  #      user = User.objects.get(pk=uid)
  #  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
   #     user = None

  #  if user is not None and default_token_generator.check_token(user, token):
    #    user.is_active = True
    #    user.save()

        # Log in the user
     #   auth_login(request, user)
     #   messages.success(request, "Doctor registration is complete. You are now logged in.")
      #  return redirect('homepage')
    #else:
     #   messages.error(request, "Doctor registration link is invalid or has expired.")
     #   return redirect('login')








    



# def logout(request):
#     return render(request, 'login.html')
# def logout(request):
#      if request.user.is_authenticated:
#       auth_logout(request) # Use the logout function to log the user out
#      return redirect('login')  # Redirect to the confirmation page

# def ChangePassword(request, token):
#     context = {}

#     try:
#         profile_obj = CustomUser.objects.filter(forget_password_token=token).first()

#         if profile_obj is None:
#             messages.success(request, 'Invalid token.')
#             return redirect('/forget-password/')

#         if request.method == 'POST':
#             new_password = request.POST.get('new_password')
#             confirm_password = request.POST.get('reconfirm_password')

#             if new_password != confirm_password:
#                 messages.success(request, 'Passwords do not match.')
#                 return redirect(f'/change-password/{token}/')

#             # Update the password for the user associated with profile_obj
#             profile_obj.set_password(new_password)
#             profile_obj.forget_password_token = None  # Remove the token
#             profile_obj.save()
#             return redirect('/login/')

#     except Exception as e:
#         print(e)
    
#     return render(request, 'change-password.html', context)


# import uuid
# def ForgetPassword(request):
#     try:
#         if request.method == 'POST':
#             username = request.POST.get('username')
            
#             user_obj = CustomUser.objects.filter(username=username).first()
            
#             if user_obj is None:
#                 messages.error(request, 'No user found with this username.')
#                 return redirect('/forget-password/')
            
#             token = str(uuid.uuid4())
#             user_obj.forget_password_token = token
#             user_obj.save()
#             send_forget_password_mail(user_obj.email, token)
#             messages.success(request, 'An email has been sent with instructions to reset your password.')
#             return redirect('/forget-password/')
    
#     except Exception as e:
#         print(e)
    
#     return render(request, 'forget-password.html')

# def patient_profile(request):
#     patient = request.user
    
#     if request.method == 'POST':
#         form = PatientProfileForm(request.POST, instance=patient)
#         if form.is_valid():
#             form.save()
#     else:
#         form = PatientProfileForm(instance=patient)

#     return render(request, 'patient_profile.html', {'patient': patient, 'form': form})