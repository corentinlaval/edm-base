# Explorateur multimodal — base du cours EDM

Environnement commun du cours *Exploration de données multimodales* (Télécom Saint-Étienne).
Une seule commande lance l'application, sur Windows, macOS (Intel ou Apple Silicon) et Linux.

## Prérequis

- Docker Desktop (Windows / macOS) ou Docker Engine (Linux), en cours d'exécution
- Git
- Un éditeur (VS Code conseillé)

## Lancer l'application

```bash
git clone <url-de-votre-depot>
cd edm-base
docker compose pull     # télécharge l'image du cours (ghcr.io/corentinlaval/edm-base)
docker compose up
```

Puis ouvrez **http://localhost:8501** dans votre navigateur.

Quand l'enseignant annonce une mise à jour de l'environnement : `docker compose pull`, puis `docker compose up`.
Si le téléchargement échoue, reconstruisez l'image localement : `docker compose up --build`.
N'utilisez pas `http://0.0.0.0:8501` : sur le réseau de l'université, le proxy la bloque (« Access Denied »).

Le premier lancement télécharge l'image (environ 400 Mo). Les suivants démarrent en quelques secondes.

Arrêter : `Ctrl + C`, ou `docker compose down`.

## Sans Docker sur la machine : GitHub Codespaces

Rien à installer, un navigateur suffit (compte GitHub personnel requis, quota gratuit mensuel).

1. Sur la page GitHub de votre dépôt : **Code → Codespaces → Create codespace on main**.
2. Attendez la construction (2 à 4 min la première fois) : VS Code s'ouvre dans le navigateur.
3. L'application démarre toute seule ; un onglet s'ouvre sur l'adresse fournie par GitHub
   (sinon : onglet **Ports** en bas, ligne 8501, icône globe).
4. En fin de séance : **Code → Codespaces → … → Stop codespace**, pour ne pas consommer le quota.

## Travailler

- Le code est dans `app/`, les données dans `data/`.
- Modifiez un fichier et enregistrez : l'application se recharge toute seule, sans relancer Docker.
- Une nouvelle page = un nouveau fichier dans `app/pages/` (ex. `2_Images.py`).
- Une nouvelle bibliothèque = une ligne dans `requirements.txt`, puis `docker compose up --build`.

## Structure

```
edm-base/
├── Dockerfile            # recette de l'image
├── docker-compose.yml    # lancement en une commande
├── requirements.txt      # bibliothèques Python (versions fixées)
├── app/
│   ├── Accueil.py        # page d'accueil
│   └── pages/
│       └── 1_Diagnostic.py
└── data/
    └── exemple.csv
```

## Réseau de l'université (proxy)

Sur un poste de l'université, Docker doit passer par le proxy pour télécharger les images et les bibliothèques.

1. Docker Desktop → Settings → Resources → Proxies → **Manual configuration** :
   - Web Server (HTTP) : `http://cache.univ-st-etienne.fr:3128`
   - Secure Web Server (HTTPS) : `http://cache.univ-st-etienne.fr:3128`
   - Bypass : `localhost, 127.0.0.1, .univ-st-etienne.fr`
   - Containers proxy : *Same as host proxy*
   Puis **Apply** (Docker Desktop redémarre).
2. Vérifiez que la commande `docker` utilise bien Docker Desktop : `docker context ls` doit marquer `desktop-linux *`
   (sinon : `docker context use desktop-linux`).
3. Téléchargez l'image de base une première fois : `docker pull python:3.11-slim`
4. Lancez : `docker compose up --build`
5. Ouvrez **http://localhost:8501** (si le proxy s'interpose encore : http://127.0.0.1:8501).

## En cas de problème

Ouvrez d'abord la page **Diagnostic** de l'application.

| Symptôme | Cause probable | Solution |
| --- | --- | --- |
| `docker: command not found` ou Docker Desktop ne démarre pas | Docker non installé ou non lancé | Lancer Docker Desktop et attendre qu'il soit prêt |
| « Virtualization not enabled » / WSL 2 manquant (Windows) | Virtualisation désactivée dans le BIOS, ou WSL non installé | `wsl --install` (droits administrateur), ou s'adresser au service informatique |
| `port is already allocated` | Le port 8501 est déjà pris | Dans `docker-compose.yml`, remplacer `"8501:8501"` par `"8502:8501"`, puis ouvrir http://localhost:8502 |
| `DeadlineExceeded` sur `load metadata for docker.io/...` | Docker ne joint pas Docker Hub (proxy) | Suivre la section « Réseau de l'université », puis `docker pull python:3.11-slim` avant de relancer |
| Échec du `pip install` pendant la construction | Proxy de l'école | Renseigner le proxy dans Docker Desktop → Settings → Resources → Proxies |
| Page « Access Denied » de cache.univ-st-etienne.fr | Le navigateur envoie l'adresse au proxy | Utiliser http://localhost:8501, pas 0.0.0.0 |
| La page ne se recharge pas après modification | Surveillance des fichiers | Rafraîchir le navigateur (F5) ; vérifier que le fichier est bien enregistré |
| `permission denied` sur Linux | Utilisateur hors du groupe docker | `sudo usermod -aG docker $USER`, puis se reconnecter |
