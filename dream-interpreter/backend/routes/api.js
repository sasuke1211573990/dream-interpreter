const express = require('express');
const router = express.Router();
const axios = require('axios');

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:5000';

// Function to call the Python AI Service
const interpretDream = async (text) => {
    try {
        // Attempt to call the AI service
        console.log(`Calling AI service at ${AI_SERVICE_URL}/interpret`);
        const response = await axios.post(`${AI_SERVICE_URL}/interpret`, { text });
        return response.data.interpretation;
    } catch (error) {
        console.error('AI Service Error:', error.message);
        if (error.response) {
            console.error('AI Service Response:', error.response.data);
        }
        
        // Fallback mock if AI service is down or unreachable (e.g. during dev without docker)
        return `[Fallback Mode] The AI service is currently unavailable. \n\nHere is a simulated interpretation for: "${text}". \n\nYour dream suggests a strong desire for connectivity and integration, mirroring the system's attempt to connect to its AI core.`;
    }
};

router.post('/interpret', async (req, res) => {
  try {
    const { dreamText } = req.body;
    if (!dreamText) {
        return res.status(400).json({ error: 'dreamText is required' });
    }
    
    const interpretation = await interpretDream(dreamText);
    res.json({ success: true, interpretation });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
