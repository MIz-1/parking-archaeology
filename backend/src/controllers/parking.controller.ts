import { Request, Response } from 'express';
import {
  getAllParkingLogs,
  getParkingLog,
  createParkingLog,
  getParkingStats,
  deleteParkingLog,
} from '../services/parking.service';
import { getParkingPrediction } from '../services/ml.service';

// ── Get All Logs ───────────────────────────────────────────
export const getAllParkings = async (req: Request, res: Response) => {
  try {
    const logs = await getAllParkingLogs();
    res.json({
      success: true,
      count: logs.length,
      data: logs
    });
  } catch (error) {
    res.status(500).json({ success: false, error: 'Failed to fetch logs' });
  }
};

// ── Get Single Log ─────────────────────────────────────────
export const getParkingById = async (req: Request, res: Response) => {
  try {
    const id  = req.params.id as string;
    const log = await getParkingLog(id);
    if (!log) {
      return res.status(404).json({ success: false, error: 'Log not found' });
    }
    res.json({ success: true, data: log });
  } catch (error) {
    res.status(500).json({ success: false, error: 'Failed to fetch log' });
  }
};

// ── Create New Log ─────────────────────────────────────────
export const createParking = async (req: Request, res: Response) => {
  try {
    const { location, spot, duration_min, cost, notes } = req.body;

    if (!location || !spot) {
      return res.status(400).json({
        success: false,
        error: 'Location and spot are required'
      });
    }

    const newLog = await createParkingLog({
      location,
      spot,
      duration_min: duration_min || 0,
      cost:         cost || 0,
      notes:        notes || ''
    });

    res.status(201).json({ success: true, data: newLog });
  } catch (error) {
    res.status(500).json({ success: false, error: 'Failed to create log' });
  }
};

// ── Get Stats ──────────────────────────────────────────────
export const getStats = async (req: Request, res: Response) => {
  try {
    const stats = await getParkingStats();
    res.json({ success: true, data: stats });
  } catch (error) {
    res.status(500).json({ success: false, error: 'Failed to fetch stats' });
  }
};

// ── ML Prediction ──────────────────────────────────────────
export const getPrediction = async (req: Request, res: Response) => {
  try {
    const hour        = Number(req.query.hour);
    const day         = Number(req.query.day);
    const location_id = Number(req.query.location_id);

    if (isNaN(hour) || isNaN(day) || isNaN(location_id)) {
      return res.status(400).json({
        success: false,
        error: 'hour, day, and location_id are required'
      });
    }

    const prediction = await getParkingPrediction(hour, day, location_id);
    res.json({ success: true, data: prediction });
  } catch (error) {
    res.status(500).json({ success: false, error: 'Failed to get prediction' });
  }
};

// ── Delete Parking Log ─────────────────────────────────────
export const deleteParking = async (req: Request, res: Response) => {
  try {
    const id = req.params.id as string;
    const deleted = await deleteParkingLog(id);
    if (!deleted) {
      return res.status(404).json({ success: false, error: 'Log not found' });
    }
    res.json({ success: true, message: `Log ${id} deleted` });
  } catch (error) {
    res.status(500).json({ success: false, error: 'Failed to delete log' });
  }
};