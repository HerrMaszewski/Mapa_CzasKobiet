FROM python:3.12-slim

# 📦 System dependencies
RUN apt-get update && apt-get install -y \
    binutils \
    gdal-bin \
    libproj-dev \
    libgdal-dev \
    libgeos-dev \
    libpq-dev \
    gcc \
    && apt-get clean

# 🩹 Fix GDAL – utwórz symboliczny link
RUN ln -s /usr/lib/libgdal.so.* /usr/lib/libgdal.so || true

# 🧪 GDAL ENV vars
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV LD_LIBRARY_PATH=/usr/lib

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]