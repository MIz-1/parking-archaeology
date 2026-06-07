import fs from 'fs';
import path from 'path';
import { parse } from 'csv-parse/sync';
import { stringify } from 'csv-stringify/sync';

// ── Types ──────────────────────────────────────────────────
export interface ParkingLog {
  id: string;
  location: string;
  spot: string;
  date: string;
  time: string;
  duration_min: number;
  cost: number;
  notes: string;
}

// ── CSV File Path ──────────────────────────────────────────
const DATA_FILE = path.join(__dirname, '../../..', 'scripts', 'parking_data.csv');

// ── Read All Logs ──────────────────────────────────────────
export const getAllParkingLogs = async (): Promise<ParkingLog[]> => {
  if (!fs.existsSync(DATA_FILE)) return [];

  const content = fs.readFileSync(DATA_FILE, 'utf-8');
  const records = parse(content, {
    columns: true,
    skip_empty_lines: true
  });

  return records.map((r: any) => ({
    id:           r.id,
    location:     r.location,
    spot:         r.spot,
    date:         r.date,
    time:         r.time,
    duration_min: Number(r.duration_min),
    cost:         Number(r.cost),
    notes:        r.notes
  }));
};

// ── Get Single Log ─────────────────────────────────────────
export const getParkingLog = async (id: string): Promise<ParkingLog | null> => {
  const logs = await getAllParkingLogs();
  return logs.find(log => log.id === id) || null;
};

// ── Create New Log ─────────────────────────────────────────
export const createParkingLog = async (data: Omit<ParkingLog, 'id' | 'date' | 'time'>): Promise<ParkingLog> => {
  const now    = new Date();
  const id     = `PKG-${now.getFullYear()}${String(now.getMonth()+1).padStart(2,'0')}${String(now.getDate()).padStart(2,'0')}${String(now.getHours()).padStart(2,'0')}${String(now.getMinutes()).padStart(2,'0')}${String(now.getSeconds()).padStart(2,'0')}`;
  const date   = now.toISOString().split('T')[0];
  const time   = now.toTimeString().split(' ')[0];

  const newLog: ParkingLog = { id, date, time, ...data };

  // Read existing logs
  const logs = await getAllParkingLogs();
  logs.push(newLog);

  // Write back to CSV
  const headers = ['id', 'location', 'spot', 'date', 'time', 'duration_min', 'cost', 'notes'];
  const csv = stringify(logs, { header: true, columns: headers });
  fs.writeFileSync(DATA_FILE, csv);

  return newLog;
};

// ── Get Stats ──────────────────────────────────────────────
export const getParkingStats = async () => {
  const logs = await getAllParkingLogs();

  if (logs.length === 0) {
    return {
      total_logs:       0,
      total_cost:       0,
      total_duration:   0,
      avg_cost:         0,
      favourite_location: null
    };
  }

  const total_cost     = logs.reduce((sum, l) => sum + l.cost, 0);
  const total_duration = logs.reduce((sum, l) => sum + l.duration_min, 0);

  const locationCount: Record<string, number> = {};
  logs.forEach(l => {
    locationCount[l.location] = (locationCount[l.location] || 0) + 1;
  });

  const favourite_location = Object.entries(locationCount)
    .sort((a, b) => b[1] - a[1])[0][0];

  return {
    total_logs:          logs.length,
    total_cost:          total_cost,
    total_duration:      total_duration,
    avg_cost:            total_cost / logs.length,
    favourite_location:  favourite_location,
    locations:           locationCount
  };
};