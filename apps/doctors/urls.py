from django.urls import path
from apps.doctors.views import (
    DoctorRegisterView,
    DoctorLoginView,
    DoctorProfileView,
    PatientCreateView,
    PatientListView,
    PatientDetailView,
    DoctorAppointmentsListView,
    AppointmentUpdateView
)

urlpatterns = [
    # Doctor Endpoints
    path('api/doctors/signup/', DoctorRegisterView.as_view(), name='doctor-signup'),
    path('api/doctors/login/', DoctorLoginView.as_view(), name='doctor-login'),
    path('api/doctors/profile/', DoctorProfileView.as_view(), name='doctor-profile'),
    path('api/doctors/profile/update/', DoctorProfileView.as_view(), name='doctor-profile-update'),

    # Patient Endpoints
    path('api/doctors/patients/create/', PatientCreateView.as_view(), name='create-patient'),
    path('api/doctors/patients/', PatientListView.as_view(), name='list-patients'),
    path('api/doctors/patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),

    # Appointment Endpoints
    path('api/doctors/appointments/', DoctorAppointmentsListView.as_view(), name='list-appointments'),
    path('api/doctors/appointments/<int:pk>/update/', AppointmentUpdateView.as_view(), name='update-appointment'),
]
