from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Institution

@admin.register(Institution)
class InstitutionAdmin(LeafletGeoAdmin):
    list_display = ('name', 'location')