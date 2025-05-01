# backend/cookie-fetcher/Dockerfile
FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    ca-certificates libasound2 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libgbm1 libnotify4 libnss3 libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 \
    libxext6 libxfixes3 libxrandr2 libxss1 libxtst6 libpangocairo-1.0-0 libpango-1.0-0 \
    libcairo2 libsqlite3-0 libgtk-3-0 xvfb fonts-liberation \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# если playwright не указан в requirements.txt
RUN pip install playwright \
 && playwright install chromium \
 && playwright install-deps

# Копируем код сервиса и entrypoint
COPY entrypoint.sh /app/entrypoint.sh
COPY cookie_service.py /app/cookie_service.py
RUN chmod +x entrypoint.sh

EXPOSE 8041

ENTRYPOINT ["./entrypoint.sh"]
