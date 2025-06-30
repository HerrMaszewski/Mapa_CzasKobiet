FROM osgeo/gdal:ubuntu-full-3.6.2

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Warsaw

# 🐍 Python + pip + GDAL
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-gdal \
    gcc \
    gdal-bin \
    libproj-dev \
    libgdal-dev \
    libgeos-dev \
    libpq-dev \
    tzdata \
    && apt-get clean

# 🔗 Link do GDAL
RUN find /usr/lib -name "libgdal.so*" && \
    ln -sf $(find /usr/lib -name "libgdal.so*" | grep -E '\.so(\.[0-9]+)?$' | head -n 1) /usr/lib/libgdal.so

# 🔧 Środowisko
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu
ENV PYTHONUNBUFFERED=1

# 🗂️ Projekt
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
COPY . .

# 🚀 Uruchomienie
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
