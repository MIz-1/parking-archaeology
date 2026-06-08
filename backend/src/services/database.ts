import Database from 'better-sqlite3';
import path from 'path';

const DB_PATH = path.join(__dirname, '../../..', 'parking.db');

const db = new Database(DB_PATH);

// ── Create Table ───────────────────────────────────────────
db.exec(`
  CREATE TABLE IF NOT EXISTS parking_logs (
    id           TEXT PRIMARY KEY,
    location     TEXT NOT NULL,
    spot         TEXT NOT NULL,
    date         TEXT NOT NULL,
    time         TEXT NOT NULL,
    duration_min INTEGER NOT NULL,
    cost         REAL NOT NULL,
    notes        TEXT DEFAULT ''
  )
`);

export default db;
