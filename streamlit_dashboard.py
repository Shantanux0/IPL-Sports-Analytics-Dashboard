import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE SETUP ---
st.set_page_config(page_title="IPL Analytics Dashboard", page_icon="🏏", layout="wide")

# --- CUSTOM CSS FOR DARK PREMIUM THEME ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    h1, h2, h3 { color: #F2C811; }
    .stMetric { background-color: #262730; padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    matches = pd.read_csv('matches.csv')
    deliveries = pd.read_csv('deliveries.csv')
    return matches, deliveries

try:
    matches, deliveries = load_data()
except FileNotFoundError:
    st.error("Data files not found. Please run generate_sample_data.py first.")
    st.stop()

# --- HEADER ---
st.title("🏏 IPL Sports Analytics Dashboard")
st.markdown("Interactive analysis of match results, player performances, and team statistics.")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")
selected_season = st.sidebar.selectbox("Select Season", ["All"] + list(matches['season'].unique()))
selected_team = st.sidebar.selectbox("Select Team", ["All"] + list(matches['team1'].unique()))

# Apply Filters
filtered_matches = matches.copy()
filtered_deliveries = deliveries.copy()

if selected_season != "All":
    filtered_matches = filtered_matches[filtered_matches['season'] == str(selected_season)]
    filtered_deliveries = filtered_deliveries[filtered_deliveries['match_id'].isin(filtered_matches['match_id'])]

if selected_team != "All":
    filtered_matches = filtered_matches[(filtered_matches['team1'] == selected_team) | (filtered_matches['team2'] == selected_team)]
    filtered_deliveries = filtered_deliveries[(filtered_deliveries['batting_team'] == selected_team) | (filtered_deliveries['bowling_team'] == selected_team)]


# --- KPI METRICS ---
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(label="Total Matches", value=len(filtered_matches))
with col2:
    st.metric(label="Total Runs", value=int(filtered_deliveries['total_runs'].sum()))
with col3:
    st.metric(label="Total Wickets", value=int(filtered_deliveries['is_wicket'].sum()))
with col4:
    sixes = int((filtered_deliveries['batsman_runs'] == 6).sum())
    st.metric(label="Total Sixes", value=sixes)
with col5:
    fours = int((filtered_deliveries['batsman_runs'] == 4).sum())
    st.metric(label="Total Fours", value=fours)

st.markdown("---")

# --- ROW 1 VISUALS ---
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("🏆 Matches Won by Team")
    wins = filtered_matches['winner'].value_counts().reset_index()
    wins.columns = ['Team', 'Wins']
    fig_wins = px.bar(wins, x='Wins', y='Team', orientation='h', color='Team', 
                      title="Total Wins per Franchise")
    st.plotly_chart(fig_wins, use_container_width=True)

with col_chart2:
    st.subheader("🪙 Toss Decision vs Match Result")
    toss_data = filtered_matches.copy()
    toss_data['Won Match'] = toss_data['toss_winner'] == toss_data['winner']
    toss_data['Won Match'] = toss_data['Won Match'].map({True: 'Won Match', False: 'Lost Match'})
    fig_toss = px.histogram(toss_data, x='toss_decision', color='Won Match', barmode='group',
                            title="Impact of Batting vs Fielding First",
                            color_discrete_map={'Won Match': '#00CC96', 'Lost Match': '#EF553B'})
    st.plotly_chart(fig_toss, use_container_width=True)

# --- ROW 2 VISUALS ---
col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    st.subheader("🏏 Top 10 Run Scorers")
    top_batsmen = filtered_deliveries.groupby('batter')['batsman_runs'].sum().reset_index().sort_values(by='batsman_runs', ascending=False).head(10)
    fig_bat = px.bar(top_batsmen, x='batter', y='batsman_runs', color='batsman_runs',
                     color_continuous_scale='Oranges', title="Highest Run Aggregates")
    st.plotly_chart(fig_bat, use_container_width=True)

with col_chart4:
    st.subheader("🎯 Top 10 Wicket Takers")
    # Only count actual wickets
    wickets = filtered_deliveries[filtered_deliveries['is_wicket'] == 1]
    top_bowlers = wickets.groupby('bowler')['is_wicket'].sum().reset_index().sort_values(by='is_wicket', ascending=False).head(10)
    fig_bowl = px.bar(top_bowlers, x='bowler', y='is_wicket', color='is_wicket',
                      color_continuous_scale='Purples', title="Highest Wicket Takers")
    st.plotly_chart(fig_bowl, use_container_width=True)
