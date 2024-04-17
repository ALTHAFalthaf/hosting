from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
#from django.contrib.auth import views as auth_views
from .import views
from .views import book_appointment
from .views import appointment_confirmation
#from .views import add_vaccine, schedule_vaccination, record_vaccine_administration
#from .views import export_vaccine_records_to_excel
from .views import doctor_appointments,doctor_profile

from .views import check_time_availability
from .views import payment_success
from .views import appointment_history
from .views import contact
from .views import upload_birth_details
# from .views import birth_details_list
# from .views import view_birth_details
from .views import Company
from .views import Checkout
from .views import CheckoutItem
from .views import process_payment














from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
   path('',views.index,name='index'),
   path('signup', views.signup, name='signup'),
   path('signup/healthcare_provider/', views.signup_healthcare_provider, name='signup_healthcare_provider'),
   path('login', views.loginn, name='login'),
   path('homepage/', views.homepage, name='homepage'),
   path('logout', views.user_logout, name='logout'),
   path('about/', views.about, name='about'),
   path('contact/', views.contact, name='contact'),
   path('adminreg',views.adminreg, name='adminreg'),
   path('myprofile',views.myprofile, name='myprofile'),
   path('editprofile',views.editprofile, name='editprofile'),
   path('send_registration_email/', views.send_registration_email, name='send_registration_email'),
   path('doctor_added/', views.doctor_added, name='doctor_added'),
   path('view_doctor/', views.view_doctor, name='view_doctor'),
   path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
   path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
   path('doctor_list/', views.doctor_list, name='doctor_list'),
   path('doctor_registration/', views.doctor_registration, name='doctor_registration'),
   path('approve_doctor/<int:doctor_id>/', views.approve_doctor, name='approve_doctor'),
   path('book_appointment/<int:doctor_id>/', book_appointment, name='book_appointment'),
   path('appointment_confirmation/<int:appointment_id>/', appointment_confirmation, name='appointment_confirmation'),

   path('doctor_home/', views.doctor_home, name='doctor_home'),
   path('doctor_appointments/', doctor_appointments, name='doctor_appointments'),

   path('clear_appointments/', views.clear_appointments, name='clear_appointments'),

   
   path('prescribe_vaccines/<int:appointment_id>/', views.prescribe_vaccines, name='prescribe_vaccines'),

   path('doctor_profile/', views.doctor_profile, name='doctor_profile'),
   path('change_password/', views.change_password, name='change_password'),

   path('healthcareprovider_home/', views.healthcareprovider_home, name='healthcareprovider_home'),
   

   path('check_time_availability/', check_time_availability, name='check_time_availability'),
   
   path('vaccination_home/', views.vaccination_home, name='vaccination_home'),

   path('vaccine_record/', views.vaccine_record, name='vaccine_record'),

   path('upload-birth-details/', upload_birth_details, name='upload_birth_details'),

   path('payment_success/', views.payment_success, name='payment_success'),
   

   path('appointment_history', appointment_history, name='appointment_history'),
   path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),

   path('generate_password_provider/<int:provider_id>/', views.generate_password_provider, name='generate_password_provider'),

   # path('birth-details/list/', birth_details_list, name='birth_details_list'),

   # path('view-birth-details/<int:user_profile_id>/', views.view_birth_details, name='view_birth_details'),

   # path('download-csv/', views.download_csv, name='download_csv'),
   

   path('view-available-vaccines/', views.view_available_vaccines, name='view_available_vaccines'),

   path('view-vaccine/', views.view_vaccine, name='view_vaccine'),

   path('add-to-cart/<int:vaccine_id>/', views.add_to_cart, name='add_to_cart'),
   path('view-cart/', views.view_cart, name='view_cart'),
   path('update-cart/', views.update_cart, name='update_cart'),

   path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),

   path('checkout/', views.checkout, name='checkout'),

   path('order_confirm/<int:checkout_id>/', views.order_confirm, name='order_confirm'),



   
   # path('purchase-success/', views.purchase_success, name='purchase_success'),

   path('register/', views.register_company, name='register_company'),
   path('generate_password_company/<int:company_id>/', views.generate_password_company, name='generate_password_company'),
   path('approve-company/<int:company_id>/', views.approve_company, name='approve_company'),
   # In urls.py
   path('deactivate_company/<int:company_id>/', views.deactivate_company, name='deactivate_company'),

   path('company/home/', views.company_home, name='company_home'),
   # path('company_details/', views.company_details, name='company_details'),
   path('company_profile/', views.company_profile, name='company_profile'),

   path('upload-excel/', views.upload_excel, name='upload_excel'),

    path('load_vaccine_schedule/', views.load_vaccine_schedule, name='load_vaccine_schedule'),

   path('delete-vaccine/<int:vaccine_id>/', views.delete_vaccine, name='delete_vaccine'),


   path('process-payment/', views.process_payment, name='process_payment'),

   
   
   path('schedule/<int:child_id>/', views.schedule_vaccination, name='schedule_vaccination'),
   
 

   # path('book-vaccination-slot/', views.book_vaccination_slot, name='book_vaccination_slot'),
   path('view-booking/<int:slot_id>/', views.view_booking, name='view_booking'),
   path('cancel-slot/<int:slot_id>/', views.cancel_vaccination_slot, name='cancel_vaccination_slot'),
   path('reschedule-slot/<int:slot_id>/', views.reschedule_vaccination_slot, name='reschedule_vaccination_slot'),
   
   path('generate-prescription-pdf/<int:appointment_id>/', views.generate_prescription_pdf, name='generate_prescription_pdf'),

   path('view-vaccination-slots/', views.view_vaccination_slots, name='view_vaccination_slots'),
   path('update-vaccine-status/<int:slot_id>/', views.update_vaccine_status, name='update_vaccine_status'),
   path('view-slot-status/<int:slot_id>/', views.view_slot_status, name='view_slot_status'),


   # path('api/booked-slots/', views.get_booked_slots, name='get_booked_slots'),
   
   path('indexes/', views.homes, name='homes'),
   path('predict/', views.predict, name='predict'),
   
   
   # path('list/', views.company_list, name='company_list'),

  

   




   
   



#forgot_password code
   path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
   path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)