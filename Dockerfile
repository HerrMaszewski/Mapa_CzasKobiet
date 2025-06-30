FROM osgeo/gdal:ubuntu-full-3.6.2

# 🐍 Instalacja Pythona i narzędzi
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev python3-setuptools python-is-python3 gcc

# 🧪 GDAL ENV (niektóre projekty tego wymagają)
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV LD_LIBRARY_PATH=/usr/lib

# 🔧 Katalog roboczy
WORKDIR /app

# 📦 Instalacja zależności
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 📁 Kod źródłowy
COPY . .

# 🌍 Serwer
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]