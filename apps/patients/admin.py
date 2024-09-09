from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Patient model.
    """
    list_display = ('id', 'first_name', 'last_name', 'email', 'created_by')  # Removed 'created_at'
    list_filter = ('created_by',)  # Removed 'created_at'
    search_fields = ('first_name', 'last_name', 'email', 'created_by__email')
    ordering = ('id',)
    readonly_fields = ('email', 'created_by')
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'password')
        }),
        ('Creator Information', {
            'fields': ('created_by',)
        }),
    )

    def has_add_permission(self, request):
        """
        Prevent adding new patients directly from the admin panel.
        """
        return False
