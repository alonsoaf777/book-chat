# Etapa 1: Construcción del frontend
FROM node:18 AS frontend-builder
WORKDIR /frontend
COPY frontend/ .
RUN npm install
RUN npm run build

# Etapa 2: backend FastAPI + copiar build del frontend
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copiar el build de React al backend
COPY --from=frontend-builder /frontend/build ./static

EXPOSE 80
ENTRYPOINT ["uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "80"]
