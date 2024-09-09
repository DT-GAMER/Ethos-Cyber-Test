# Ethos-Cyber-Test

1. **Project Overview**
2. **Features**
3. **Tech Stack**
4. **Installation and Setup Instructions**
5. **Database Setup and Migration**
6. **Populating the Database with Sample Data**
7. **Running the Application**
8. **Running Tests**
9. **API Endpoints**
10. **Notes**
    

Ethos Cyber Sett is a Django-based web application designed to manage patients, doctors, and appointments in a healthcare setting. The system allows doctors to create and manage patient accounts, while patients can log in, view and update their profiles, and book appointments with doctors.

## Features

- **Doctor Management**: Doctors can register, log in, manage their profiles, and create patient accounts.
- **Patient Management**: Patients can log in, update their profiles, view and manage appointments.
- **Appointment Booking**: Patients can book and view their appointments with doctors.
- **Secure Authentication**: Utilizes Django's authentication system with tokens for secure API access.
- **Role-Based Access Control**: Custom permissions to control access based on user roles (Doctor or Patient).

## Tech Stack

- **Backend**: Django 4.x, Django REST Framework
- **Database**: SQLite (default), but can be configured to use PostgreSQL, MySQL, or any other Django-supported database.
- **Authentication**: Token-based authentication using `rest_framework.authtoken`
- **Frontend**: None (API-based system)

## Installation and Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/DT-GAMER/ethos-cyber-sett.git
   cd ethos-cyber-sett
   ```

2. **Create a Virtual Environment:**

   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install Required Packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Database Setup and Migration

1. **Make Migrations:**

   ```bash
   python manage.py makemigrations
   ```

2. **Apply Migrations:**

   ```bash
   python manage.py migrate
   ```

3. **Create a Superuser:**

   To create a superuser account for accessing the Django admin panel, run:

   ```bash
   python manage.py createsuperuser
   ```

   Follow the prompts to set up your superuser account.

## Populating the Database with Sample Data

You can populate the database with some initial data using fixtures or by manually creating entries via the Django admin panel.

1. **Using Django Admin:**

   - Start the server:

     ```bash
     python manage.py runserver
     ```

   - Visit `http://127.0.0.1:8000/admin` in the browser.
   - Log in using the superuser credentials you created earlier.
   - Add doctors, patients, and appointments via the admin interface.

2. **Using Fixtures:**

   You can create a JSON fixture file to load sample data:

   ```bash
   python manage.py loaddata sample_data.json
   ```

   Ensure that `sample_data.json` is formatted correctly with sample doctors, patients, and appointments.

## Running the Application

To run the application, use the Django development server:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

## Running Tests

Tests are located in the `tests` directory of each app. To run all tests:

```bash
python manage.py test apps.doctors.tests
python manage.py test apps.patients.tests
```

This will run all unit tests and provide a coverage report.

```bash
coverage report
```

## API Endpoints

Here is a list of the main API endpoints provided in the Ethos Cyber Sett project:

### **Auth and Profile Management**

- **Login (Patient):** `POST /api/patients/login/`
- **Patient Profile:** `GET /api/patients/profile/` and `PUT /api/patients/profile/`

### **Appointments**

- **List Appointments (Patient):** `GET /api/patients/appointments/`
- **Create Appointment (Patient):** `POST /api/patients/appointments/`
- **Appointment Details (Patient):** `GET /api/patients/appointments/<id>/`

### **Doctor Management**

- **Register Doctor:** `POST /api/doctors/register/`
- **Doctor Login:** `POST /api/doctors/login/`
- **Manage Patient Accounts (Doctors only):** `POST /api/doctors/patients/`

### **Patient Management (Doctors only)**

- **Create Patient Account:** `POST /api/doctors/patients/create/`
- **List Patients:** `GET /api/doctors/patients/`

## Notes

- Ensure the virtual environment is activated whenever running any Django management commands.
- The project uses token-based authentication; ensure you include the token in the `Authorization` header when making API requests.

