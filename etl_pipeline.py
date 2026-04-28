import pandas as pd
import numpy as np
import os

def run_etl_pipeline():
    print("🚀 Starting IPL ETL Pipeline...")
    
    # 1. EXTRACT: Read the raw data
    try:
        df_matches = pd.read_csv('matches.csv')
        df_deliveries = pd.read_csv('deliveries.csv')
        print("✅ Data Extraction Successful.")
    except FileNotFoundError:
        print("❌ Error: Raw data files not found. Please run generate_sample_data.py first.")
        return

    # 2. TRANSFORM: Clean and Engineer Features
    print("🔄 Transforming Data...")
    
    # A. Handling Missing Values (Imputing City based on Venue)
    venue_city_map = {
        'Wankhede Stadium': 'Mumbai',
        'M.Chinnaswamy Stadium': 'Bangalore',
        'Eden Gardens': 'Kolkata',
        'Arun Jaitley Stadium': 'Delhi',
        'MA Chidambaram Stadium': 'Chennai',
        'Rajiv Gandhi International Stadium': 'Hyderabad'
    }
    df_matches['city'] = df_matches['city'].fillna(df_matches['venue'].map(venue_city_map))
    
    # B. Standardize Team Names (Handling legacy names if any exist)
    team_mapping = {
        'Delhi Daredevils': 'Delhi Capitals',
        'Kings XI Punjab': 'Punjab Kings',
        'Deccan Chargers': 'Sunrisers Hyderabad'
    }
    df_matches['team1'] = df_matches['team1'].replace(team_mapping)
    df_matches['team2'] = df_matches['team2'].replace(team_mapping)
    df_matches['winner'] = df_matches['winner'].replace(team_mapping)
    
    # C. Feature Engineering (Creating Calculated Columns)
    # Calculate Powerplay Runs (Overs 0-5)
    powerplay_df = df_deliveries[df_deliveries['over'] < 6].groupby(['match_id', 'batting_team'])['total_runs'].sum().reset_index()
    powerplay_df.rename(columns={'total_runs': 'powerplay_runs'}, inplace=True)
    
    # Calculate Death Overs Runs (Overs 15-19)
    death_overs_df = df_deliveries[df_deliveries['over'] >= 15].groupby(['match_id', 'batting_team'])['total_runs'].sum().reset_index()
    death_overs_df.rename(columns={'total_runs': 'death_overs_runs'}, inplace=True)
    
    # 3. LOAD: Save the Cleaned & Transformed Data
    # Create an 'output' directory if it doesn't exist
    if not os.path.exists('clean_data'):
        os.makedirs('clean_data')
        
    df_matches.to_csv('clean_data/matches_clean_etl.csv', index=False)
    powerplay_df.to_csv('clean_data/powerplay_stats.csv', index=False)
    death_overs_df.to_csv('clean_data/death_overs_stats.csv', index=False)
    
    print("✅ Transformation Complete.")
    print("✅ Data Successfully Loaded into /clean_data folder.")
    print("🎉 ETL Pipeline Finished!")

if __name__ == "__main__":
    run_etl_pipeline()
