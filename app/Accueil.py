"""Page d'accueil de l'explorateur multimodal — cours EDM."""
from pathlib import Path

import pandas as pd
import streamlit as st

# --- À MODIFIER PAR L'ÉTUDIANT -------------------------------------------
NOM_ETUDIANT = "Prénom Nom"
# -------------------------------------------------------------------------

DATA = Path(__file__).resolve().parent.parent / "data" / "exemple.csv"

st.set_page_config(page_title="Explorateur multimodal", page_icon="🔎", layout="wide")

st.title("Explorateur multimodal")
st.caption(f"Projet EDM — {NOM_ETUDIANT}")

if NOM_ETUDIANT == "Prénom Nom":
    st.info("Modifiez `NOM_ETUDIANT` dans `app/Accueil.py`, enregistrez : la page se met à jour toute seule.")
else:
    st.success(f"Bienvenue {NOM_ETUDIANT}, votre environnement fonctionne.")

st.subheader("Jeu de données d'exemple")
try:
    df = pd.read_csv(DATA)
except FileNotFoundError:
    st.error(f"Fichier introuvable : {DATA}")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Objets", len(df))
col2.metric("Modalités", df["modalite"].nunique())
col3.metric("Années couvertes", f"{df['annee'].min()}–{df['annee'].max()}")

modalites = st.multiselect("Filtrer par modalité", sorted(df["modalite"].unique()))
vue = df[df["modalite"].isin(modalites)] if modalites else df
st.dataframe(vue, use_container_width=True, hide_index=True)

st.bar_chart(df["modalite"].value_counts())

st.divider()
st.write("En cas de problème, ouvrez la page **Diagnostic** dans le menu de gauche.")
