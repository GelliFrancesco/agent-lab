FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 5050

# Run the dashboard (scheduler runs in same process)
CMD ["python3", "soccer_dashboard.py"]
