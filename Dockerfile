FROM osgeo/gdal:ubuntu-full-3.6.2

# 🐍 Python + pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    gcc \
    gdal-bin \
    libproj-dev \
    libgdal-dev \
    libgeos-dev \
    libpq-dev \
    && ln -sf /usr/lib/x86_64-linux-gnu/libgdal.so /usr/lib/libgdal.so \
    && apt-get clean

# 🔧 Zmienne środowiskowe dla GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu
ENV PYTHONUNBUFFERED=1

# 🔧 Katalog roboczy
WORKDIR /app

# 📦 Zależności Pythona
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

# 📁 Kod źródłowy
COPY . .

# 🌍 Serwer
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
