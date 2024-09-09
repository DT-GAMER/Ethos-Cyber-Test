from django.test import TestCase
from apps.patients.models import Patient
from django.core.exceptions import ValidationError


class PatientModelTests(TestCase):

    def setUp(self):
        """Create a unique patient instance for testing."""
        self.first_name = "testuser"
        self.last_name = "seconduser"
        self.email = "test@example.com"
        self.password = "securepassword"
        self.patient = Patient.objects.create_user(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password
        )

    def test_patient_creation(self):
        """Test that a patient can be created successfully with all required fields."""
        self.assertIsInstance(self.patient, Patient)
        self.assertEqual(self.patient.first_name, self.first_name)
        self.assertEqual(self.patient.last_name, self.last_name)
        self.assertEqual(self.patient.email, self.email)

    def test_invalid_email(self):
        """Test that an invalid email raises an error."""
        with self.assertRaises(ValidationError):
            Patient.objects.create_user(
                first_name="invalidemailuser",
                last_name="invalidemailuser",
                email="invalid-email",
                password="securepassword"
            )

    def test_no_address(self):
        """Test that a patient can be created without an address."""
        patient = Patient.objects.create_user(
            first_name="anotheruser",
            last_name="anotruser",
            email="another@example.com",
            password="securepassword"
        )
        self.assertIsNone(patient.address)

    def test_no_phone_number(self):
        """Test that a patient can be created without a phone number."""
        patient = Patient.objects.create_user(
            first_name="yetanotheruser",
            last_name="yetotheruser",
            email="yetanother@example.com",
            password="securepassword"
        )
        self.assertIsNone(patient.phone_number)

    def test_update_patient(self):
        """Test that patient details can be updated successfully."""
        self.patient.address = "123 Main St"
        self.patient.phone_number = "123-456-7890"
        self.patient.save()
        updated_patient = Patient.objects.get(first_name=self.first_name)
        update_patient = Patient.objects.get(last_name=self.last_name)
        self.assertEqual(updated_patient.address, "123 Main St")
        self.assertEqual(updated_patient.phone_number, "123-456-7890")
