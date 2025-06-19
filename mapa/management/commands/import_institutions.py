import csv
import time
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from mapa.models import Institution
from geopy.geocoders import Nominatim


class Command(BaseCommand):
    help = 'Importuje instytucje z pliku CSV do bazy danych'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Ścieżka do pliku CSV z danymi instytucji')

    def handle(self, *args, **options):
        path = options['csv_file']
        geolocator = Nominatim(user_agent="czaskobiet_map")

        errors = []

        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, start=1):
                address = row['address'].strip()
                address_clean = (
                    address.replace("ul. ", "")
                           .replace("UL. ", "")
                           .replace("Ul. ", "")
                           .replace("al. ", "")
                           .replace("Al. ", "")
                           .replace("pl. ", "")
                           .replace("Pl. ", "")
                )

                try:
                    location = geolocator.geocode(address_clean + ", Polska")
                    time.sleep(1)
                except Exception as e:
                    msg = f"[{idx}] Błąd geolokalizacji: {address_clean} ({e})"
                    self.stderr.write(msg)
                    errors.append({'index': idx, 'name': row['name'], 'address': address, 'reason': str(e)})
                    continue

                if not location:
                    msg = f"[{idx}] Nie znaleziono geolokalizacji: {address_clean}"
                    self.stderr.write(msg)
                    errors.append({'index': idx, 'name': row['name'], 'address': address, 'reason': 'Geocoding failed'})
                    continue

                point = Point(location.longitude, location.latitude)

                def parse_bool(val):
                    return str(val).strip().lower() in ['tak', 'true', '1', 't']

                type_map = {
                    'Pozarządowa': 'NGO',
                    'Publiczna': 'GOV'
                }

                institution_type = type_map.get(row['type'].strip(), 'NGO')

                email = row.get('email', '').strip()
                email = '' if email.lower() in ['nie', 'brak', ''] else email

                infoline = row.get('infoline', '').strip()
                infoline = '' if infoline.lower() in ['nie', 'brak'] else infoline

                opening_hours = row.get('opening_hours', '').strip()
                opening_hours = '' if opening_hours.lower() in ['nie', 'brak'] else opening_hours

                # Unikaj duplikatów po nazwie + adresie
                if Institution.objects.filter(name=row['name'].strip(), address=address).exists():
                    self.stdout.write(f"[{idx}] Pominięto (duplikat): {row['name']}")
                    continue

                institution = Institution(
                    name=row['name'].strip(),
                    address=address,
                    phone_number=row['phone_number'].strip(),
                    type=institution_type,
                    psychological_help=parse_bool(row.get('psychological_help', '')),
                    legal_help=parse_bool(row.get('legal_help', '')),
                    social_help=parse_bool(row.get('social_help', '')),
                    accommodation=parse_bool(row.get('accommodation', '')),
                    location=point,
                    description='',
                    email=email,
                    infoline=infoline,
                    opening_hours=opening_hours
                )

                try:
                    institution.save()
                    self.stdout.write(f"[{idx}] Dodano: {institution.name}")
                except Exception as e:
                    msg = f"[{idx}] Błąd przy zapisie: {e}"
                    self.stderr.write(msg)
                    errors.append({'index': idx, 'name': row['name'], 'address': address, 'reason': str(e)})

        # Zapisz błędy do pliku
        if errors:
            with open('import_errors.csv', 'w', newline='', encoding='utf-8') as errfile:
                writer = csv.DictWriter(errfile, fieldnames=['index', 'name', 'address', 'reason'])
                writer.writeheader()
                writer.writerows(errors)
            self.stdout.write(f"\nZakończono z {len(errors)} błędami — zapisano w import_errors.csv")
        else:
            self.stdout.write("\nImport zakończony bez błędów.")
