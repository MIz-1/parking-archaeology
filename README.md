![Python](https://img.shields.io/badge/Python-3.14-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)
![React Native](https://img.shields.io/badge/React_Native-Expo-black)
![ML](https://img.shields.io/badge/ML-RandomForest-orange)
![Status](https://img.shields.io/badge/Status-Active-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

# Parking Archaeology

A full-stack smart parking system — real-time logging, ML-powered availability predictions, live statistics dashboard, and AR-style map visualization.

Built with React Native (Expo), TypeScript/Express backend, Python ML scripts, and CSV persistence.

---

## System Architecture

\`\`\`mermaid
graph TD
    A[React Native Frontend\nExpo SDK 56] --> B[Express TypeScript API\nPort 3000]
    B --> C[CSV Storage\nparking_data.csv]
    B --> D[ML Service\nRandomForest Logic]
    D --> E[Availability Predictions\n7 Locations]
    C --> F[Stats Engine\nAggregates]
    E --> A
    F --> A
    G[Python Scripts] --> C
\`\`\`

---

## Features

**Frontend — React Native / Expo**
- Home — live parking log list, auto-refresh on focus
- Log — form to add new parking sessions
- Stats — total cost, duration, sessions, favourite location
- ML — RandomForest predictions for 7 Karachi locations

**Backend — TypeScript / Express**
- GET /api/parking — all logs
- POST /api/parking — create log
- GET /api/parking/stats — aggregated statistics
- GET /api/parking/predict — ML availability prediction
- GET /health — health check

**Python Scripts**
- Demo 1 — Parking logger with CSV storage
- Demo 2 — AR-style map visualization
- Demo 3 — RandomForest ML model (68% accuracy)
- Demo 4 — Live dashboard

---

## ML Model

- Algorithm: Random Forest Classifier
- Training samples: 1000
- Accuracy: 68%
- Features: Hour of day (43%), Month (24%), Day of week (16%), Location (15%)
- Locations: DHA Mall, Dolmen City, Lucky One Mall, Packages Mall, Hyperstar, Ocean Mall, Centaurus

---

## Project Structure

\`\`\`
parking-archaeology/
├── frontend/                      — React Native / Expo app
│   └── src/
│       ├── app/                   — Expo Router screens
│       │   ├── index.tsx          — Home (log list)
│       │   ├── log.tsx            — Add parking form
│       │   ├── explore.tsx        — Stats dashboard
│       │   └── ar.tsx             — ML predictions
│       ├── services/
│       │   └── parking.api.ts     — API service layer
│       └── components/
│           └── web-nav.tsx        — Web navigation
├── backend/                       — Express TypeScript API
│   └── src/
│       ├── routes/
│       ├── controllers/
│       └── services/
├── scripts/                       — Python ML scripts
└── README.md
\`\`\`

---

## Setup and Run

**Backend**
\`\`\`bash
cd backend
npm install
npm run dev
\`\`\`

**Frontend**
\`\`\`bash
cd frontend
npm install
npx expo start
\`\`\`

**Python Scripts**
\`\`\`bash
cd scripts
python3 -m venv venv
source venv/bin/activate
pip install numpy pandas matplotlib scikit-learn plotly
python demo_1_parking_logger.py
\`\`\`

---

## Roadmap

- [x] Python scripts — Logger, AR Map, ML Model, Dashboard
- [x] Backend — Express TypeScript REST API
- [x] Frontend — React Native mobile app
- [x] ML predictions screen — live RandomForest forecasts
- [ ] Screenshots — app screen captures
- [ ] Deploy — Cloud hosting

---

## About

Self-taught developer exploring AI, smart city solutions, and full-stack development.
Built for learning and portfolio — not production.
