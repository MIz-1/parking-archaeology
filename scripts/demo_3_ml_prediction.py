import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

# ── Generate Training Data ─────────────────────────────────
def generate_training_data(n_samples=1000):
    """Generate realistic parking pattern data"""
    np.random.seed(42)

    data = []
    for _ in range(n_samples):
        hour        = np.random.randint(6, 24)
        day_of_week = np.random.randint(0, 7)   # 0=Monday, 6=Sunday
        location_id = np.random.randint(0, 7)
        month       = np.random.randint(1, 13)

        # Realistic availability logic
        # Rush hours: 9-11am, 1-3pm, 5-8pm
        is_rush_hour = (9 <= hour <= 11) or (13 <= hour <= 15) or (17 <= hour <= 20)
        is_weekend   = day_of_week >= 5
        is_mall_loc  = location_id in [0, 1, 2]   # Malls get more traffic

        # Base availability probability
        prob_available = 0.6

        if is_rush_hour:   prob_available -= 0.3
        if is_weekend:     prob_available -= 0.2
        if is_mall_loc:    prob_available -= 0.1
        if hour < 8:       prob_available += 0.3   # Early morning = more spots
        if hour > 21:      prob_available += 0.2   # Late night = more spots

        prob_available = max(0.05, min(0.95, prob_available))
        available      = 1 if np.random.random() < prob_available else 0

        data.append([hour, day_of_week, location_id, month, available])

    df = pd.DataFrame(data, columns=['hour', 'day_of_week', 'location_id', 'month', 'available'])
    return df

# ── Train Model ────────────────────────────────────────────
def train_model(df):
    X = df[['hour', 'day_of_week', 'location_id', 'month']]
    y = df['available']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred   = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n✅ Model trained successfully!")
    print(f"   Accuracy : {accuracy*100:.1f}%")
    print(f"   Samples  : {len(df)}")

    return model, accuracy

# ── Predict ────────────────────────────────────────────────
def predict_availability(model, hour, day, location_id, month=6):
    prediction = model.predict([[hour, day, location_id, month]])[0]
    probability = model.predict_proba([[hour, day, location_id, month]])[0]
    return prediction, probability

# ── Heatmap ────────────────────────────────────────────────
def show_heatmap(model):
    locations = ['DHA Mall', 'Dolmen City', 'Lucky One', 'Packages Mall',
                 'Hyperstar', 'Ocean Mall', 'Centaurus']
    hours     = list(range(6, 24))

    heatmap_data = np.zeros((len(locations), len(hours)))

    for i, loc_id in enumerate(range(len(locations))):
        for j, hour in enumerate(hours):
            _, prob = predict_availability(model, hour, 2, loc_id)  # Wednesday
            heatmap_data[i, j] = prob[1]  # Probability of being available

    fig, ax = plt.subplots(figsize=(14, 6), facecolor='#0d1117')
    ax.set_facecolor('#0d1117')

    im = ax.imshow(heatmap_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)

    ax.set_xticks(range(len(hours)))
    ax.set_xticklabels([f'{h}:00' for h in hours], rotation=45, color='white', fontsize=8)
    ax.set_yticks(range(len(locations)))
    ax.set_yticklabels(locations, color='white', fontsize=9)

    for i in range(len(locations)):
        for j in range(len(hours)):
            val  = heatmap_data[i, j]
            text = ax.text(j, i, f'{val:.0%}', ha='center', va='center',
                          fontsize=6.5, color='black' if val > 0.5 else 'white',
                          fontweight='bold')

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Availability Probability', color='white', fontsize=9)
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')

    ax.set_title('PARKING AVAILABILITY HEATMAP — Wednesday\n'
                 'Green = High Availability | Red = Low Availability',
                 color='white', fontsize=11, fontweight='bold', pad=15)

    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')

    plt.tight_layout()
    plt.savefig('ml_heatmap.png', dpi=150, bbox_inches='tight', facecolor='#0d1117')
    plt.show()
    print("Heatmap saved as ml_heatmap.png")

# ── Feature Importance ────────────────────────────────────
def show_feature_importance(model):
    features    = ['Hour', 'Day of Week', 'Location', 'Month']
    importances = model.feature_importances_

    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0d1117')
    ax.set_facecolor('#0d1117')

    colors = ['#3fb950', '#58a6ff', '#d29922', '#f85149']
    bars   = ax.barh(features, importances, color=colors, alpha=0.9)

    for bar, imp in zip(bars, importances):
        ax.text(imp + 0.005, bar.get_y() + bar.get_height()/2,
                f'{imp:.1%}', va='center', color='white', fontsize=10)

    ax.set_xlabel('Importance', color='white')
    ax.set_title('ML FEATURE IMPORTANCE\nWhat affects parking availability most?',
                 color='white', fontsize=11, fontweight='bold')
    ax.tick_params(colors='white')
    ax.set_xlim(0, max(importances) * 1.3)

    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')

    plt.tight_layout()
    plt.savefig('ml_features.png', dpi=150, facecolor='#0d1117')
    plt.show()
    print("Feature importance saved as ml_features.png")

# ── Interactive Prediction ────────────────────────────────
def interactive_predict(model):
    locations = ['DHA Mall', 'Dolmen City', 'Lucky One', 'Packages Mall',
                 'Hyperstar', 'Ocean Mall', 'Centaurus']
    days      = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                 'Friday', 'Saturday', 'Sunday']

    print("\n" + "="*50)
    print("   ML PARKING PREDICTOR")
    print("="*50)

    print("\nLocations:")
    for i, loc in enumerate(locations):
        print(f"  {i} — {loc}")

    loc_id = int(input("\nSelect location (0-6): "))
    hour   = int(input("Enter hour (6-23): "))
    day    = int(input("Day (0=Mon, 6=Sun): "))

    pred, prob = predict_availability(model, hour, day, loc_id)

    print(f"\n{'='*50}")
    print(f"  PREDICTION RESULT")
    print(f"{'='*50}")
    print(f"  Location    : {locations[loc_id]}")
    print(f"  Time        : {hour}:00 on {days[day]}")
    print(f"  Available   : {'✅ YES' if pred == 1 else '❌ NO'}")
    print(f"  Probability : {prob[1]*100:.1f}% available")
    print(f"  Confidence  : {max(prob)*100:.1f}%")

    if prob[1] >= 0.7:
        print(f"\n  Recommendation: GO NOW — High availability!")
    elif prob[1] >= 0.4:
        print(f"\n  Recommendation: MAYBE — Limited spots expected")
    else:
        print(f"\n  Recommendation: AVOID — Very low availability")

# ── Main ───────────────────────────────────────────────────
def main():
    print("\n" + "="*50)
    print("   PARKING ARCHAEOLOGY — ML PREDICTION")
    print("="*50)

    print("\nTraining ML model...")
    df    = generate_training_data(1000)
    model, accuracy = train_model(df)

    while True:
        print("\n" + "="*50)
        print("  1. Show Availability Heatmap")
        print("  2. Show Feature Importance")
        print("  3. Predict Availability")
        print("  4. Exit")
        print("="*50)

        choice = input("\nSelect option (1-4): ").strip()

        if   choice == '1': show_heatmap(model)
        elif choice == '2': show_feature_importance(model)
        elif choice == '3': interactive_predict(model)
        elif choice == '4':
            print("\nGoodbye!")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()