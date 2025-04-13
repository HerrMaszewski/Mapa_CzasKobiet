from django.contrib.gis.db import models

class Institution(models.Model):
    TYPE_CHOICES = [
        ('NGO', 'Organizacja pozarządowa'),
        ('GOV', 'Instytucja publiczna'),
    ]

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    psychological_help = models.BooleanField(default=False)
    social_help = models.BooleanField(default=False)
    legal_help = models.BooleanField(default=False)
    accommodation = models.BooleanField(default=False)
    location = models.PointField()  # latitude and longitude
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
