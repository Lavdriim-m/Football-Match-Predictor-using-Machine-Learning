from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

app = Flask(__name__)

# Load dataset
file_path = "full_data.csv"
df = pd.read_csv(file_path)

# Drop missing scores
df = df.dropna(subset=['H_Score', 'A_Score'])

# Encode categorical features
le_league = LabelEncoder()
df['League_Label'] = le_league.fit_transform(df['League'])

le_team = LabelEncoder()
df['Home_Label'] = le_team.fit_transform(df['Home'])
df['Away_Label'] = le_team.transform(df['Away'])

# Selecting features and target variables
features = ['League_Label', 'Home_Label', 'Away_Label']
target_stats = ['H_Score', 'A_Score', 'H_Ball_Possession', 'A_Ball_Possession',
                'H_Goal_Attempts', 'A_Goal_Attempts', 'H_Shots_on_Goal', 'A_Shots_on_Goal',
                'H_Corner_Kicks', 'A_Corner_Kicks', 'H_Free_Kicks', 'A_Free_Kicks',
                'H_Offsides', 'A_Offsides', 'H_Yellow_Cards', 'A_Yellow_Cards']

# Convert percentage strings to numeric values
for col in ['H_Ball_Possession', 'A_Ball_Possession']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace('%', '').astype(float)

# Fill missing values
df[target_stats] = df[target_stats].fillna(df[target_stats].median())

# Train models for each target variable
target_models = {}
accuracy_scores = {}

for target in target_stats:
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    target_models[target] = model

    # Compute accuracy
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    accuracy = 100 - (mae / y_test.mean()) * 100
    accuracy_scores[target] = round(accuracy, 2)

# Generate reasoning based on predictions
def generate_reason(home_team, away_team, predictions):
    important_stats = ['H_Ball_Possession', 'H_Goal_Attempts', 'H_Shots_on_Goal', 'H_Corner_Kicks']
    reasons = []

    for stat in important_stats:
        away_stat = stat.replace('H_', 'A_')
        if predictions[stat] > predictions[away_stat]:
            reasons.append(f"{home_team} had better {stat.replace('H_', '').replace('_', ' ').lower()}.")
        elif predictions[stat] < predictions[away_stat]:
            reasons.append(f"{away_team} had better {stat.replace('H_', '').replace('_', ' ').lower()}.")

    return " ".join(reasons) if reasons else "No clear advantage detected."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/leagues', methods=['GET'])
def get_leagues():
    """Return all unique leagues."""
    leagues = sorted(df['League'].unique().tolist())
    return jsonify(leagues)

@app.route('/teams/<league>', methods=['GET'])
def get_teams(league):
    """Return teams from a given league."""
    teams = sorted(df[df['League'] == league]['Home'].unique().tolist())
    return jsonify(teams)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    home_league = data['home_league']
    away_league = data['away_league']
    home = data['home']
    away = data['away']

    if home == away:
        return jsonify({'error': "Teams cannot be the same!"}), 400

    league_code = le_league.transform([home_league])[0]
    home_code = le_team.transform([home])[0]
    away_code = le_team.transform([away])[0]

    input_data = pd.DataFrame([[league_code, home_code, away_code]], columns=features)
    predictions = {stat: target_models[stat].predict(input_data)[0] for stat in target_stats}
    reason = generate_reason(home, away, predictions)

    response = {
        "result": f"{home} {int(predictions['H_Score'])} - {int(predictions['A_Score'])} {away}",
        "stats": {
            "Ball Possession": f"{predictions['H_Ball_Possession']:.0f}% - {predictions['A_Ball_Possession']:.0f}%",
            "Goal Attempts": f"{predictions['H_Goal_Attempts']:.0f} - {predictions['A_Goal_Attempts']:.0f}",
            "Shots on Goal": f"{predictions['H_Shots_on_Goal']:.0f} - {predictions['A_Shots_on_Goal']:.0f}",
            "Corner Kicks": f"{predictions['H_Corner_Kicks']:.0f} - {predictions['A_Corner_Kicks']:.0f}",
            "Free Kicks": f"{predictions['H_Free_Kicks']:.0f} - {predictions['A_Free_Kicks']:.0f}",
            "Offsides": f"{predictions['H_Offsides']:.0f} - {predictions['A_Offsides']:.0f}",
            "Yellow Cards": f"{predictions['H_Yellow_Cards']:.0f} - {predictions['A_Yellow_Cards']:.0f}"
        },
        "accuracy": f"{accuracy_scores['H_Score']}% (Score prediction)",
        "reason": reason
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
