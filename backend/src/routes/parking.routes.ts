import { Router } from 'express';
import {
  getAllParkings,
  getParkingById,
  createParking,
  getStats,
  getPrediction
} from '../controllers/parking.controller';

const router = Router();

// ── CRUD Routes ────────────────────────────────────────────
router.get('/',           getAllParkings);   // Get all logs
router.get('/stats',      getStats);         // Get statistics
router.get('/predict',    getPrediction);    // ML prediction
router.get('/:id',        getParkingById);   // Get single log
router.post('/',          createParking);    // Create new log

export default router;