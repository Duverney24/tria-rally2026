# TRIA: API (FastAPI) + prototipo en un solo contenedor. Funciona sin internet una vez construida.
#   docker build -t tria .
#   docker run -p 8000:8000 tria                      → http://localhost:8000
#   docker run -p 8000:8000 -e TRIA_CLAVE=... tria    → exige clave en las rutas que cambian el estado
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

# Dependencias primero para aprovechar la caché de capas
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY tria/ tria/
COPY datos/ datos/
COPY prototipo/ prototipo/

# Usuario sin privilegios
RUN useradd --create-home --uid 10001 tria
USER tria

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import os,urllib.request;urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\",\"8000\")}/version',timeout=2)" || exit 1

CMD ["sh", "-c", "uvicorn tria.api:app --host 0.0.0.0 --port ${PORT}"]
