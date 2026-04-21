FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Data directory for SQLite
RUN mkdir -p /app/data

EXPOSE 5051

CMD ["python3", "app/app.py"]
