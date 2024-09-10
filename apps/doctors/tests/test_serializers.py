from django.test import TestCase
from django.utils import timezone
from apps.doctors.models import Doctor, Patient, Appointment
from apps.doctors.serializers import (
    DoctorCreateSerializer,
    DoctorLoginSerializer,
    DoctorProfileSerializer,
    PatientCreationSerializer,
    PatientSerializer,
    AppointmentSerializer,
)
from rest_framework.exceptions import ValidationError


class DoctorCreateSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }
        self.invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "confirm_password": "password321",
        }

    def test_valid_data(self):
        serializer = DoctorCreateSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        doctor = serializer.save()
        self.assertEqual(doctor.email, self.valid_data["email"])

    def test_invalid_data(self):
        serializer = DoctorCreateSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)


class DoctorLoginSerializerTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(
            email="doctor@example.com",
            first_name="Doctor",
            last_name="Example",
            password="password123",
        )

    def test_valid_login(self):
        serializer = DoctorLoginSerializer(data={"email": "doctor@example.com", "password": "password123"})
        self.assertTrue(serializer.is_valid())

    def test_invalid_login(self):
        serializer = DoctorLoginSerializer(data={"email": "doctor@example.com", "password": "wrongpassword"})
        self.assertTrue(serializer.is_valid())  # Serializer does not validate credentials


class DoctorProfileSerializerTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(
            email="doctor@example.com",
            first_name="Doctor",
            last_name="Example",
            password="password123",
            phone_number="+1234567890",
            address="123 Main St",
        )

    def test_profile_data(self):
        serializer = DoctorProfileSerializer(instance=self.doctor)
        self.assertEqual(serializer.data["first_name"], self.doctor.first_name)
        self.assertEqual(serializer.data["last_name"], self.doctor.last_name)
        self.assertEqual(serializer.data["email"], self.doctor.email)
        self.assertEqual(serializer.data["phone_number"], self.doctor.phone_number)
        self.assertEqual(serializer.data["address"], self.doctor.address)


class PatientCreationSerializerTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(
            email="doctor@example.com",
            first_name="Doctor",
            last_name="Example",
            password="password123",
        )
        self.valid_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "password123",
        }

    def test_create_patient(self):
        serializer = PatientCreationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        patient = serializer.save(created_by=self.doctor)
        self.assertEqual(patient.email, self.valid_data["email"])
        self.assertEqual(patient.created_by, self.doctor)


class PatientSerializerTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(
            email="doctor@example.com",
            first_name="Doctor",
            last_name="Example",
            password="password123",
        )
        self.patient = Patient.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            password="password123",
            created_by=self.doctor,
        )

    def test_patient_data(self):
        serializer = PatientSerializer(instance=self.patient)
        self.assertEqual(serializer.data["first_name"], self.patient.first_name)
        self.assertEqual(serializer.data["last_name"], self.patient.last_name)
        self.assertEqual(serializer.data["email"], self.patient.email)
        #self.assertEqual(serializer.data["password"], self.patient.password)
        self.assertEqual(serializer.data["created_by"], self.patient.created_by.id)


class AppointmentSerializerTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(
            email="doctor@example.com",
            first_name="Doctor",
            last_name="Example",
            password="password123",
        )
        self.patient = Patient.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            password="password123",
            created_by=self.doctor,
        )
        self.appointment_data = {
            "doctor": self.doctor.id,
            "patient": self.patient.id,
            "date": timezone.now().date(),
            "time": timezone.now().time(),
            "status": "scheduled",
            "reason": "Routine check-up",
        }

    def test_create_appointment(self):
        serializer = AppointmentSerializer(data=self.appointment_data)
        self.assertTrue(serializer.is_valid())
        appointment = serializer.save()
        self.assertEqual(appointment.patient, self.patient)
        self.assertEqual(appointment.doctor, self.doctor)

    def test_appointment_invalid_status(self):
        invalid_data = self.appointment_data.copy()
        invalid_data["status"] = "unknown"
        serializer = AppointmentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)
