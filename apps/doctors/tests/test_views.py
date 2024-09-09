from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from apps.doctors.models import Doctor, Patient

User = get_user_model()

class DoctorViewsTestCase(APITestCase):

    def setUp(self):
        # Create a doctor for testing
        self.doctor = Doctor.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='testpassword'
        )
        self.patient = Patient.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='jane.doe@example.com',
            created_by=self.doctor
        )
        self.login_url = '/api/doctors/login/'
        self.register_url = '/api/doctors/register/'
        self.profile_url = '/api/doctors/profile/'
        self.create_patient_url = '/api/doctors/patients/'
        self.patient_detail_url = f'/api/doctors/patients/{self.patient.id}/'
        self.patient_list_url = '/api/doctors/patients/'
        self.tokens = None

    def test_doctor_registration(self):
        data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice.smith@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Doctor.objects.filter(email='alice.smith@example.com').exists())

    def test_doctor_login(self):
        data = {
            'email': 'john.doe@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        print(f"Login response data: {response.data}")  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tokens = response.data  # Ensure tokens are saved
        self.assertIn('access', self.tokens)  # Ensure 'access' token is present
        # Set the Authorization header for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.tokens['access'])

    def test_doctor_profile_retrieval(self):
        self.test_doctor_login()  # Ensure we are logged in
        response = self.client.get(self.profile_url)
        print(f"Profile retrieval response status: {response.status_code}, data: {response.data}")  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.doctor.email)

    def test_doctor_profile_update(self):
        self.test_doctor_login()  # Ensure we are logged in
        data = {
            'phone_number': '123-456-7890',
            'address': '123 Main St',
            'medical_specialization': 'Cardiology',
            'availability_days': 'Monday-Friday',
            'availability_time_range': '09:00-17:00'
        }
        response = self.client.patch(self.profile_url, data, format='json')
        print(f"Profile update response status: {response.status_code}, data: {response.data}")  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], '123-456-7890')

    def test_create_patient(self):
        self.test_doctor_login()  # Ensure we are logged in
        data = {
            'first_name': 'Michael',
            'last_name': 'Jordan',
            'email': 'michael.jordan@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.create_patient_url, data, format='json')
        print(f"Create patient response status: {response.status_code}, data: {response.data}")  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Patient.objects.filter(email='michael.jordan@example.com').exists())

    def test_retrieve_patient_details(self):
        self.test_doctor_login()  # Ensure we are logged in
        response = self.client.get(self.patient_detail_url)
        print(f"Retrieve patient response status: {response.status_code}, data: {response.data}")  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.patient.email)

    def test_list_patients(self):
        self.test_doctor_login()  # Ensure we are logged in
        response = self.client.get(self.patient_list_url)
        print(f"List patients response status: {response.status_code}, data: {response.data}")  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Ensure the list is not empty
