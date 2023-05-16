import profile
from django.contrib import admin

# Register your models here.

from .models import Account  # Replace Event with your actual model name

admin.site.register(Account)  # Repeat this line for each model in the application
