# Usa una imagen ligera de Python
FROM python:3.9

# Instala dependencias del sistema necesarias para Flet
RUN apt-get update && apt-get install -y \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-libav \
    gstreamer1.0-alsa \
    gstreamer1.0-pulseaudio \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /generator

# Copia el contenido del proyecto al contenedor
COPY . /generator

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone un puerto si la aplicación necesita uno
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["python", "-m", "generator.main"]
