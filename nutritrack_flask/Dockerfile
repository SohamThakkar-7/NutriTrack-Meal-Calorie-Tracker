# Use a lightweight Python image
FROM python:3.9-slim

# Install system dependencies required for OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up a new user with user ID 1000 (Required by Hugging Face)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy requirements and install
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY --chown=user . .

# Expose the port Hugging Face Spaces uses
EXPOSE 7860

# Start the Flask app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
