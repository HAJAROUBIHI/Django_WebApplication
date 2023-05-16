from django.db import models
from django.contrib.auth.models import User



class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='event_images', blank=True, null=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

# Create your models here.
