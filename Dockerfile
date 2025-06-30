FROM osgeo/gdal:ubuntu-full-3.6.2

# 🐍 Instalacja Pythona i narzędzi
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    binutils \
    gdal-bin \
    libproj-dev \
    libgdal-dev \
    libgeos-dev \
    libpq-dev \
    gcc \
    && ln -sf /usr/lib/x86_64-linux-gnu/libgdal.so /usr/lib/libgdal.so \
    && apt-get clean

# 🧪 Ustaw GDAL/GEOS w zmiennych środowiskowych
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu

# 🔧 Katalog roboczy
WORKDIR /app

# 📦 Instalacja zależności
COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# 📁 Kod źródłowy
COPY . .

# 🌍 Serwer
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
