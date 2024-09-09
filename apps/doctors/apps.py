from django.apps import AppConfig

class DoctorsConfig(AppConfig):
    """
    Configuration class for the 'doctors' app.
    This class is for defining the application settings and signals.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.doctors'

    def ready(self):
        """
        Overriding the ready method to import signals.
        This method is called when the application is ready to be used.
        """
