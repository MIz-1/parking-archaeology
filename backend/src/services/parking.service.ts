import db from './database';

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

export const getAllParkingLogs = async (): Promise<ParkingLog[]> => {
  const rows = db.prepare('SELECT * FROM parking_logs ORDER BY date DESC, time DESC').all();
  return rows as ParkingLog[];
};

export const getParkingLog = async (id: string): Promise<ParkingLog | null> => {
  const row = db.prepare('SELECT * FROM parking_logs WHERE id = ?').get(id);
  return (row as ParkingLog) || null;
};

export const createParkingLog = async (data: Omit<ParkingLog, 'id' | 'date' | 'time'>): Promise<ParkingLog> => {
  const now  = new Date();
  const id   = `PKG-${now.getFullYear()}${String(now.getMonth()+1).padStart(2,'0')}${String(now.getDate()).padStart(2,'0')}${String(now.getHours()).padStart(2,'0')}${String(now.getMinutes()).padStart(2,'0')}${String(now.getSeconds()).padStart(2,'0')}`;
  const date = now.toISOString().split('T')[0];
  const time = now.toTimeString().split(' ')[0];

  db.prepare(`
    INSERT INTO parking_logs (id, location, spot, date, time, duration_min, cost, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `).run(id, data.location, data.spot, date, time, data.duration_min, data.cost, data.notes || '');

  return { id, date, time, ...data };
};

export const getParkingStats = async () => {
  const logs = await getAllParkingLogs();

  if (logs.length === 0) {
    return { total_logs: 0, total_cost: 0, total_duration: 0, avg_cost: 0, favourite_location: null, locations: {} };
  }

  const total_cost     = logs.reduce((sum, l) => sum + l.cost, 0);
  const total_duration = logs.reduce((sum, l) => sum + l.duration_min, 0);

  const locationCount: Record<string, number> = {};
  logs.forEach(l => { locationCount[l.location] = (locationCount[l.location] || 0) + 1; });
  const favourite_location = Object.entries(locationCount).sort((a, b) => b[1] - a[1])[0][0];

  return {
    total_logs: logs.length,
    total_cost,
    total_duration,
    avg_cost: total_cost / logs.length,
    favourite_location,
    locations: locationCount
  };
};

export const deleteParkingLog = async (id: string): Promise<boolean> => {
  const result = db.prepare('DELETE FROM parking_logs WHERE id = ?').run(id);
  return result.changes > 0;
};
