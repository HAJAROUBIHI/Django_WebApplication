from django.contrib import admin

# Register your models here.
from .models import Event  # Replace Event with your actual model name

admin.site.register(Event)  # Repeat this line for each model in the application

