from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.permissions import IsAuthenticated
from apps.doctors.permissions import IsDoctor
from apps.patients.permissions import IsPatient, IsOwner
from apps.doctors.models import Doctor
from apps.patients.models import Patient

User = get_user_model()

class PermissionTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()

        # Create a doctor user
        self.doctor_user = Doctor.objects.create_user(
            email='doctor@example.com',
            password='testpassword123',
            first_name='DoctorFirstName',
            last_name='DoctorLastName'
        )

        # Create a patient user and link it to the doctor
        self.patient_user = Patient.objects.create(
            first_name='PatientFirstName',
            last_name='PatientLastName',
            email='patient@example.com',
            password='testpassword123',
            created_by=self.doctor_user
        )

    def test_is_doctor_permission_with_authenticated_doctor(self):
        request = self.factory.get('/some-url/')
        request.user = self.doctor_user

        permission = IsDoctor()
        self.assertTrue(permission.has_permission(request, None))

    def test_is_doctor_permission_with_authenticated_patient(self):
        request = self.factory.get('/some-url/')
        request.user = self.patient_user

        permission = IsDoctor()
        self.assertFalse(permission.has_permission(request, None))

    def test_is_doctor_permission_with_unauthenticated_user(self):
        request = self.factory.get('/some-url/')
        request.user = None

        permission = IsDoctor()
        self.assertFalse(permission.has_permission(request, None))


    def test_is_owner_permission_with_authenticated_owner(self):
        """
        Test if an authenticated patient who is the owner can access their own resources.
        """
        request = self.factory.get('/some-url/')
        request.user = self.patient_user

        # Simulate the object being accessed by the owner
        permission = IsOwner()
        self.assertTrue(permission.has_object_permission(request, None, self.patient_user))

    #def test_is_owner_permission_with_authenticated_owner(self):
     #   request = self.factory.get('/some-url/')
      #  request.user = self.patient_user

        # Simulate the object being accessed by the owner
       # permission = IsOwner()
        #self.assertTrue(permission.has_object_permission(request, None, self.patient_user))

    def test_is_owner_permission_with_authenticated_non_owner(self):
        request = self.factory.get('/some-url/')
        request.user = self.patient_user

        # Simulate the object being accessed by a non-owner
        another_patient = Patient.objects.create(
            email='another_patient@example.com',
            password='anotherpatientpassword',
            first_name='Another',
            last_name='Patient',
            created_by=self.doctor_user  # Provide the 'created_by' field value
        )

        permission = IsOwner()
        self.assertFalse(permission.has_object_permission(request, None, another_patient))



    def test_is_owner_permission_with_unauthenticated_user(self):
        request = self.factory.get('/some-url/')
        request.user = None
        # Simulate the object being accessed
        permission = IsOwner()
        self.assertFalse(permission.has_object_permission(request, None, self.patient_user))
