# Stage 1: Build do Frontend React
FROM node:18-alpine AS frontend-builder
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY frontend ./frontend
COPY vite.config.js build-template.js ./
RUN npm run build

# Stage 2: Imagem final com Flask
FROM python:3.8-slim
WORKDIR /src
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /src

# Copia os arquivos buildados do React da stage anterior
COPY --from=frontend-builder /app/static/frontend /src/static/frontend
COPY --from=frontend-builder /app/templates/react_index.html /src/templates/react_index.html

EXPOSE 5000

ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]