import os
import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.gis.geos import Point
from mapa.models import Institution
import googlemaps

class Command(BaseCommand):
    help = 'Import instytucji z przygotowanego CSV przy użyciu Google Maps API (z logowaniem błędów i postępem)'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Ścieżka do pliku CSV')

    def handle(self, *args, **options):
        csv_path = options['csv_path']

        if not os.path.exists(csv_path):
            self.stderr.write(f"❌ Plik nie istnieje: {csv_path}")
            return

        try:
            gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        except Exception as e:
            self.stderr.write(f"❌ Błąd inicjalizacji Google Maps API: {e}")
            return

        errors = []
        added = 0
        skipped = 0

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row_num, row in enumerate(reader, start=1):
                name = row.get("name", "").strip()
                address = row.get("address", "").strip()

                if not name or not address:
                    errors.append(f"[{row_num}] Brak nazwy lub adresu")
                    continue

                print(f"[{row_num}] 🔍 Geokoduję: {address}")

                # Pomijanie duplikatów
                if Institution.objects.filter(name=name, address=address).exists():
                    skipped += 1
                    print(f"[{row_num}] ⚠️ Pominięto duplikat: {name}")
                    continue

                # Geokodowanie
                try:
                    geo = gmaps.geocode(address + ", Polska")
                    if not geo:
                        raise Exception("Brak wyników geokodowania")
                    loc = geo[0]['geometry']['location']
                    point = Point(loc['lng'], loc['lat'])
                except Exception as e:
                    print(f"[{row_num}] ❌ Błąd geokodowania: {e}")
                    errors.append(f"[{row_num}] {name} — geokodowanie nieudane: {e}")
                    continue

                try:
                    Institution.objects.create(
                        name=name[:255],
                        type=row.get("type", "NGO").strip(),
                        address=address[:500],
                        email=row.get("email", "")[:255] or None,
                        phone_number=row.get("phone_number", "")[:255],
                        opening_hours=row.get("opening_hours", "")[:255] or None,
                        psychological_help=row.get("psychological_help", "").strip().lower() == 'true',
                        legal_help=row.get("legal_help", "").strip().lower() == 'true',
                        social_help=row.get("social_help", "").strip().lower() == 'true',
                        accommodation=row.get("accommodation", "").strip().lower() == 'true',
                        infoline=row.get("infoline", "")[:255] or None,
                        description=row.get("description", "") or None,
                        location=point
                    )
                    added += 1
                    print(f"[{row_num}] ✅ Dodano: {name}")
                except Exception as e:
                    print(f"[{row_num}] ❌ Błąd zapisu: {e}")
                    errors.append(f"[{row_num}] {name} — błąd zapisu: {e}")

        print(f"\n✅ Zaimportowano: {added}")
        print(f"⚠️ Pominięto duplikatów: {skipped}")
        print(f"❌ Błędów: {len(errors)}")

        if errors:
            log_file = 'import_errors.log'
            with open(log_file, 'w', encoding='utf-8') as f:
                for err in errors:
                    f.write(err + '\n')
            print(f"📄 Zapisano log błędów do: {log_file}")
