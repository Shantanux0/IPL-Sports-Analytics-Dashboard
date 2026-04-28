import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

def train_win_predictor():
    print("🤖 Initializing Machine Learning Win Predictor...")
    
    try:
        matches = pd.read_csv('matches.csv')
    except FileNotFoundError:
        print("❌ Error: matches.csv not found.")
        return

    # Filter out matches with no result
    matches = matches[matches['result'] != 'no result']
    matches = matches.dropna(subset=['winner'])

    # Feature Engineering for the Model
    # Features: Venue, Team1, Team2, Toss Winner, Toss Decision
    # Target: Winner
    
    # We will encode categorical text features into numerical values for the ML model
    print("⚙️ Encoding features for the ML model...")
    encoder = LabelEncoder()
    
    # Create a unified mapping for all teams so team encodings remain consistent
    all_teams = pd.concat([matches['team1'], matches['team2']]).unique()
    encoder.fit(all_teams)
    
    matches['team1_encoded'] = encoder.transform(matches['team1'])
    matches['team2_encoded'] = encoder.transform(matches['team2'])
    matches['toss_winner_encoded'] = encoder.transform(matches['toss_winner'])
    matches['winner_encoded'] = encoder.transform(matches['winner'])
    
    # Encode Toss Decision (0 for bat, 1 for field)
    toss_decision_encoder = LabelEncoder()
    matches['toss_decision_encoded'] = toss_decision_encoder.fit_transform(matches['toss_decision'])
    
    # Select our Features (X) and Target (y)
    X = matches[['team1_encoded', 'team2_encoded', 'toss_winner_encoded', 'toss_decision_encoded']]
    y = matches['winner_encoded']
    
    # Split the data into Training and Testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the Logistic Regression Model
    print("🏋️ Training Logistic Regression Model...")
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    
    # Test the model's accuracy
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    print(f"✅ Model Training Complete!")
    print(f"🎯 Model Accuracy Score: {accuracy * 100:.2f}%")
    print("💡 Note: Accuracy is low because T20 cricket is highly unpredictable and we are using a simplified dataset. Real models use ball-by-ball run rates!")
    
    return model

if __name__ == "__main__":
    train_win_predictor()
