from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password


class DoctorManager(BaseUserManager):
    """
    Manager for creating Doctor instances.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        doctor = Doctor(email=email, **extra_fields)
        doctor.set_password(password)
        doctor.save(using=self._db)
        return doctor

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class Doctor(AbstractUser):
    """
    Custom user model for doctors.
    """
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')],
        blank=True,
        null=True
    )
    password = models.CharField(max_length=128)
    address = models.CharField(max_length=255, blank=True, null=True)
    availability_days = models.CharField(max_length=100, blank=True, null=True)
    availability_time_range = models.CharField(max_length=50, blank=True, null=True)
    # Maintain default user_permissions relationship for handling user permissions
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="doctor_user_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = DoctorManager()  # Use the custom manager

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'


class Patient(models.Model):
    """
    Model representing a patient.
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patients')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    @property
    def is_authenticated(self):
        return True


class Appointment(models.Model):
    """
    Model representing an appointment.
    """
    APPOINTMENT_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS_CHOICES, default='scheduled')
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with {self.patient.first_name} {self.patient.last_name} on {self.date} at {self.time}"
