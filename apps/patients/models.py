from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.conf import settings

class PatientManager(BaseUserManager):
    """
    Custom manager for the Patient model.
    """
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        patient = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        patient.set_password(password)
        patient.save(using=self._db)
        return patient

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, first_name, last_name, password, **extra_fields)

class Patient(AbstractBaseUser, PermissionsMixin):
    """
    Custom Patient model for managing patient data and authentication.
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        'doctors.Doctor',  # Reference to the Doctor model
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_patients'

    groups = models.ManyToManyField(
        Group,
        related_name="patient_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="patient_user_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    objects = PatientManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    def get_full_name(self):
        """
        Returns the first name and last name of the patient.
        """
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        """
        Returns the first name of the patient.
        """
        return self.first_name
