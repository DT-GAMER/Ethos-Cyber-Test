# apps/patients/tests/test_serializers.py

from django.test import TestCase
from rest_framework.exceptions import ValidationError
from apps.patients.models import Patient
from apps.patients.serializers import PatientSerializer, PatientCreationSerializer

class PatientSerializerTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone_number': '1234567890',
            'address': '123 Street Name',
            'password': 'password123'
        }
        self.patient = Patient.objects.create_user(**self.valid_data)

    def test_patient_serializer_valid(self):
        serializer = PatientSerializer(instance=self.patient)
        data = serializer.data
        self.assertEqual(data['first_name'], self.valid_data['first_name'])
        self.assertEqual(data['last_name'], self.valid_data['last_name'])
        self.assertEqual(data['email'], self.valid_data['email'])
        self.assertEqual(data['phone_number'], self.valid_data['phone_number'])
        self.assertEqual(data['address'], self.valid_data['address'])

    def test_patient_creation_serializer_valid(self):
        creation_data = self.valid_data.copy()
        creation_data['email'] = 'new.email@example.com'
        serializer = PatientCreationSerializer(data=creation_data)
        self.assertTrue(serializer.is_valid())
        patient = serializer.save()
        self.assertEqual(patient.first_name, creation_data['first_name'])
        self.assertEqual(patient.last_name, creation_data['last_name'])
        self.assertEqual(patient.email, creation_data['email'])
        self.assertTrue(patient.check_password(creation_data['password']))

    def test_invalid_email(self):
        serializer = PatientCreationSerializer(data={
            **self.valid_data,
            'email': 'invalid-email'
        })
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_email_already_exists(self):
        creation_data = self.valid_data.copy()
        serializer = PatientCreationSerializer(data=creation_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
