import csv
from django.core.management.base import BaseCommand
from mapa.models import Institution

class Command(BaseCommand):
    help = "Aktualizuje numery telefonów instytucji na podstawie pliku CSV"

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Ścieżka do pliku CSV z telefonami')

    def handle(self, *args, **options):
        path = options['csv_path']
        updated = 0
        not_found = []

        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['name'].strip()
                address = row['address'].strip()
                phone_number = row['phone_number'].strip()

                try:
                    inst = Institution.objects.get(name=name, address=address)
                    inst.phone_number = phone_number
                    inst.save()
                    updated += 1
                    self.stdout.write(f"✅ Zaktualizowano: {name}")
                except Institution.DoesNotExist:
                    not_found.append(f"{name} — {address}")

        self.stdout.write(f"\n🔁 Zaktualizowano {updated} rekordów.")
        if not_found:
            self.stdout.write(f"⚠️ Nie znaleziono {len(not_found)} instytucji. Lista:")
            for nf in not_found:
                self.stdout.write(f" - {nf}")
