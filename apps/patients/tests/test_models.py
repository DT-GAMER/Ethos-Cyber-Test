from django.test import TestCase
from django.contrib.auth.models import Permission
from apps.doctors.models import Doctor
from apps.patients.models import Patient, PatientManager

class PatientTestCase(TestCase):
    def test_str_method(self):
        # Test the __str__ method of the Patient model
        doctor = Doctor.objects.create(
            email='doctor@example.com',
            first_name='Jane',
            last_name='Doe'
        )
        patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            email='patient@example.com',
            created_by=doctor,
            password='password123'
        )
        self.assertEqual(str(patient), 'John Doe (patient@example.com)')

    def test_get_full_name(self):
        # Test the get_full_name method
        patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            email='patient@example.com',
            password='password123'
        )
        self.assertEqual(patient.get_full_name(), 'John Doe')

    def test_get_short_name(self):
        # Test the get_short_name method
        patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            email='patient@example.com',
            password='password123'
        )
        self.assertEqual(patient.get_short_name(), 'John')

    def test_create_user_with_phone_number(self):
        # Test creating a patient with a phone number
        doctor = Doctor.objects.create(
            email='doctor@example.com',
            first_name='Jane',
            last_name='Doe'
        )
        patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            email='patient@example.com',
            phone_number='123-456-7890',
            created_by=doctor,
            password='password123'
        )
        self.assertEqual(patient.phone_number, '123-456-7890')
