// ── ML Service ─────────────────────────────────────────────
// Simulates ML predictions from our Python RandomForest model

// ── Types ──────────────────────────────────────────────────
interface PredictionResult {
  location_id:   number;
  location_name: string;
  hour:          number;
  day:           number;
  day_name:      string;
  available:     boolean;
  probability:   number;
  recommendation: string;
}

// ── Location Names ─────────────────────────────────────────
const LOCATIONS = [
  'DHA Mall',
  'Dolmen City',
  'Lucky One Mall',
  'Packages Mall',
  'Hyperstar',
  'Ocean Mall',
  'Centaurus'
];

const DAYS = [
  'Monday', 'Tuesday', 'Wednesday', 'Thursday',
  'Friday', 'Saturday', 'Sunday'
];

// ── Prediction Logic (mirrors Python ML model) ─────────────
const calculateProbability = (hour: number, day: number, location_id: number): number => {
  let prob = 0.6;

  // Rush hours
  const isRushHour = (hour >= 9 && hour <= 11) ||
                     (hour >= 13 && hour <= 15) ||
                     (hour >= 17 && hour <= 20);

  const isWeekend = day >= 5;
  const isMall    = [0, 1, 2].includes(location_id);

  if (isRushHour) prob -= 0.3;
  if (isWeekend)  prob -= 0.2;
  if (isMall)     prob -= 0.1;
  if (hour < 8)   prob += 0.3;
  if (hour > 21)  prob += 0.2;

  return Math.max(0.05, Math.min(0.95, prob));
};

// ── Get Recommendation ─────────────────────────────────────
const getRecommendation = (probability: number): string => {
  if (probability >= 0.7) return 'GO NOW — High availability expected!';
  if (probability >= 0.4) return 'MAYBE — Limited spots expected';
  return 'AVOID — Very low availability expected';
};

// ── Main Prediction Function ───────────────────────────────
export const getParkingPrediction = async (
  hour: number,
  day: number,
  location_id: number
): Promise<PredictionResult> => {

  const probability    = calculateProbability(hour, day, location_id);
  const available      = probability >= 0.5;
  const location_name  = LOCATIONS[location_id] || 'Unknown';
  const day_name       = DAYS[day] || 'Unknown';
  const recommendation = getRecommendation(probability);

  return {
    location_id,
    location_name,
    hour,
    day,
    day_name,
    available,
    probability:     Math.round(probability * 100) / 100,
    recommendation
  };
};

// ── Bulk Prediction (all locations for a time) ─────────────
export const getAllLocationsPrediction = async (hour: number, day: number) => {
  const predictions = LOCATIONS.map((name, id) => {
    const probability   = calculateProbability(hour, day, id);
    const available     = probability >= 0.5;
    const recommendation = getRecommendation(probability);

    return {
      location_id:   id,
      location_name: name,
      available,
      probability:   Math.round(probability * 100) / 100,
      recommendation
    };
  });

  return predictions.sort((a, b) => b.probability - a.probability);
};