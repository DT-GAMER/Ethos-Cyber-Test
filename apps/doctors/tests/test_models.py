from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from apps.doctors.models import Doctor, Patient, Appointment
from django.utils import timezone
import json

class DoctorManagerTestCase(TestCase):
    def test_create_user(self):
        Doctor = get_user_model()
        user = Doctor.objects.create_user(email='test@example.com', password='testpass123', first_name='John', last_name='Doe')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        Doctor = get_user_model()
        admin_user = Doctor.objects.create_superuser(email='admin@example.com', password='adminpass123', first_name='Admin', last_name='User')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.check_password('adminpass123'))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_create_user_without_email(self):
        Doctor = get_user_model()
        with self.assertRaises(ValueError):
            Doctor.objects.create_user(email='', password='testpass123')

class DoctorModelTestCase(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(
            email='doctor@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            phone_number='123-456-7890',
            address='123 Test St, Test City',
            specialization='General'
        )

    def test_doctor_creation(self):
        self.assertEqual(self.doctor.email, 'doctor@example.com')
        self.assertEqual(self.doctor.first_name, 'John')
        self.assertEqual(self.doctor.last_name, 'Doe')
        self.assertEqual(self.doctor.phone_number, '1234567890')
        self.assertEqual(self.doctor.address, '123 Test St, Test City')
        self.assertEqual(self.doctor.specialization, 'General')

    def test_doctor_str_method(self):
        self.assertEqual(str(self.doctor), 'John Doe (doctor@example.com)')

    def test_phone_number_formatting(self):
        self.doctor.phone_number = '(123) 456-7890'
        self.doctor.save()
        self.assertEqual(self.doctor.phone_number, '1234567890')

    def test_availability_json_field(self):
        availability = [
            {"day": "Monday", "start": "09:00", "end": "17:00"},
            {"day": "Tuesday", "start": "09:00", "end": "17:00"}
        ]
        self.doctor.availability = availability
        self.doctor.save()
        self.assertEqual(self.doctor.availability, availability)

class PatientModelTestCase(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(
            email='doctor@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.patient = Patient(
            first_name='Jane',
            last_name='Smith',
            email='patient@example.com',
            created_by=self.doctor
        )
        self.patient.raw_password = 'testpass123'
        self.patient.save()

    def test_patient_creation(self):
        self.assertEqual(self.patient.first_name, 'Jane')
        self.assertEqual(self.patient.last_name, 'Smith')
        self.assertEqual(self.patient.email, 'patient@example.com')
        self.assertEqual(self.patient.created_by, self.doctor)
        self.assertNotEqual(self.patient.password, 'testpass123')  # Password should be hashed

    def test_patient_str_method(self):
        self.assertEqual(str(self.patient), 'Jane Smith')

    def test_patient_unique_email(self):
        with self.assertRaises(IntegrityError):
            new_patient = Patient(
                first_name='Another',
                last_name='Patient',
                email='patient@example.com',
                created_by=self.doctor
            )
            new_patient.raw_password = 'testpass123'
            new_patient.save()

class AppointmentModelTestCase(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create_user(
            email='doctor@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.patient = Patient(
            first_name='Jane',
            last_name='Smith',
            email='patient@example.com',
            created_by=self.doctor
        )
        self.patient.raw_password = 'testpass123'
        self.patient.save()

        self.appointment_time = timezone.now() + timezone.timedelta(days=1)
        self.appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_time=self.appointment_time,
            reason='General checkup'
        )

    def test_appointment_creation(self):
        self.assertEqual(self.appointment.doctor, self.doctor)
        self.assertEqual(self.appointment.patient, self.patient)
        self.assertEqual(self.appointment.appointment_time, self.appointment_time)
        self.assertEqual(self.appointment.reason, 'General checkup')

    def test_appointment_str_method(self):
        expected_str = f"Appointment with Dr. Doe on {self.appointment_time}"
        self.assertEqual(str(self.appointment), expected_str)

    def test_unique_doctor_appointment_time(self):
        with self.assertRaises(IntegrityError):
            Appointment.objects.create(
                doctor=self.doctor,
                patient=self.patient,
                appointment_time=self.appointment_time,
                reason='Another appointment'
            )

    def test_multiple_appointments_same_time_different_doctors(self):
        another_doctor = Doctor.objects.create_user(
            email='another_doctor@example.com',
            password='testpass123',
            first_name='Jane',
            last_name='Doe'
        )
        try:
            Appointment.objects.create(
                doctor=another_doctor,
                patient=self.patient,
                appointment_time=self.appointment_time,
                reason='Another appointment'
            )
        except IntegrityError:
            self.fail("Should allow appointments at the same time for different doctors")
