from rest_framework import permissions

class IsDoctor(permissions.BasePermission):
    """
    Custom permission to only allow authenticated doctors to access certain views.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated and is a Doctor.

        Args:
            request: The HTTP request instance.
            view: The view instance.

        Returns:
            bool: True if the user is authenticated and is a Doctor, False otherwise.
        """
        return request.user and request.user.is_authenticated and hasattr(request.user, 'doctor')

class CanManagePatient(permissions.BasePermission):
    """
    Custom permission to ensure doctors can only manage their own patients.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to manage patients.

        Args:
            request: The HTTP request instance.
            view: The view instance.

        Returns:
            bool: True if the user is authenticated and is a Doctor, False otherwise.
        """
        # The user must be a doctor to manage patients.
        return request.user and request.user.is_authenticated and hasattr(request.user, 'doctor')

    def has_object_permission(self, request, view, obj):
        """
        Check if the doctor has permission to manage the specific patient object.

        Args:
            request: The HTTP request instance.
            view: The view instance.
            obj: The patient object to check permission for.

        Returns:
            bool: True if the logged-in doctor is the creator of the patient, False otherwise.
        """
        # THis give object-level permission to allow doctors to manage only their own patients.
        return request.user == obj.created_by
