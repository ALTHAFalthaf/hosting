from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib import admin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None,dob=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role,dob=dob, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password=None, role='Admin',dob=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, role=role,dob=dob, **extra_fields)  
    

class CustomUser(AbstractUser):
    ADMIN = 'Admin'
    CHILD = 'Child'
    DOCTOR = 'Doctor'
    HEALTHCARE_PROVIDER = 'HealthcareProvider'  # New role for healthcare providers
    COMPANY= 'Company'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CHILD, 'Child'),
        (DOCTOR, 'Doctor'),
        (HEALTHCARE_PROVIDER, 'HealthcareProvider'),  # Add Healthcare Provider to role choices
        (COMPANY, 'Company')
    ]


    GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
    )

    # Fields for custom user roles
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=CHILD)  # Default role for regular users
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True)
    provider = models.ForeignKey('HealthcareProvider', on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True)
    forget_password_token = models.UUIDField(null=True, blank=True) #forgetpass
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=15)
    objects = CustomUserManager()
    username = models.CharField(max_length=150, unique=False)
    # Define boolean fields for specific roles
    is_admin = models.BooleanField(default=True)
    is_child = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=True)
    is_healthcare_provider = models.BooleanField(default=True)  # New field to indicate healthcare provider role
    is_company = models.BooleanField(default=True) 


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email 





class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile', null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    certification = models.CharField(max_length=100, null=True, blank=True)
    resume = models.FileField(upload_to='doctor/resume/', null=True, blank=True)
    license_copy = models.FileField(upload_to='doctor/license_copy/', null=True, blank=True)
    photo = models.ImageField(upload_to='doctor/photo/', null=True, blank=True)
    approved = models.BooleanField(default=False)  # You can set the default value as needed


    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class BirthDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_details',null=True, blank=True)
    child_fname = models.CharField(max_length=100, null=True, blank=True)
    child_lname = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    place_of_birth = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # Using DecimalField for precision
    height = models.DecimalField(max_digits=5, decimal_places=2)  # Using DecimalField for precision
    regno = models.CharField(max_length=50, unique=True)
    rchid = models.CharField(max_length=50)
    age = models.PositiveIntegerField()  # Age in years

    

    def __str__(self):
        return self.child_name      

 

class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_appointments',default=1)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments', default=1)  # Replace '1' with the default doctor's ID
    child = models.ForeignKey(BirthDetails, on_delete=models.CASCADE, related_name='child_appointments',default=1)  # New field for child
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    description = models.TextField( null=True, blank=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with {self.doctor.first_name} {self.doctor.last_name} on {self.appointment_date}"

class HealthcareProvider(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='healthcare_provider_profile', null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone= models.CharField(max_length=15, blank=True, null=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    certification = models.CharField(max_length=100, null=True, blank=True)
    resume = models.FileField(upload_to='provider/resume/', null=True, blank=True)
    license_copy = models.FileField(upload_to='provider/license_copy/', null=True, blank=True)
    photo = models.ImageField(upload_to='provider/photo/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    # Add more fields as needed
   
    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Vaccine(models.Model):
    name = models.CharField(max_length=200,null=True, blank=True)
    #manufacturer = models.CharField(max_length=100)
    edition_date = models.DateField(null=True, blank=True)
    edition_status = models.CharField(max_length=200,null=True, blank=True)
    last_updated_date = models.DateField(null=True, blank=True)
   # quantity = models.PositiveIntegerField(default=0)
   # expiration_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  

    def __str__(self):
        return self.name



class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s Cart Item - {self.vaccine.name}"

    def save(self, *args, **kwargs):
        # Calculate subtotal before saving
        self.subtotal = self.vaccine.price * self.quantity
        super().save(*args, **kwargs)



class Checkout(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkout for {self.user.email}"

class CheckoutItem(models.Model):
    checkout = models.ForeignKey(Checkout, related_name='items', on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.vaccine.name} in {self.checkout}"



class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.vaccine.name} by {self.user.username} - {self.amount}"



class VaccinePurchase(models.Model):
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE,null=True)
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    purchase_date = models.DateTimeField(default=timezone.now)
    # Add more fields as needed
   
    def __str__(self):
        return f"{self.quantity} doses of {self.vaccine.name} purchased by {self.buyer.email} on {self.purchase_date}"


class Company(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
    ]

    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return self.name


class VaccineSchedule(models.Model):
    age = models.FloatField()
    vaccine_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.age} months - {self.vaccine_name}"




class VaccinationSlot(models.Model):
    

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('given', 'Given'),
        ('cancelled', 'Cancelled'),
    ]

    

    child = models.ForeignKey(BirthDetails, on_delete=models.CASCADE)
    booking_date = models.DateField()
    slot = models.TimeField()
    recipient_phone = models.CharField(max_length=20, default='')
    is_booked = models.BooleanField(default=False)  # Field to indicate if the slot is booked or not
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.child.child_fname}'s Slot for {self.vaccine} on {self.booking_date}"






class VaccinePrescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='vaccine_prescription',null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='vaccine_prescriptions',null=True)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name='prescriptions', null=True)
    doses = models.PositiveIntegerField(default=1,null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Prescription for {self.appointment.child.child_fname} {self.appointment.child.child_lname} by Dr. {self.doctor.last_name}: {self.vaccine_name} - {self.doses} doses"


