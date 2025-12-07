// server.js

const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());

// Environment variables: GEMINI_API_KEY, SYSTEM_PROMPT
const API_KEY = process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY;
const MODEL_NAME = process.env.MODEL_NAME || 'gemini-2.0-flash';

// Default system context prompt for HeyBuddy (mental health companion)
// This prompt is prepended to user messages to guide the model's behavior and tone.
// Override by setting the SYSTEM_PROMPT environment variable.
const DEFAULT_SYSTEM_PROMPT = `You are HeyBuddy, a compassionate and supportive mental health companion. Your role is to:
- Listen actively and with empathy to the user's concerns and feelings.
- Provide thoughtful, non-judgmental responses that validate their emotions.
- Offer practical coping strategies, grounding techniques, and suggestions for self-care.
- Encourage professional help when appropriate (e.g., for crisis situations, therapy, counseling).
- Maintain a warm, conversational tone while being mindful of mental health boundaries.
- IMPORTANT: If the user mentions suicidal thoughts, self-harm, or immediate danger, always encourage them to contact emergency services or the helpline: 14416.
- Never pretend to be a licensed therapist or provide medical advice.
- Be supportive, but honest about your limitations as an AI.`;

const SYSTEM_PROMPT = process.env.SYSTEM_PROMPT || DEFAULT_SYSTEM_PROMPT;

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

        // Prepend system context to the user prompt so the model maintains HeyBuddy's persona and behavior.
        const fullPrompt = `${SYSTEM_PROMPT}\n\nUser: ${prompt}`;

        const payload = {
            contents: [
                {
                    parts: [{ text: fullPrompt }]
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
