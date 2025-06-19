import csv
import time
import os
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from mapa.models import Institution
from opencage.geocoder import OpenCageGeocode
from dotenv import load_dotenv
load_dotenv()


class Command(BaseCommand):
    help = 'Importuje instytucje z CSV do bazy danych z użyciem OpenCage API'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Ścieżka do pliku CSV')

    def handle(self, *args, **options):
        path = options['csv_file']
        api_key = os.environ.get("OPENCAGE_API_KEY")

        if not api_key:
            self.stderr.write("❌ Brak klucza OPENCAGE_API_KEY w zmiennych środowiskowych.")
            return

        geocoder = OpenCageGeocode(api_key)
        errors = []

        def parse_bool(val):
            return str(val).strip().lower() in ['tak', 'true', '1', 't']

        type_map = {'Pozarządowa': 'NGO', 'Publiczna': 'GOV'}

        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, start=1):
                name = row['name'].strip()
                address = row['address'].strip()

                query = f"{address}, Polska"
                location = None

                try:
                    results = geocoder.geocode(query, language='pl', limit=5)
                    time.sleep(0.4)
                except Exception as e:
                    self.stderr.write(f"[{idx}] Błąd API: {e}")
                    errors.append({'index': idx, 'name': name, 'address': address, 'reason': str(e)})
                    continue

                if results:
                    for res in results:
                        components = res.get('components', {})
                        if 'city' in components and components['city'].lower() in address.lower():
                            location = res
                            break
                    if not location:
                        location = results[0]
                else:
                    self.stderr.write(f"[{idx}] ❗ Nie znaleziono lokalizacji: {address}")
                    errors.append({'index': idx, 'name': name, 'address': address, 'reason': 'Brak wyników'})
                    continue

                point = Point(location['geometry']['lng'], location['geometry']['lat'])

                institution_type = type_map.get(row['type'].strip(), 'NGO')
                phone = row.get('phone_number', '').strip()
                email = row.get('email', '').strip()
                infoline = row.get('infoline', '').strip()
                opening_hours = row.get('opening_hours', '').strip()

                if email.lower() in ['brak', 'nie', '']: email = ''
                if infoline.lower() in ['brak', 'nie', '']: infoline = ''
                if opening_hours.lower() in ['brak', 'nie', '']: opening_hours = ''

                if Institution.objects.filter(name=name, address=address).exists():
                    self.stdout.write(f"[{idx}] Pominięto (duplikat): {name}")
                    continue

                inst = Institution(
                    name=name,
                    address=address,
                    phone_number=phone,
                    type=institution_type,
                    psychological_help=parse_bool(row.get('psychological_help', '')),
                    legal_help=parse_bool(row.get('legal_help', '')),
                    social_help=parse_bool(row.get('social_help', '')),
                    accommodation=parse_bool(row.get('accommodation', '')),
                    location=point,
                    email=email,
                    infoline=infoline,
                    opening_hours=opening_hours,
                    description=''
                )

                try:
                    inst.save()
                    self.stdout.write(f"[{idx}] ✅ Dodano: {name}")
                except Exception as e:
                    self.stderr.write(f"[{idx}] ❌ Błąd zapisu: {e}")
                    errors.append({'index': idx, 'name': name, 'address': address, 'reason': str(e)})

        if errors:
            with open('import_errors.csv', 'w', newline='', encoding='utf-8') as errfile:
                writer = csv.DictWriter(errfile, fieldnames=['index', 'name', 'address', 'reason'])
                writer.writeheader()
                writer.writerows(errors)
            self.stdout.write(f"\n⚠️ Zakończono z {len(errors)} błędami – zapisano do import_errors.csv")
        else:
            self.stdout.write("\n🎉 Import zakończony bez błędów.")