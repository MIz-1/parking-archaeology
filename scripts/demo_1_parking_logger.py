import csv
import os
from datetime import datetime

# ── Storage File ───────────────────────────────────────────
DATA_FILE = 'parking_data.csv'

# ── Initialize CSV ─────────────────────────────────────────
def init_storage():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'location', 'spot', 'date', 'time', 'duration_min', 'cost', 'notes'])
        print(f"Storage initialized: {DATA_FILE}")

# ── Log Parking ────────────────────────────────────────────
def log_parking():
    print("\n" + "="*50)
    print("   PARKING ARCHAEOLOGY — LOG PARKING")
    print("="*50)

    location  = input("\nLocation name (e.g. Mall, Office): ").strip()
    spot      = input("Spot number/name (e.g. A12, Basement-3): ").strip()
    duration  = input("Duration (minutes): ").strip()
    cost      = input("Cost (PKR/leave blank if free): ").strip() or "0"
    notes     = input("Notes (optional): ").strip()

    now       = datetime.now()
    date_str  = now.strftime("%Y-%m-%d")
    time_str  = now.strftime("%H:%M:%S")

    # Generate ID
    record_id = f"PKG-{now.strftime('%Y%m%d%H%M%S')}"

    with open(DATA_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([record_id, location, spot, date_str, time_str, duration, cost, notes])

    print("\n✅ Parking logged successfully!")
    print(f"   ID       : {record_id}")
    print(f"   Location : {location}")
    print(f"   Spot     : {spot}")
    print(f"   Date     : {date_str}")
    print(f"   Time     : {time_str}")
    print(f"   Duration : {duration} mins")
    print(f"   Cost     : PKR {cost}")

# ── View All Logs ──────────────────────────────────────────
def view_logs():
    print("\n" + "="*50)
    print("   PARKING ARCHAEOLOGY — VIEW LOGS")
    print("="*50)

    if not os.path.exists(DATA_FILE):
        print("No data found. Log some parking first!")
        return

    with open(DATA_FILE, 'r') as f:
        reader = csv.DictReader(f)
        rows   = list(reader)

    if not rows:
        print("No records yet!")
        return

    print(f"\nTotal records: {len(rows)}\n")
    print(f"{'ID':<20} {'Location':<15} {'Spot':<12} {'Date':<12} {'Duration':<10} {'Cost'}")
    print("-" * 80)

    for row in rows:
        print(f"{row['id']:<20} {row['location']:<15} {row['spot']:<12} {row['date']:<12} {row['duration_min']:<10} PKR {row['cost']}")

# ── Stats ──────────────────────────────────────────────────
def show_stats():
    print("\n" + "="*50)
    print("   PARKING ARCHAEOLOGY — STATS")
    print("="*50)

    if not os.path.exists(DATA_FILE):
        print("No data found!")
        return

    with open(DATA_FILE, 'r') as f:
        reader = csv.DictReader(f)
        rows   = list(reader)

    if not rows:
        print("No records yet!")
        return

    total_records  = len(rows)
    total_cost     = sum(float(r['cost']) for r in rows)
    total_duration = sum(float(r['duration_min']) for r in rows if r['duration_min'])

    locations = {}
    for row in rows:
        loc = row['location']
        locations[loc] = locations.get(loc, 0) + 1

    fav_location = max(locations, key=locations.get)

    print(f"\n  Total Parkings  : {total_records}")
    print(f"  Total Cost      : PKR {total_cost:.0f}")
    print(f"  Total Duration  : {total_duration:.0f} mins ({total_duration/60:.1f} hours)")
    print(f"  Avg Cost        : PKR {total_cost/total_records:.0f}")
    print(f"  Favourite Spot  : {fav_location} ({locations[fav_location]} times)")

# ── Main Menu ──────────────────────────────────────────────
def main():
    init_storage()

    while True:
        print("\n" + "="*50)
        print("   PARKING ARCHAEOLOGY")
        print("="*50)
        print("  1. Log New Parking")
        print("  2. View All Logs")
        print("  3. Show Stats")
        print("  4. Exit")
        print("="*50)

        choice = input("\nSelect option (1-4): ").strip()

        if   choice == '1': log_parking()
        elif choice == '2': view_logs()
        elif choice == '3': show_stats()
        elif choice == '4':
            print("\nGoodbye! Keep parking smartly. 🚗")
            break
        else:
            print("Invalid option. Try again!")

if __name__ == "__main__":
    main()