# Update to Python 3.13
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install system dependencies and Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p challenges data final_challenges

# Expose port 8501 (Streamlit's default port)
EXPOSE 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["streamlit", "run", "CodeGen.py", "--server.port=8501", "--server.address=0.0.0.0"] 