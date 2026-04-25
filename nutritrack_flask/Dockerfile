# Use a lightweight Python image
FROM python:3.9-slim

# Install system dependencies required for OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy python dependencies file
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the flask application
COPY . .

# Expose the port Hugging Face Spaces uses
EXPOSE 7860

# Start the Flask app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
