from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/doctors/', include('apps.doctors.urls')),
    path('api/patients/', include('apps.patients.urls')),
]
