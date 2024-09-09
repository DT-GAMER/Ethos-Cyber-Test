from django.urls import path
from .views import (
    PatientLoginView,
    PatientProfileView,
    PatientProfileView,
    PatientAppointmentsView,
    PatientAppointmentDetailView
)

urlpatterns = [
    path('login/', PatientLoginView.as_view(), name='patient-login'),
    path('profile/', PatientProfileView.as_view(), name='patient-profile'),
    path('profile/update/', PatientProfileView.as_view(), name='patient-update-profile'),
    path('appointments/book/', PatientAppointmentsView.as_view(), name='book-appointment'),
    path('appointments/', PatientAppointmentsView.as_view(), name='list-appointments'),
    path('appointments/<int:appointment_id>/', PatientAppointmentDetailView.as_view(), name='appointment-detail'),
]
