from apps.doctors.tests.test_serializers import PatientCreationSerializerTest
from django.test import TestCase
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from apps.doctors.models import DoctorManager, Doctor, Patient, Appointment

class DoctorManagerTestCase(TestCase):
    def test_create_user(self):
        # Test creating a regular user
        doctor = DoctorManager().create_user(email='test@example.com', password='password123')
        self.assertEqual(doctor.email, 'test@example.com')
        self.assertTrue(doctor.check_password('password123'))
        self.assertTrue(doctor.is_active)
        self.assertFalse(doctor.is_staff)
        self.assertFalse(doctor.is_superuser)

    def test_create_superuser(self):
        # Test creating a superuser
        doctor = DoctorManager().create_superuser(email='admin@example.com', password='password123')
        self.assertEqual(doctor.email, 'admin@example.com')
        self.assertTrue(doctor.check_password('password123'))
        self.assertTrue(doctor.is_active)
        self.assertTrue(doctor.is_staff)
        self.assertTrue(doctor.is_superuser)

    def test_create_user_without_email(self):
        # Test creating a user without an email
        with self.assertRaises(ValueError):
            DoctorManager().create_user(email=None, password='password123')

    def test_create_superuser_without_is_staff(self):
        # Test creating a superuser without is_staff=True
        with self.assertRaises(ValueError):
            DoctorManager().create_superuser(email='admin@example.com', password='password123', is_staff=False)

    def test_create_superuser_without_is_superuser(self):
        # Test creating a superuser without is_superuser=True
        with self.assertRaises(ValueError):
            DoctorManager().create_superuser(email='admin@example.com', password='password123', is_superuser=False)

class DoctorTestCase(TestCase):
    def test_str_method(self):
        # Test the __str__ method of the Doctor model
        doctor = Doctor.objects.create(
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(str(doctor), 'John Doe (test@example.com)')

    def test_user_permissions(self):
        # Test the user_permissions relationship
        doctor = Doctor.objects.create(
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )

        # Get or create a ContentType instance to avoid duplicate entries
        content_type, created = ContentType.objects.get_or_create(
            app_label='doctors',
            model='doctor'
        )

        # Create a Permission instance with the correct content_type_id
        permission = Permission.objects.create(
            name='Can view patient',
            content_type=content_type
        )

        doctor.user_permissions.add(permission)
        self.assertIn(permission, doctor.user_permissions.all())

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
            password='password123',
            created_by=doctor
        )
        self.assertEqual(str(patient), 'John Doe (patient@example.com)')

class AppointmentTestCase(TestCase):
    def test_str_method(self):
        # Test the __str__ method of the Appointment model
        doctor = Doctor.objects.create(
            email='doctor@example.com',
            first_name='Jane',
            last_name='Doe'
        )
        patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            email='patient@example.com',
            password='password123',
            created_by=doctor
        )
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date='2023-05-01',
            time='10:00:00'
        )
        self.assertEqual(str(appointment), 'Appointment with John Doe on 2023-05-01 at 10:00:00')
