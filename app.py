import streamlit as st
import pandas as pd

st.set_page_config(page_title="NBA Projections", layout="wide")
st.title("NBA Player Projections")

df = pd.DataFrame({
    "player_name": ["Luka Doncic", "Stephen Curry", "Jayson Tatum"],
    "playerteamName": ["Mavericks", "Warriors", "Celtics"],
    "opponentteamName": ["Lakers", "Suns", "Bucks"],
    "predicted_points": [27.9, 28.4, 25.3]
})

st.sidebar.header("Filtros")

teams = ["All"] + sorted(df["playerteamName"].unique().tolist())
team_selected = st.sidebar.selectbox("Equipo", teams)

players = ["All"] + sorted(df["player_name"].unique().tolist())
player_selected = st.sidebar.selectbox("Jugador", players)

filtered = df.copy()
if team_selected != "All":
    filtered = filtered[filtered["playerteamName"] == team_selected]
if player_selected != "All":
    filtered = filtered[filtered["player_name"] == player_selected]

st.metric("Jugadores mostrados", len(filtered))
st.dataframe(filtered.sort_values("predicted_points", ascending=False), use_container_width=True)
