from rest_framework import permissions
from apps.doctors.models import Appointment
from apps.patients.models import Patient

class IsPatient(permissions.BasePermission):
    """
    Custom permission to only allow authenticated patients to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a Patient
        return request.user and request.user.is_authenticated and hasattr(request.user, 'patient')

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow patients to edit their own information.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the object
        # For patient profile and appointments, the user should be the owner
        if isinstance(obj, Patient):
            return obj == request.user
        elif isinstance(obj, Appointment):
            return obj.patient == request.user
        return False
