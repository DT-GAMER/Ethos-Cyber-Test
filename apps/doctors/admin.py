from django.contrib import admin
from apps.doctors.models import Doctor, Patient, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Doctor model.
    """
    list_display = ('id', 'first_name', 'last_name', 'email', 'medical_specialization', 'is_active')
    list_filter = ('medical_specialization', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'medical_specialization')
    ordering = ('id',)
    readonly_fields = ('email', 'password')
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'password', 'is_active')
        }),
        ('Professional Info', {
            'fields': ('medical_specialization', 'phone_number', 'address', 'availability_days', 'availability_time_range')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Make email and password fields read-only in the admin panel.
        """
        if obj:
            return self.readonly_fields + ('email',)
        return self.readonly_fields

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Patient model.
    """
    list_display = ('id', 'first_name', 'last_name', 'email', 'created_by')
    list_filter = ('created_by',)
    search_fields = ('first_name', 'last_name', 'email', 'created_by__email')
    ordering = ('id',)
    readonly_fields = ('created_by',)

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Creator Information', {
            'fields': ('created_by',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Make the created_by field read-only for existing patients.
        """
        if obj:
            return self.readonly_fields + ('email',)
        return self.readonly_fields

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Appointment model.
    """
    list_display = ('id', 'doctor', 'patient', 'date', 'time', 'status', 'reason')
    list_filter = ('doctor', 'date', 'status')
    search_fields = ('doctor__email', 'patient__email', 'reason')
    ordering = ('date', 'time')
    fieldsets = (
        (None, {
            'fields': ('doctor', 'patient', 'date', 'time', 'status', 'reason')
        }),
    )

    def has_add_permission(self, request):
        """
        Prevent adding new appointments directly from the admin panel.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Allow only status updates for appointments in the admin panel.
        """
        if obj:
            return request.user.is_superuser or 'status' in [f.name for f in obj._meta.fields]
        return True
