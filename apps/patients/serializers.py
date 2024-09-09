from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.doctors.models import Appointment

Patient = get_user_model()

class PatientLoginSerializer(serializers.Serializer):
    """
    Serializer for patient login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class PatientProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and updating patient profile.
    """
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'phone_number']


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving patient data.
    """
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'email']


class PatientAppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and managing patient appointments.
    """
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'date', 'time', 'status', 'reason']
