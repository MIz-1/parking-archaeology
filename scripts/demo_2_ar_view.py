import csv
import os
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime

# ── Load Data ──────────────────────────────────────────────
DATA_FILE = 'parking_data.csv'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def generate_demo_data():
    """Generate demo parking spots if no real data exists"""
    locations = [
        {"name": "DHA Mall",        "x": 2.1,  "y": 3.4, "spots": 45, "available": 12},
        {"name": "Dolmen City",     "x": 5.3,  "y": 7.1, "spots": 80, "available": 3},
        {"name": "Lucky One Mall",  "x": 8.2,  "y": 2.8, "spots": 60, "available": 28},
        {"name": "Packages Mall",   "x": 3.7,  "y": 8.5, "spots": 55, "available": 0},
        {"name": "Hyperstar",       "x": 6.8,  "y": 5.2, "spots": 40, "available": 15},
        {"name": "Ocean Mall",      "x": 1.5,  "y": 6.3, "spots": 35, "available": 8},
        {"name": "Centaurus",       "x": 9.1,  "y": 8.9, "spots": 70, "available": 22},
    ]
    return locations

# ── AR Map View ────────────────────────────────────────────
def show_ar_map():
    locations = generate_demo_data()
    rows      = load_data()

    fig, ax = plt.subplots(1, 1, figsize=(12, 9), facecolor='#0d1117')
    ax.set_facecolor('#0d1117')

    # Grid
    ax.grid(True, alpha=0.1, color='#30363d', linewidth=0.5)

    # Road lines
    for i in range(0, 11, 2):
        ax.axhline(y=i, color='#21262d', linewidth=1.5, alpha=0.5)
        ax.axvline(x=i, color='#21262d', linewidth=1.5, alpha=0.5)

    # Plot each location
    for loc in locations:
        x, y         = loc['x'], loc['y']
        available    = loc['available']
        total        = loc['spots']
        occupancy    = (total - available) / total

        # Color based on availability
        if available == 0:
            color  = '#f85149'   # Red — Full
            status = 'FULL'
        elif available <= 5:
            color  = '#d29922'   # Yellow — Almost full
            status = f'{available} left'
        else:
            color  = '#3fb950'   # Green — Available
            status = f'{available} spots'

        # Outer glow circle
        glow = plt.Circle((x, y), 0.45, color=color, alpha=0.15)
        ax.add_patch(glow)

        # Main circle
        circle = plt.Circle((x, y), 0.28, color=color, alpha=0.9)
        ax.add_patch(circle)

        # Parking icon
        ax.text(x, y, 'P', ha='center', va='center',
                fontsize=12, fontweight='bold', color='white')

        # Location name
        ax.text(x, y + 0.55, loc['name'], ha='center', va='bottom',
                fontsize=7.5, color='white', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#161b22',
                         edgecolor=color, alpha=0.85))

        # Status
        ax.text(x, y - 0.52, status, ha='center', va='top',
                fontsize=7, color=color, fontweight='bold')

        # Occupancy bar
        bar_width = 0.6
        ax.barh(y - 0.75, bar_width, height=0.08,
                left=x - bar_width/2, color='#30363d', alpha=0.8)
        ax.barh(y - 0.75, bar_width * occupancy, height=0.08,
                left=x - bar_width/2, color=color, alpha=0.9)

    # User location (YOU ARE HERE)
    ax.plot(5.5, 5.0, '*', markersize=20, color='#58a6ff', zorder=5)
    ax.text(5.5, 5.35, 'YOU', ha='center', va='bottom',
            fontsize=8, color='#58a6ff', fontweight='bold')

    # Legend
    green_patch  = mpatches.Patch(color='#3fb950', label='Available')
    yellow_patch = mpatches.Patch(color='#d29922', label='Almost Full (<=5)')
    red_patch    = mpatches.Patch(color='#f85149', label='Full')
    blue_patch   = mpatches.Patch(color='#58a6ff', label='Your Location')

    legend = ax.legend(handles=[green_patch, yellow_patch, red_patch, blue_patch],
                       loc='lower right', facecolor='#161b22',
                       edgecolor='#30363d', labelcolor='white', fontsize=8)

    # Stats bar at top
    total_spots     = sum(l['spots'] for l in locations)
    total_available = sum(l['available'] for l in locations)
    total_full      = sum(1 for l in locations if l['available'] == 0)

    ax.set_title(
        f'PARKING ARCHAEOLOGY — AR MAP VIEW\n'
        f'Total Spots: {total_spots}  |  Available: {total_available}  |  Full Locations: {total_full}  |  '
        f'{datetime.now().strftime("%H:%M:%S")}',
        color='white', fontsize=11, fontweight='bold', pad=15,
        bbox=dict(boxstyle='round', facecolor='#161b22', edgecolor='#30363d')
    )

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 11)
    ax.set_xticks([])
    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')

    plt.tight_layout()
    plt.savefig('ar_map.png', dpi=150, bbox_inches='tight',
                facecolor='#0d1117')
    plt.show()
    print("AR Map saved as ar_map.png")

# ── Radar View ─────────────────────────────────────────────
def show_radar():
    locations = generate_demo_data()

    fig, ax = plt.subplots(1, 1, figsize=(8, 8),
                           subplot_kw=dict(polar=True),
                           facecolor='#0d1117')
    ax.set_facecolor('#0d1117')

    names      = [l['name'] for l in locations]
    available  = [l['available'] for l in locations]
    N          = len(names)
    angles     = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    available += available[:1]
    angles    += angles[:1]

    ax.plot(angles, available, color='#3fb950', linewidth=2)
    ax.fill(angles, available, color='#3fb950', alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(names, color='white', fontsize=8)
    ax.tick_params(colors='white')
    ax.set_facecolor('#0d1117')
    ax.grid(color='#30363d', alpha=0.5)

    ax.set_title('AVAILABILITY RADAR', color='white',
                 fontsize=12, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig('ar_radar.png', dpi=150, facecolor='#0d1117')
    plt.show()
    print("Radar saved as ar_radar.png")

# ── Main ───────────────────────────────────────────────────
def main():
    print("\n" + "="*50)
    print("   PARKING ARCHAEOLOGY — AR VIEW")
    print("="*50)
    print("  1. Show AR Map")
    print("  2. Show Availability Radar")
    print("  3. Exit")
    print("="*50)

    choice = input("\nSelect option (1-3): ").strip()

    if   choice == '1': show_ar_map()
    elif choice == '2': show_radar()
    elif choice == '3': print("Goodbye!")
    else: print("Invalid option!")

if __name__ == "__main__":
    main()