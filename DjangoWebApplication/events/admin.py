from django.contrib import admin

# Register your models here.

from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'date', 'location', 'status']
    list_filter = ['status', 'date']
    search_fields = ['title', 'organizer__account__full_name', 'location']

admin.site.register(Event, EventAdmin)


