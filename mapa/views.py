import json
import requests
from django.shortcuts import render
from .models import Institution
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt

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
            'psychological_help': i.psychological_help,
            'legal_help': i.legal_help,
            'social_help': i.social_help,
            'accommodation': i.accommodation,
            'opening_hours': i.opening_hours or "",
            'email': i.email or '',
            'infoline': i.infoline or '',
        })
    
    return render(request, 'mapa/map.html', {
        'institutions_json': json.dumps(data)
    })

@csrf_exempt  # jeśli robisz GET, zwykle nie trzeba, ale na wszelki wypadek
@require_GET
def geocode_proxy(request):
    q = request.GET.get("q")
    if not q:
        return JsonResponse({"error": "Missing query parameter 'q'"}, status=400)

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": q,
        "format": "json",
        "addressdetails": 1,
        "limit": 5,
    }

    try:
        response = requests.get(url, params=params, headers={"User-Agent": "CzasKobietApp"})
        response.raise_for_status()
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=502)

    return JsonResponse(response.json(), safe=False)
