# app.py — OPA-AC 2025 — Interface officielle magnifique
import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

st.set_page_config(
    page_title="OPA-AC 2025 | ISSEA",
    page_icon="https://opa-ac.issea-cemac.org/wp-content/uploads/2024/01/logo-opa-ac-2024.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== STYLE MAGNIFIQUE =====================
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #003399 0%, #006600 100%); padding: 2rem; border-radius: 20px;}
    h1, h2, h3 {font-family: 'Georgia', serif; color: #FFD700; text-shadow: 2px 2px 4px #000;}
    .header-title {font-size: 4.5rem !important; font-weight: 900;}
    .stButton>button {background: linear-gradient(45deg, #FFD700, #FFA500); color: #003399; 
                      font-weight: bold; border-radius: 50px; padding: 15px 40px; font-size: 1.3rem;}
    .stMetric {background: rgba(255,255,255,0.2); border-radius: 20px; padding: 1.5rem; backdrop-filter: blur(10px);}
    .footer {text-align: center; color: #FFD700; font-size: 1.2rem; margin-top: 4rem; padding: 2rem;}
</style>
""", unsafe_allow_html=True)

# ===================== CONNEXION NEON =====================
@st.cache_resource
def get_conn():
    return psycopg2.connect(
        host=os.getenv("PG_HOST"),
        database=os.getenv("PG_DBNAME"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        sslmode="require"
    )
conn = get_conn()

# ===================== HEADER OFFICIEL =====================
st.markdown("<div class='main'>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 3, 1])
with c1:
    st.image("www/logo-issea.png", width=180)
with c2:
    st.markdown("<h1 class='header-title'>OPA-AC</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#f0f0f0; font-size:1.8rem;'>Observatoire régional des Pratiques Anormales<br>sur les Principaux Corridors de l’Afrique Centrale</p>", unsafe_allow_html=True)
with c3:
    st.image("www/logo-ue.png", width=120)
st.markdown("**Coopération Cameroun – Union Européenne | Contrat N°FED/2019/413-035**")
st.markdown("</div>", unsafe_allow_html=True)

# ===================== SIDEBAR =====================
with st.sidebar:
    st.image("www/logo-opa-ac.png", width=220)
    page = st.radio("Navigation", ["Accueil", "Saisie", "Tableau de bord", "À propos"])

# ===================== PAGES =====================
if page == "Accueil":
    st.image("www/carte-corridors-2025.png", use_column_width=True)
    st.success("Application connectée à la base Neon.tech")

elif page == "Saisie":
    st.markdown("<h2>Nouveau Questionnaire 2025</h2>", unsafe_allow_html=True)
    with st.form("form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            code_agent = st.text_input("Code agent", "CM001")
            annee = st.number_input("Année", 2020, 2030, 2025)
            trimestre = st.selectbox("Trimestre", ["T1","T2","T3","T4"])
            corridor = st.selectbox("Corridor", ["DB - Douala→Bangui", "DN - Douala→N’Djamena", "YL - Yaoundé→Libreville"])
        with col2:
            sens = st.radio("Sens", ["Aller", "Retour"], horizontal=True)
            charge = st.radio("Camion chargé ?", ["Oui", "Non"], horizontal=True)
            poids_autorise = st.number_input("Poids total autorisé (t)", 0.0)

        if charge == "Oui":
            type_march = st.text_input("Type de marchandise")
            poids_march = st.number_input("Poids chargement (t)", 0.1)

        submitted = st.form_submit_button("Enregistrer")
        if submitted:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO voyages (code_agent, annee, trimestre, corridor, sens, charge, poids_total_autorise, type_marchandise, poids_chargement)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (code_agent, annee, trimestre, corridor[:2], sens[0], "1" if charge=="Oui" else "2",
                  poids_autorise, type_march if charge=="Oui" else None, poids_march if charge=="Oui" else None))
            conn.commit()
            st.balloons()
            st.success("Enregistré avec succès !")

elif page == "Tableau de bord":
    df = pd.read_sql("SELECT * FROM voyages ORDER BY created_at DESC", conn)
    c1, c2, c3 = st.columns(3)
    c1.metric("Voyages", len(df))
    c2.metric("DB", len(df[df.corridor=="DB"]))
    c3.metric("DN", len(df[df.corridor=="DN"]))

    fig = px.pie(df.corridor.value_counts(), names=["DB","DN","YL"], title="Répartition")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df[['code_agent','corridor','sens','charge','created_at']], use_container_width=True)

else:
    st.markdown("### À propos")
    st.image("www/logo-cemac.png", width=200)
    st.info("Application officielle OPA-AC 2025 – ISSEA Yaoundé")

st.markdown("<div class='footer'>© 2025 ISSEA – Financé par l’Union Européenne</div>", unsafe_allow_html=True)
