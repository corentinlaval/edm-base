# Image de base du cours EDM — Exploration de données multimodales
# Volontairement légère : Python + Streamlit + pandas uniquement.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dépendances d'abord (mise en cache Docker : pas de réinstallation si seul le code change)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Code et données (remplacés par les volumes en développement, voir docker-compose.yml)
COPY app/ ./app/
COPY data/ ./data/

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health', timeout=3)" || exit 1

# runOnSave + poll : l'appli se recharge dès qu'on enregistre un fichier, y compris sous Windows
CMD ["streamlit", "run", "app/Accueil.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--browser.serverAddress=localhost", \
     "--server.runOnSave=true", \
     "--server.fileWatcherType=poll", \
     "--browser.gatherUsageStats=false"]
