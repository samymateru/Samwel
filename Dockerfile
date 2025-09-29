FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ✅ Copy only requirements first (so this layer is cached unless requirements change)
COPY requirements.txt .

# Install dependencies
RUN pip install  -r requirements.txt

# ✅ Copy the rest of the code AFTER installing dependencies
COPY . .

EXPOSE 8001

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
