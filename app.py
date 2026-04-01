import streamlit as st
import pandas as pd

st.set_page_config(page_title="NBA Projections", layout="wide")
st.title("NBA Player Projections")

@st.cache_data
def load_data():
    df = pd.read_csv("predictions_today.csv")
    df["game_date"] = pd.to_datetime(df["game_date"], errors="coerce")
    df["year"] = df["game_date"].dt.year
    return df

df = load_data()

# Rename columns only for display
rename_map = {
    "player_name": "Player Name",
    "playerteamName": "Team",
    "opponentteamName": "Opponent",
    "game_date": "Game Date",
    "predicted_points": "Predicted Points",
    "predicted_assists": "Predicted Assists",
    "predicted_rebounds": "Predicted Rebounds",
    "predicted_fga": "Predicted FGA",
    "predicted_threepa": "Predicted 3PA",
    "year": "Year"
}

df = df.rename(columns=rename_map)

st.sidebar.header("Filters")

years = ["All"] + sorted([str(int(y)) for y in df["Year"].dropna().unique()])
year_selected = st.sidebar.selectbox("Year", years)

teams = ["All"] + sorted(df["Team"].dropna().unique().tolist())
team_selected = st.sidebar.selectbox("Team", teams)

players = ["All"] + sorted(df["Player Name"].dropna().unique().tolist())
player_selected = st.sidebar.selectbox("Player", players)

filtered = df.copy()

if year_selected != "All":
    filtered = filtered[filtered["Year"] == int(year_selected)]

if team_selected != "All":
    filtered = filtered[filtered["Team"] == team_selected]

if player_selected != "All":
    filtered = filtered[filtered["Player Name"] == player_selected]

st.metric("Players shown", len(filtered))

# Show only columns that actually exist
preferred_cols = [
    "Player Name",
    "Team",
    "Opponent",
    "Game Date",
    "Predicted Points",
    "Predicted Assists",
    "Predicted Rebounds",
    "Predicted FGA",
    "Predicted 3PA"
]

cols_to_show = [c for c in preferred_cols if c in filtered.columns]

if len(filtered) > 0:
    sort_col = "Predicted Points" if "Predicted Points" in filtered.columns else cols_to_show[-1]
    st.dataframe(
        filtered.sort_values(sort_col, ascending=False)[cols_to_show],
        use_container_width=True
    )
else:
    st.warning("No rows match the selected filters.")
