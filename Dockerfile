FROM python:3.9-slim

WORKDIR /app

# Cài đặt các dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Chạy bot
CMD ["python", "src/main.py"] 