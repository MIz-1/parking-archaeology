import { Router } from 'express';
import {
  getAllParkings,
  getParkingById,
  createParking,
  deleteParking,
  getStats,
  getPrediction
} from '../controllers/parking.controller';

const router = Router();

router.get('/',        getAllParkings);
router.get('/stats',   getStats);
router.get('/predict', getPrediction);
router.post('/',       createParking);
router.delete('/:id',  deleteParking);
router.get('/:id',     getParkingById);

export default router;
