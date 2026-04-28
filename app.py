import streamlit as st
import pandas as pd
import plotly.express as px
import os
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# --- PAGE SETUP ---
st.set_page_config(page_title="IPL Analytics Platform", page_icon="🏏", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    h1, h2, h3 { color: #F2C811; }
    .stMetric { background-color: #262730; padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA FUNCTION ---
@st.cache_data
def load_data():
    try:
        matches = pd.read_csv('matches.csv')
        deliveries = pd.read_csv('deliveries.csv')
        return matches, deliveries
    except FileNotFoundError:
        st.error("Data files not found. Please ensure matches.csv and deliveries.csv exist.")
        st.stop()

matches, deliveries = load_data()

# --- APP LAYOUT WITH TABS ---
st.title("🏏 IPL Advanced Data Platform")
st.markdown("A complete End-to-End Data Application featuring Analytics, ETL, and Machine Learning.")

tab1, tab2, tab3 = st.tabs(["📊 Analytics Dashboard", "⚙️ ETL Pipeline", "🤖 ML Win Predictor"])

# ==========================================
# TAB 1: ANALYTICS DASHBOARD
# ==========================================
with tab1:
    st.sidebar.header("Dashboard Filters")
    selected_season = st.sidebar.selectbox("Select Season", ["All"] + list(matches['season'].unique()))
    selected_team = st.sidebar.selectbox("Select Team", ["All"] + list(matches['team1'].unique()))

    filtered_matches = matches.copy()
    filtered_deliveries = deliveries.copy()

    if selected_season != "All":
        filtered_matches = filtered_matches[filtered_matches['season'] == str(selected_season)]
        filtered_deliveries = filtered_deliveries[filtered_deliveries['match_id'].isin(filtered_matches['match_id'])]

    if selected_team != "All":
        filtered_matches = filtered_matches[(filtered_matches['team1'] == selected_team) | (filtered_matches['team2'] == selected_team)]
        filtered_deliveries = filtered_deliveries[(filtered_deliveries['batting_team'] == selected_team) | (filtered_deliveries['bowling_team'] == selected_team)]

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("Total Matches", len(filtered_matches))
    with col2: st.metric("Total Runs", int(filtered_deliveries['total_runs'].sum()))
    with col3: st.metric("Total Wickets", int(filtered_deliveries['is_wicket'].sum()))
    with col4: st.metric("Total Sixes", int((filtered_deliveries['batsman_runs'] == 6).sum()))
    with col5: st.metric("Total Fours", int((filtered_deliveries['batsman_runs'] == 4).sum()))

    st.markdown("---")
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("🏆 Matches Won by Team")
        wins = filtered_matches['winner'].value_counts().reset_index()
        wins.columns = ['Team', 'Wins']
        fig_wins = px.bar(wins, x='Wins', y='Team', orientation='h', color='Team', title="Total Wins per Franchise")
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

# ==========================================
# TAB 2: ETL PIPELINE
# ==========================================
with tab2:
    st.header("⚙️ Automated ETL (Extract, Transform, Load)")
    st.markdown("Run the data engineering pipeline to clean data and generate advanced metrics.")
    
    if st.button("▶️ Run ETL Pipeline Now"):
        with st.spinner("Extracting and Transforming Data..."):
            # Transformation logic
            df_m = matches.copy()
            df_d = deliveries.copy()
            
            venue_city_map = {'Wankhede Stadium': 'Mumbai', 'M.Chinnaswamy Stadium': 'Bangalore', 'Eden Gardens': 'Kolkata'}
            df_m['city'] = df_m['city'].fillna(df_m['venue'].map(venue_city_map))
            
            powerplay_df = df_d[df_d['over'] < 6].groupby(['match_id', 'batting_team'])['total_runs'].sum().reset_index()
            death_overs_df = df_d[df_d['over'] >= 15].groupby(['match_id', 'batting_team'])['total_runs'].sum().reset_index()
            
            if not os.path.exists('clean_data'):
                os.makedirs('clean_data')
                
            df_m.to_csv('clean_data/matches_clean_etl.csv', index=False)
            powerplay_df.to_csv('clean_data/powerplay_stats.csv', index=False)
            death_overs_df.to_csv('clean_data/death_overs_stats.csv', index=False)
            
        st.success("✅ ETL Pipeline Completed Successfully! Clean data saved to /clean_data folder.")
        
        st.subheader("Preview: Powerplay Stats (Calculated during ETL)")
        st.dataframe(powerplay_df.head(10))

# ==========================================
# TAB 3: ML WIN PREDICTOR
# ==========================================
with tab3:
    st.header("🤖 Machine Learning Win Predictor")
    st.markdown("Uses Logistic Regression to predict which team will win based on historical match data.")
    
    # Train model automatically for demo purposes
    @st.cache_resource
    def get_ml_model(matches_df):
        df = matches_df[matches_df['result'] != 'no result'].dropna(subset=['winner'])
        
        team_encoder = LabelEncoder()
        all_teams = pd.concat([df['team1'], df['team2']]).unique()
        team_encoder.fit(all_teams)
        
        df['team1_enc'] = team_encoder.transform(df['team1'])
        df['team2_enc'] = team_encoder.transform(df['team2'])
        df['toss_winner_enc'] = team_encoder.transform(df['toss_winner'])
        df['winner_enc'] = team_encoder.transform(df['winner'])
        
        toss_decision_encoder = LabelEncoder()
        df['toss_dec_enc'] = toss_decision_encoder.fit_transform(df['toss_decision'])
        
        X = df[['team1_enc', 'team2_enc', 'toss_winner_enc', 'toss_dec_enc']]
        y = df['winner_enc']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LogisticRegression(max_iter=200)
        model.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, model.predict(X_test))
        
        return model, team_encoder, toss_decision_encoder, accuracy, all_teams
        
    model, team_encoder, toss_decision_encoder, accuracy, all_teams = get_ml_model(matches)
    
    st.info(f"Model trained successfully. Historical Accuracy: {accuracy * 100:.2f}%")
    
    st.subheader("Predict a Match")
    colA, colB = st.columns(2)
    with colA:
        team1_input = st.selectbox("Select Team 1", all_teams)
        toss_winner_input = st.selectbox("Who won the toss?", [team1_input, "Team 2"])
    with colB:
        team2_input = st.selectbox("Select Team 2", [t for t in all_teams if t != team1_input])
        toss_decision_input = st.selectbox("Toss Decision", ["bat", "field"])
        
    if toss_winner_input == "Team 2": toss_winner_input = team2_input

    if st.button("🔮 Predict Winner"):
        t1_enc = team_encoder.transform([team1_input])[0]
        t2_enc = team_encoder.transform([team2_input])[0]
        tw_enc = team_encoder.transform([toss_winner_input])[0]
        td_enc = toss_decision_encoder.transform([toss_decision_input])[0]
        
        prediction_enc = model.predict([[t1_enc, t2_enc, tw_enc, td_enc]])
        predicted_winner = team_encoder.inverse_transform(prediction_enc)[0]
        
        probabilities = model.predict_proba([[t1_enc, t2_enc, tw_enc, td_enc]])[0]
        
        st.success(f"🏆 Predicted Winner: **{predicted_winner}**")
        st.write("Win Probability breakdown:")
        st.progress(max(probabilities))
