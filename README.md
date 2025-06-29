# 🗺️ Mapa Wsparcia dla Kobiet

Projekt **Mapy Wsparcia dla Kobiet** to interaktywne narzędzie internetowe, które umożliwia szybkie i intuicyjne odnalezienie instytucji oferujących wsparcie kobietom doświadczającym przemocy – psychologiczne, prawne, socjalne oraz noclegowe.

📍 Mapa obejmuje całą Polskę i umożliwia filtrowanie wyników według rodzaju pomocy, typu instytucji (GOV/NGO) oraz lokalizacji.

---

## 🎯 Cel projektu

Projekt został zrealizowany na zlecenie Fundacji **Czas Kobiet**  
💬 finansowany dzięki **Ambasadzie Francji** oraz **Ambasadzie Szwajcarii**.

Wykonanie: [Tadeusz Maszewski](mailto:tadeusz.maszewski@gmail.com)

---

## ⚙️ Technologie i narzędzia

Projekt został wykonany w oparciu o następujący stos technologiczny:

### 🧩 Backend
- **Django** (v4.2+) – szybki framework do aplikacji webowych
- **PostgreSQL** z rozszerzeniem **PostGIS** – obsługa danych przestrzennych
- **Geopy + OpenCage API** – do geolokalizacji instytucji na etapie importu
- **Customowe komendy Django** (`manage.py import_institutions`) – do importu danych z CSV

### 🗺️ Frontend
- **Leaflet.js** – interaktywna mapa oparta o OpenStreetMap
- **Leaflet.markercluster** – grupowanie znaczników
- **Leaflet Geocoder** – obsługa wyszukiwania lokalizacji po adresie
- **Customowy CSS** (w tym tryb mobilny) – stylowanie filtrowania i wyników

---

## 📦 Struktura projektu

DjangoProject/
├── mapa/
│ ├── templates/
│ ├── static/
│ ├── management/commands/
│ ├── models.py
│ └── ...
├── requirements.txt
├── manage.py
└── .env.example

yaml
Kopiuj
Edytuj

---

## 🧪 Działanie aplikacji

- Użytkownik podaje swoją lokalizację (adres)
- Wybiera typ instytucji (GOV / NGO)
- Wybiera rodzaj pomocy (np. psychologiczna)
- System wyświetla instytucje w promieniu X km, z listą oraz znacznikami na mapie

Każdy wynik zawiera:
- Dane kontaktowe
- Ikony usług
- Typ instytucji (GOV/NGO)
- Odległość od użytkownika
- Możliwość rozwinięcia/schowania szczegółów

---

## 📥 Import danych

Do importu instytucji służy customowa komenda:

```bash
python manage.py import_with_opencage institutions.csv
Używana tylko raz – w celu uzyskania dokładnych współrzędnych dla bazy ponad 3000 instytucji.

🌍 Deployment (Railway)
Projekt przystosowany do wdrożenia na platformie Railway:

Wymagane zmienne środowiskowe:

DJANGO_SECRET_KEY

DEBUG

OPENCAGE_API_KEY

Baza danych: PostgreSQL z PostGIS (Railway wspiera)

Frontend nie wymaga osobnego builda

📁 Pliki konfiguracyjne
.env.example – szablon do własnych zmiennych środowiskowych

.gitignore – ignoruje CSV, klucze, środowiska, pliki tymczasowe

📜 Licencja
Projekt dedykowany na potrzeby Fundacji Czas Kobiet.
Użycie komercyjne lub zewnętrzne tylko za zgodą autora i fundacji.

Dziękujemy za wsparcie i współtworzenie systemu pomocy dla kobiet! 💜