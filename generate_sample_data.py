import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_sample_data(num_matches=50):
    teams = ['Chennai Super Kings', 'Mumbai Indians', 'Royal Challengers Bangalore', 
             'Kolkata Knight Riders', 'Delhi Capitals', 'Sunrisers Hyderabad', 
             'Rajasthan Royals', 'Punjab Kings']
    venues = ['Wankhede Stadium', 'M.Chinnaswamy Stadium', 'Eden Gardens', 
              'Arun Jaitley Stadium', 'MA Chidambaram Stadium', 'Rajiv Gandhi International Stadium']
    cities = ['Mumbai', 'Bangalore', 'Kolkata', 'Delhi', 'Chennai', 'Hyderabad']
    
    players_dict = {
        'Chennai Super Kings': ['MS Dhoni', 'R Gaikwad', 'R Jadeja', 'D Chahar'],
        'Mumbai Indians': ['R Sharma', 'I Kishan', 'S Yadav', 'J Bumrah'],
        'Royal Challengers Bangalore': ['V Kohli', 'F du Plessis', 'G Maxwell', 'M Siraj'],
        'Kolkata Knight Riders': ['S Iyer', 'A Russell', 'S Narine', 'V Chakravarthy'],
        'Delhi Capitals': ['R Pant', 'D Warner', 'A Patel', 'K Yadav'],
        'Sunrisers Hyderabad': ['A Markram', 'H Klaasen', 'B Kumar', 'T Natarajan'],
        'Rajasthan Royals': ['S Samson', 'J Buttler', 'Y Jaiswal', 'Y Chahal'],
        'Punjab Kings': ['S Dhawan', 'L Livingstone', 'S Curran', 'A Singh']
    }

    matches_data = []
    deliveries_data = []

    start_date = datetime(2023, 3, 31)
    
    match_id = 1
    for i in range(num_matches):
        team1, team2 = random.sample(teams, 2)
        venue_idx = random.randint(0, len(venues)-1)
        venue = venues[venue_idx]
        city = cities[venue_idx]
        date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        season = '2023'
        
        toss_winner = random.choice([team1, team2])
        toss_decision = random.choice(['bat', 'field'])
        
        # Simple simulation for winner
        winner = random.choice([team1, team2])
        result = 'normal'
        result_margin = random.randint(1, 50)
        player_of_match = random.choice(players_dict[winner])

        matches_data.append({
            'match_id': match_id,
            'season': season,
            'date': date,
            'city': city,
            'venue': venue,
            'team1': team1,
            'team2': team2,
            'toss_winner': toss_winner,
            'toss_decision': toss_decision,
            'winner': winner,
            'result': result,
            'result_margin': result_margin,
            'player_of_match': player_of_match
        })

        # Generate deliveries for this match
        for inning, batting_team in enumerate([team1, team2], 1):
            bowling_team = team2 if batting_team == team1 else team1
            batters = players_dict[batting_team]
            bowlers = players_dict[bowling_team]
            
            batter_idx = 0
            non_striker_idx = 1
            
            for over in range(20):
                bowler = random.choice(bowlers)
                for ball in range(1, 7):
                    batsman_runs = random.choices([0, 1, 2, 3, 4, 6], weights=[40, 30, 5, 1, 12, 12])[0]
                    extra_runs = random.choices([0, 1], weights=[95, 5])[0]
                    total_runs = batsman_runs + extra_runs
                    
                    is_wicket = random.choices([0, 1], weights=[95, 5])[0]
                    dismissal_kind = ''
                    player_dismissed = ''
                    
                    if is_wicket == 1:
                        dismissal_kind = random.choice(['caught', 'bowled', 'lbw', 'run out', 'stumped'])
                        player_dismissed = batters[batter_idx]
                        batter_idx = (batter_idx + 1) % len(batters)
                        if batter_idx == non_striker_idx:
                            batter_idx = (batter_idx + 1) % len(batters)

                    deliveries_data.append({
                        'match_id': match_id,
                        'inning': inning,
                        'batting_team': batting_team,
                        'bowling_team': bowling_team,
                        'over': over,
                        'ball': ball,
                        'batter': batters[batter_idx],
                        'bowler': bowler,
                        'non_striker': batters[non_striker_idx],
                        'batsman_runs': batsman_runs,
                        'extra_runs': extra_runs,
                        'total_runs': total_runs,
                        'is_wicket': is_wicket,
                        'dismissal_kind': dismissal_kind,
                        'player_dismissed': player_dismissed
                    })
                    
                    if is_wicket == 1 and batter_idx >= len(batters):
                        break # all out
                if is_wicket == 1 and batter_idx >= len(batters):
                    break # all out
        
        match_id += 1

    df_matches = pd.DataFrame(matches_data)
    df_deliveries = pd.DataFrame(deliveries_data)
    
    df_matches.to_csv('matches.csv', index=False)
    df_deliveries.to_csv('deliveries.csv', index=False)
    print("Generated matches.csv and deliveries.csv successfully.")

if __name__ == "__main__":
    generate_sample_data(50)
