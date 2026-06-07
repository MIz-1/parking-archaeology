import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import parkingRoutes from './routes/parking.routes';

dotenv.config();

const app = express();

// ── Middleware ─────────────────────────────────────────────
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ── Routes ─────────────────────────────────────────────────
app.use('/api/parking', parkingRoutes);

// ── Health Check ───────────────────────────────────────────
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    message: 'Parking Archaeology API running',
    timestamp: new Date().toISOString()
  });
});

// ── 404 Handler ────────────────────────────────────────────
app.use((req, res) => {
  res.status(404).json({
    error: 'Route not found',
    path: req.path
  });
});

export default app;