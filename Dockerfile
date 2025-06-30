# 🌍 BAZA z bibliotekami GIS
FROM python:3.12-slim

# 🧰 Zainstaluj zależności systemowe
RUN apt-get update && apt-get install -y \
    binutils \
    gdal-bin \
    libproj-dev \
    libgdal-dev \
    libgeos-dev \
    libpq-dev \
    gcc \
    && apt-get clean

# 🧪 Ustaw GDAL/GEOS w zmiennych środowiskowych
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV LD_LIBRARY_PATH=/usr/lib

# 🔧 Ustaw katalog roboczy
WORKDIR /app

# 📦 Skopiuj zależności
COPY requirements.txt .

# 🧪 Instaluj zależności Pythona
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 📂 Skopiuj cały kod projektu
COPY . .

# 🧭 Port i serwer
EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
