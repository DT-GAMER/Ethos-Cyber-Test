from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.doctors.models import Appointment, Doctor
from apps.patients.serializers import (
    PatientLoginSerializer,
    PatientProfileSerializer,
    PatientSerializer,
    PatientAppointmentSerializer,
)
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.utils import timezone

Patient = get_user_model()

class PatientLoginSerializerTest(TestCase):
    def setUp(self):
        self.patient_data = {
            "email": "testpatient@example.com",
            "first_name": "Test",
            "last_name": "Patient",
            "password": "password123",
        }
        self.patient = Patient.objects.create_user(**self.patient_data)

    def test_valid_data(self):
        serializer = PatientLoginSerializer(data={
            "email": "testpatient@example.com",
            "password": "password123",
        })
        self.assertTrue(serializer.is_valid())


    def test_missing_password(self):
        serializer = PatientLoginSerializer(data={
            "email": "testpatient@example.com",
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)


class PatientProfileSerializerTest(TestCase):
    def setUp(self):
        self.patient_data = {
            "email": "testpatient@example.com",
            "first_name": "Test",
            "last_name": "Patient",
            "password": "password123",
            "phone_number": "1234567890",
        }
        self.patient = Patient.objects.create_user(**self.patient_data)

    def test_patient_profile_retrieve(self):
        serializer = PatientProfileSerializer(instance=self.patient)
        self.assertEqual(serializer.data['first_name'], self.patient.first_name)
        self.assertEqual(serializer.data['last_name'], self.patient.last_name)
        self.assertEqual(serializer.data['email'], self.patient.email)
        self.assertEqual(serializer.data['phone_number'], self.patient.phone_number)

    def test_patient_profile_update(self):
        serializer = PatientProfileSerializer(
            instance=self.patient,
            data={'first_name': 'Updated', 'last_name': 'Name', 'phone_number': '0987654321'},
            partial=True
        )
        self.assertTrue(serializer.is_valid())
        updated_patient = serializer.save()
        self.assertEqual(updated_patient.first_name, 'Updated')
        self.assertEqual(updated_patient.last_name, 'Name')
        self.assertEqual(updated_patient.phone_number, '0987654321')


class PatientSerializerTest(TestCase):
    def setUp(self):
        self.patient_data = {
            "email": "testpatient@example.com",
            "first_name": "Test",
            "last_name": "Patient",
            "password": "password123",
        }
        self.patient = Patient.objects.create_user(**self.patient_data)

    def test_patient_data_retrieve(self):
        serializer = PatientSerializer(instance=self.patient)
        self.assertEqual(serializer.data['first_name'], self.patient.first_name)
        self.assertEqual(serializer.data['last_name'], self.patient.last_name)
        self.assertEqual(serializer.data['email'], self.patient.email)
