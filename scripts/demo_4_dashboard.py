import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.ensemble import RandomForestClassifier
import csv
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ── Load/Generate Data ─────────────────────────────────────
DATA_FILE = 'parking_data.csv'

LOCATIONS = ['DHA Mall', 'Dolmen City', 'Lucky One', 'Packages Mall',
             'Hyperstar', 'Ocean Mall', 'Centaurus']

DEMO_SPOTS = [
    {"name": "DHA Mall",       "spots": 45, "available": 12},
    {"name": "Dolmen City",    "spots": 80, "available": 3},
    {"name": "Lucky One",      "spots": 60, "available": 28},
    {"name": "Packages Mall",  "spots": 55, "available": 0},
    {"name": "Hyperstar",      "spots": 40, "available": 15},
    {"name": "Ocean Mall",     "spots": 35, "available": 8},
    {"name": "Centaurus",      "spots": 70, "available": 22},
]

def load_logs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return list(csv.DictReader(f))

def generate_ml_data(n=1000):
    np.random.seed(42)
    data = []
    for _ in range(n):
        hour        = np.random.randint(6, 24)
        day         = np.random.randint(0, 7)
        loc_id      = np.random.randint(0, 7)
        month       = np.random.randint(1, 13)
        is_rush     = (9 <= hour <= 11) or (13 <= hour <= 15) or (17 <= hour <= 20)
        is_weekend  = day >= 5
        is_mall     = loc_id in [0, 1, 2]
        prob        = 0.6
        if is_rush:    prob -= 0.3
        if is_weekend: prob -= 0.2
        if is_mall:    prob -= 0.1
        if hour < 8:   prob += 0.3
        if hour > 21:  prob += 0.2
        prob = max(0.05, min(0.95, prob))
        available = 1 if np.random.random() < prob else 0
        data.append([hour, day, loc_id, month, available])
    df = pd.DataFrame(data, columns=['hour', 'day', 'loc_id', 'month', 'available'])
    return df

def train_ml(df):
    X = df[['hour', 'day', 'loc_id', 'month']]
    y = df['available']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

