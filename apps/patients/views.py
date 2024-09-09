
from django.contrib.auth import authenticate, login
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import Patient
from .serializers import PatientSerializer, PatientLoginSerializer, PatientProfileSerializer, PatientAppointmentSerializer
from .permissions import IsOwner
from apps.doctors.models import Appointment
from apps.doctors.serializers import AppointmentSerializer

class PatientLoginView(APIView):
    """
    Patient login view to authenticate and log in patients using email and password.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PatientLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Authenticate the patient
        patient = authenticate(request, email=email, password=password)

        if patient is not None:
            # Log the patient in
            login(request, patient)

            # Create or get an authentication token for the patient
            token, created = Token.objects.get_or_create(user=patient)

            # Return the token and patient details
            return Response(
                {
                    'token': token.key,
                    'patient': PatientProfileSerializer(patient).data
                },
                status=status.HTTP_200_OK
            )
        else:
            # Invalid credentials provided
            return Response(
                {'error': 'Invalid email or password'},
                status=status.HTTP_400_BAD_REQUEST
            )


class PatientProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the logged-in patient's profile.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user


class PatientAppointmentsView(generics.ListCreateAPIView):
    """
    List all appointments of the logged-in patient or book a new appointment.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Return the logged-in patient's appointments
        return Appointment.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the patient to the logged-in user
        serializer.save(patient=self.request.user)


class PatientAppointmentDetailView(generics.RetrieveAPIView):
    """
    Retrieve details of a specific appointment for the logged-in patient.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Ensure the patient can only access their own appointments
        return Appointment.objects.filter(patient=self.request.user)
