// server.js

const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());

// Environment variables: GEMINI_API_KEY
const API_KEY = process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY;
const MODEL_NAME = process.env.MODEL_NAME || 'gemini-2.0-flash';

if (!API_KEY) {
    console.warn('⚠️ WARNING: No Gemini API key set. Set GEMINI_API_KEY before using.');
}

// -------------------------
// Gemini Proxy Endpoint
// -------------------------
app.post('/api/gemini', async (req, res) => {
    try {
        if (!API_KEY) {
            return res.status(500).json({
                error: 'Server not configured: missing GEMINI_API_KEY'
            });
        }

        const { prompt } = req.body;

        if (!prompt || typeof prompt !== 'string') {
            return res.status(400).json({
                error: 'Missing prompt string in request body'
            });
        }

        // Correct Gemini 1.5 Endpoint
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL_NAME}:generateContent?key=${API_KEY}`;

        const payload = {
            contents: [
                {
                    parts: [{ text: prompt }]
                }
            ]
        };

        const aiRes = await axios.post(url, payload, {
            headers: { "Content-Type": "application/json" }
        });

        const data = aiRes.data;

        // Extract text reply
        const reply =
            data?.candidates?.[0]?.content?.parts?.[0]?.text ||
            '';

        if (!reply) {
            console.warn("⚠️ Unknown response from Gemini:", data);
            return res.json({ reply: "", debug: data });
        }

        return res.json({ reply });

    } catch (err) {
        console.error("❌ Gemini API error:", err?.response?.data || err.message);

        return res.status(err?.response?.status || 500).json({
            error: err?.response?.data || "Unknown Error"
        });
    }
});

// -------------------------
// Start server
// -------------------------
app.listen(port, () => {
    console.log(`🚀 Gemini Proxy running at http://localhost:${port}`);
});
