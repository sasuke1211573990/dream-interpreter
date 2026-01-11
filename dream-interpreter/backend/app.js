const express = require('express');
const cors = require('cors');
const apiRoutes = require('./routes/api');
const logger = require('./utils/logger');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Request logging middleware
app.use((req, res, next) => {
  logger.info(`${req.method} ${req.url}`);
  next();
});

app.use('/api', apiRoutes);

app.get('/', (req, res) => {
  res.send('Dream Interpreter API is running');
});

app.listen(PORT, () => {
  logger.info(`Server is running on port ${PORT}`);
  console.log(`Server is running on port ${PORT}`);
});
