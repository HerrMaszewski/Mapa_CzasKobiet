from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from geopy.geocoders import Nominatim

class Institution(models.Model):
    TYPE_CHOICES = [
        ('NGO', 'Organizacja pozarządowa'),
        ('GOV', 'Instytucja publiczna'),
    ]

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=100)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    psychological_help = models.BooleanField(default=False)
    social_help = models.BooleanField(default=False)
    legal_help = models.BooleanField(default=False)
    accommodation = models.BooleanField(default=False)
    location = models.PointField()  # latitude and longitude
    description = models.TextField(blank=True, null=True)
    opening_hours = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, default=False, blank=True, null=True)
    infoline = models.CharField(max_length=255, default=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.location and self.address:
            geolocator = Nominatim(user_agent="czaskobiet_map")
            try:
                location = geolocator.geocode(self.address)
                if location:
                    self.location = Point(location.longitude, location.latitude)
            except Exception as e:
                print(f"Geocoding failed: {e}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
