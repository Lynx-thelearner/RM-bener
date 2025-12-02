#DockerFile for Python FastAPI application
FROM python:3.13-slim

# Set Direktori Kerja
WORKDIR /app

# Salin file requirements.txt dan install dependencies
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Salin seluruh kode aplikasi ke dalam container
COPY . .

# Expose port yang digunakan oleh FastAPI
EXPOSE 8000

# Jalankan aplikasi menggunakan uv dengan uv run uvicorn
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]