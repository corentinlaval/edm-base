"""Vérifie que l'environnement est prêt pour le cours."""
import os
import platform
import sys
import time
import urllib.request
from importlib.metadata import version
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Diagnostic", page_icon="🩺")
st.title("Diagnostic de l'environnement")

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
resultats = []


def verifier(nom, fonction):
    try:
        detail = fonction()
        resultats.append((True, nom, detail))
    except Exception as e:  # on veut afficher toute erreur, pas planter
        resultats.append((False, nom, f"{type(e).__name__} : {e}"))


verifier("Python", lambda: sys.version.split()[0])
verifier("Architecture", lambda: platform.machine())
verifier("Streamlit", lambda: version("streamlit"))
verifier("pandas", lambda: version("pandas"))
verifier("Cœurs CPU disponibles", lambda: str(os.cpu_count()))
verifier("Lecture des données", lambda: f"{len(list(DATA_DIR.glob('*')))} fichier(s) dans {DATA_DIR}")


def test_ecriture():
    f = DATA_DIR / "_test_ecriture.txt"
    f.write_text(f"ok {time.time()}")
    f.unlink()
    return "le volume data/ est bien monté en écriture"


verifier("Écriture dans data/", test_ecriture)

for ok, nom, detail in resultats:
    (st.success if ok else st.error)(f"**{nom}** — {detail}")

st.subheader("Accès réseau depuis le conteneur")
st.write("Utile plus tard pour télécharger des modèles. Facultatif aujourd'hui.")
if st.button("Tester l'accès à Internet"):
    for url in ["https://pypi.org", "https://huggingface.co"]:
        try:
            t0 = time.time()
            urllib.request.urlopen(url, timeout=5)
            st.success(f"{url} joignable ({time.time() - t0:.1f} s)")
        except Exception as e:
            st.warning(f"{url} injoignable : {e}. Proxy de l'école ? Voir le README.")

st.subheader("Rechargement automatique")
st.write(
    f"Heure de chargement de la page : **{time.strftime('%H:%M:%S')}**. "
    "Modifiez puis enregistrez ce fichier : si l'heure change sans relancer Docker, "
    "le rechargement automatique fonctionne."
)
