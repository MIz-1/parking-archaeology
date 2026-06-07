import app from './app';

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════╗
║   PARKING ARCHAEOLOGY API             ║
║   Server running on port ${PORT}          ║
║   Health: http://localhost:${PORT}/health ║
╚════════════════════════════════════════╝
  `);
});