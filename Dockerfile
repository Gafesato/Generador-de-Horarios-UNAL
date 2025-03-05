# Use a lightweight Python image
FROM python:3.9

# Install system dependencies required by Flet
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

# Sets the working directory inside the container
WORKDIR /generator

# Copy the contents of the project to the container
COPY . /generator

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port if the application needs one
EXPOSE 8080

# Command to run the application
CMD ["python", "-m", "generator.main"]
