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
    path('signup', DoctorRegisterView.as_view(), name='doctor-signup'),
    path('login', DoctorLoginView.as_view(), name='doctor-login'),
    path('profile', DoctorProfileView.as_view(), name='doctor-profile'),
    path('profile/update', DoctorProfileView.as_view(), name='doctor-profile-update'),

    # Patient Endpoints
    path('patients/create', PatientCreateView.as_view(), name='create-patient'),
    path('patients', PatientListView.as_view(), name='list-patients'),
    path('patients/<int:pk>', PatientDetailView.as_view(), name='patient-detail'),

    # Appointment Endpoints
    path('appointments', DoctorAppointmentsListView.as_view(), name='list-appointments'),
    path('appointments/<int:pk>/update', AppointmentUpdateView.as_view(), name='update-appointment'),
]
