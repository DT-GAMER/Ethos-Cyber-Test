from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from apps.doctors.models import Doctor, Patient, Appointment
from apps.doctors.serializers import (
    DoctorLoginSerializer,
    DoctorCreateSerializer,
    DoctorProfileSerializer,
    PatientCreationSerializer,
    PatientSerializer,
    AppointmentSerializer,
)
from apps.doctors.permissions import IsDoctor, CanManagePatient



class DoctorRegisterView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorCreateSerializer
    permission_classes = [permissions.AllowAny]


class DoctorLoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = DoctorLoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        doctor = authenticate(email=email, password=password)
        if doctor is not None and doctor.is_active:
            refresh = RefreshToken.for_user(doctor)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class DoctorProfileView(generics.RetrieveUpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_object(self):
        return self.request.user


class PatientCreateView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientCreationSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PatientDetailView(generics.RetrieveAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsDoctor, CanManagePatient]

    def get_object(self):
        patient = super().get_object()
        if patient.created_by != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to view this patient.")
        return patient


class PatientListView(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)


class DoctorAppointmentsListView(generics.ListAPIView):
    """
    View for listing all appointments for the logged-in doctor.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user)


class AppointmentUpdateView(generics.UpdateAPIView):
    """
    View for updating or canceling an appointment by the logged-in doctor.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_object(self):
        appointment = super().get_object()
        if appointment.doctor != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to update this appointment.")
        return appointment
