# Use official Python image
FROM python:3.11-slim

# Install build essentials, pkg-config, and libmariadb-dev
# libmariadb-dev replaces libmysqlclient-dev on Debian-based images
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

#install Gunicorn (for production-ready server)
RUN pip install gunicorn

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Add MySQL client for debugging purposes - REMOVE THIS LINE LATER!
#RUN apt-get update && apt-get install -y default-mysql-client && rm -rf /var/lib/apt/lists/*


# Copy app source
COPY . .

# Expose port
EXPOSE 5000

# Run app
CMD ["gunicorn", "--workers", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "run:app"]