# ── Main Dashboard ─────────────────────────────────────────
def show_dashboard():
    print("Loading dashboard...")
    logs  = load_logs()
    df    = generate_ml_data()
    model = train_ml(df)
    now   = datetime.now()

    fig = plt.figure(figsize=(18, 11), facecolor='#0d1117')
    gs  = gridspec.GridSpec(3, 4, figure=fig, hspace=0.55, wspace=0.4)

    # ── Title Bar ──────────────────────────────────────────
    fig.suptitle(
        f'PARKING ARCHAEOLOGY — LIVE DASHBOARD    {now.strftime("%A, %d %B %Y  |  %H:%M:%S")}',
        color='white', fontsize=13, fontweight='bold', y=0.98,
        bbox=dict(boxstyle='round', facecolor='#161b22', edgecolor='#30363d')
    )

    # ── Panel 1: Availability Bar Chart ───────────────────
    ax1 = fig.add_subplot(gs[0, :2])
    ax1.set_facecolor('#111111')

    names     = [l['name'] for l in DEMO_SPOTS]
    available = [l['available'] for l in DEMO_SPOTS]
    occupied  = [l['spots'] - l['available'] for l in DEMO_SPOTS]
    colors    = ['#f85149' if a == 0 else '#d29922' if a <= 5 else '#3fb950'
                 for a in available]

    x = range(len(names))
    ax1.bar(x, occupied,  label='Occupied',  color='#f85149', alpha=0.7)
    ax1.bar(x, available, label='Available', color='#3fb950', alpha=0.9,
            bottom=occupied)

    ax1.set_xticks(x)
    ax1.set_xticklabels([n.split()[0] for n in names], color='white', fontsize=8)
    ax1.set_ylabel('Spots', color='white', fontsize=8)
    ax1.set_title('CURRENT AVAILABILITY', color='#4fc3f7',
                  fontsize=9, fontweight='bold')
    ax1.tick_params(colors='white')
    ax1.legend(facecolor='#222222', labelcolor='white', fontsize=7)
    ax1.set_facecolor('#111111')
    for spine in ax1.spines.values():
        spine.set_edgecolor('#30363d')

    # ── Panel 2: ML Heatmap (mini) ────────────────────────
    ax2 = fig.add_subplot(gs[0, 2:])
    ax2.set_facecolor('#111111')

    hours        = list(range(6, 24))
    heatmap_data = np.zeros((7, len(hours)))
    for i in range(7):
        for j, h in enumerate(hours):
            prob = model.predict_proba([[h, now.weekday(), i, now.month]])[0][1]
            heatmap_data[i, j] = prob

    im = ax2.imshow(heatmap_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    ax2.set_xticks(range(len(hours)))
    ax2.set_xticklabels([f'{h}' for h in hours], color='white', fontsize=6, rotation=45)
    ax2.set_yticks(range(7))
    ax2.set_yticklabels([n.split()[0] for n in LOCATIONS], color='white', fontsize=7)
    ax2.set_title('ML AVAILABILITY FORECAST (Today)', color='#ffa726',
                  fontsize=9, fontweight='bold')
    for spine in ax2.spines.values():
        spine.set_edgecolor('#30363d')

    # ── Panel 3: Stats Cards ──────────────────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor('#111111')
    ax3.axis('off')

    total_spots     = sum(l['spots'] for l in DEMO_SPOTS)
    total_available = sum(l['available'] for l in DEMO_SPOTS)
    total_full      = sum(1 for l in DEMO_SPOTS if l['available'] == 0)
    occupancy_rate  = (total_spots - total_available) / total_spots * 100

    stats = [
        ('TOTAL SPOTS',    str(total_spots),          '#4fc3f7'),
        ('AVAILABLE',      str(total_available),       '#3fb950'),
        ('FULL LOCATIONS', str(total_full),            '#f85149'),
        ('OCCUPANCY',      f'{occupancy_rate:.0f}%',   '#d29922'),
    ]

    for i, (label, value, color) in enumerate(stats):
        y_pos = 0.85 - i * 0.22
        ax3.text(0.5, y_pos, value, transform=ax3.transAxes,
                 ha='center', va='center', fontsize=22,
                 fontweight='bold', color=color)
        ax3.text(0.5, y_pos - 0.08, label, transform=ax3.transAxes,
                 ha='center', va='center', fontsize=7, color='#8b949e')

    ax3.set_title('LIVE STATS', color='#4fc3f7', fontsize=9, fontweight='bold')
    for spine in ax3.spines.values():
        spine.set_edgecolor('#30363d')

    # ── Panel 4: Hourly Prediction ────────────────────────
    ax4 = fig.add_subplot(gs[1, 1:3])
    ax4.set_facecolor('#111111')

    hour_probs = []
    for h in hours:
        probs = [model.predict_proba([[h, now.weekday(), i, now.month]])[0][1]
                 for i in range(7)]
        hour_probs.append(np.mean(probs))

    colors_line = ['#f85149' if p < 0.3 else '#d29922' if p < 0.6 else '#3fb950'
                   for p in hour_probs]

    for i in range(len(hours) - 1):
        ax4.fill_between([hours[i], hours[i+1]],
                         [hour_probs[i], hour_probs[i+1]],
                         alpha=0.3, color=colors_line[i])
        ax4.plot([hours[i], hours[i+1]],
                 [hour_probs[i], hour_probs[i+1]],
                 color=colors_line[i], linewidth=2)

    current_hour = now.hour
    if 6 <= current_hour <= 23:
        idx = current_hour - 6
        ax4.axvline(x=current_hour, color='#58a6ff', linestyle='--', alpha=0.8)
        ax4.text(current_hour, 0.95, 'NOW', color='#58a6ff',
                 fontsize=7, ha='center')

    ax4.set_xlim(6, 23)
    ax4.set_ylim(0, 1)
    ax4.set_xlabel('Hour', color='white', fontsize=8)
    ax4.set_ylabel('Avg Availability', color='white', fontsize=8)
    ax4.set_title('HOURLY AVAILABILITY FORECAST', color='#3fb950',
                  fontsize=9, fontweight='bold')
    ax4.tick_params(colors='white', labelsize=7)
    ax4.grid(True, alpha=0.2, color='#30363d')
    ax4.set_facecolor('#111111')
    for spine in ax4.spines.values():
        spine.set_edgecolor('#30363d')

    # ── Panel 5: Donut Chart ──────────────────────────────
    ax5 = fig.add_subplot(gs[1, 3])
    ax5.set_facecolor('#111111')

    occ  = total_spots - total_available
    avail = total_available
    wedges, texts, autotexts = ax5.pie(
        [occ, avail],
        labels=['Occupied', 'Available'],
        colors=['#f85149', '#3fb950'],
        autopct='%1.0f%%',
        startangle=90,
        wedgeprops=dict(width=0.5),
        textprops=dict(color='white', fontsize=8)
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(8)

    ax5.set_title('OCCUPANCY RATE', color='#ab47bc',
                  fontsize=9, fontweight='bold')

    # ── Panel 6: Log History ──────────────────────────────
    ax6 = fig.add_subplot(gs[2, :2])
    ax6.set_facecolor('#111111')
    ax6.axis('off')

    ax6.set_title('RECENT PARKING LOGS', color='#4fc3f7',
                  fontsize=9, fontweight='bold')

    if logs:
        headers = ['ID', 'Location', 'Spot', 'Date', 'Duration', 'Cost']
        col_x   = [0.02, 0.22, 0.42, 0.55, 0.72, 0.87]

        for j, (header, cx) in enumerate(zip(headers, col_x)):
            ax6.text(cx, 0.92, header, transform=ax6.transAxes,
                     fontsize=7, color='#8b949e', fontweight='bold')

        for i, row in enumerate(logs[-4:]):
            y = 0.75 - i * 0.18
            vals = [row['id'][-8:], row['location'], row['spot'],
                    row['date'], f"{row['duration_min']}m", f"PKR {row['cost']}"]
            for val, cx in zip(vals, col_x):
                ax6.text(cx, y, str(val), transform=ax6.transAxes,
                         fontsize=7, color='white')
    else:
        ax6.text(0.5, 0.5, 'No logs yet — run Demo 1 first!',
                 transform=ax6.transAxes, ha='center', color='#8b949e',
                 fontsize=9)

    for spine in ax6.spines.values():
        spine.set_edgecolor('#30363d')

    # ── Panel 7: Feature Importance ───────────────────────
    ax7 = fig.add_subplot(gs[2, 2:])
    ax7.set_facecolor('#111111')

    features    = ['Hour', 'Day', 'Location', 'Month']
    importances = model.feature_importances_
    colors_f    = ['#3fb950', '#58a6ff', '#d29922', '#f85149']

    bars = ax7.barh(features, importances, color=colors_f, alpha=0.9)
    for bar, imp in zip(bars, importances):
        ax7.text(imp + 0.003, bar.get_y() + bar.get_height()/2,
                 f'{imp:.1%}', va='center', color='white', fontsize=8)

    ax7.set_xlabel('Importance', color='white', fontsize=8)
    ax7.set_title('ML FEATURE IMPORTANCE', color='#d29922',
                  fontsize=9, fontweight='bold')
    ax7.tick_params(colors='white', labelsize=8)
    ax7.set_facecolor('#111111')
    for spine in ax7.spines.values():
        spine.set_edgecolor('#30363d')

    plt.savefig('dashboard.png', dpi=150, bbox_inches='tight', facecolor='#0d1117')
    plt.show()
    print("Dashboard saved as dashboard.png!")

if __name__ == "__main__":
    show_dashboard()