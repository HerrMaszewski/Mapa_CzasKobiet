from django.shortcuts import render
from .models import Institution  
import json

def map_view(request):
    institutions = Institution.objects.all()
    data = []
    for i in institutions:
        data.append({
            'name': i.name,
            'address': i.address,
            'phone_number': i.phone_number,
            'type': i.type,
            'location': {
                'latitude': i.location.y,
                'longitude': i.location.x
            },
            'description': i.description or "",
        })
    
    return render(request, 'mapa/map.html', {
        'institutions_json': json.dumps(data)
    })
