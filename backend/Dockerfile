FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8080
ENTRYPOINT ["bash", "-lc"]
CMD [ "uvicorn app:app --host 0.0.0.0 --port 8080 --reload" ]
