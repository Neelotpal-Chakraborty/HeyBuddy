# Gemini proxy for beta1.html

Short explanation
- The browser UI in `beta1.html` will attempt to use local predefined responses. When a category has no predefined reply, the client will call a server-side endpoint `/api/gemini` to generate a response.
- This repository includes a small Node.js/Express proxy server (`server.js`) to forward the prompts to Google Generative / Gemini-like API.

Important security note
- Do NOT place your API key in client-side code — always use a server-side proxy like this to keep your key secret.

Quick start (Windows / PowerShell)
1. Install dependencies

```powershell
cd c:\Users\neelo\Downloads\code
npm install
```

2. Set your API key and run the server

```powershell
$env:GEMINI_API_KEY = 'YOUR_GOOGLE_API_KEY_OR_GEMINI_KEY'
npm start
```

3. Open `beta1.html` in the browser and the client will POST to http://localhost:3000/api/gemini when needed.

Note about file:// and CORS
- If you open `beta1.html` directly (double-click -> file://...), the browser treats the page as coming from the file protocol. A fetch to a relative path like `/api/gemini` will resolve to `file:///api/gemini` and fail — you'll see errors like "Fetch at 'file:///C:/api/gemini' blocked". To avoid this, serve the page over HTTP.

Serving the static page locally (recommended)
You can quickly serve the directory over HTTP so the client can talk to the proxy:

Option A — Node http-server (fast)
```powershell
npm install -g http-server
cd c:\Users\neelo\Downloads\code
http-server -p 8080
# then open http://localhost:8080/beta1.html
```

Option B — npx (no global install) ( Preferred)
```powershell
cd c:\Users\neelo\Downloads\code
npx http-server -p 8080
```

If you prefer to still open the page directly via file://, the client attempts to default to `http://localhost:3000/api/gemini` when it detects file:// so make sure your proxy is running on port 3000. For production or remote hosting, set your proxy host and allow CORS from your app's origin.

How the server works
- The server forwards the POST body { prompt: '...' } to the Google Generative Text API using the text-bison-001 model. The server returns { reply: '...' }.
- The code uses the v1beta2 endpoint `models/text-bison-001:generateText` in `server.js`. If you prefer a different model or the chat endpoint, change the server.

Troubleshooting 404 "Requested entity was not found."
- If you get a 404 error like: { code: 404, message: 'Requested entity was not found.' }
  - Check that the Generative Language API is enabled in the Google Cloud project that issued the API key.
  - Verify the API key is valid and belongs to the project that has the Generative API enabled.
  - Ensure billing is enabled on the project (some APIs require billing).
  - Models and endpoints vary by account (region / access). Try overriding `MODEL_NAME` via environment variable if your account uses a different model id.
    Example: MODEL_NAME=chat-bison-001 or MODEL_NAME=text-bison@001 (depending on your account/version).
  - You can also override `API_BASE` (for example if your API needs a different root) by setting the environment variable API_BASE.

Server debug / improved response
- The server now returns a debug payload when the model response doesn't contain a simple text string — this helps you inspect the model's actual shape. If the API returned a non-2xx error, the server forwards the API details so you can see the exact message (helpful when diagnosing 404s).

Example test (local)
- POST a quick test via curl/powershell after starting the server:

```powershell
curl -Method POST http://localhost:3000/api/gemini -ContentType "application/json" -Body '{"prompt":"Hello world"}'
```

Production notes
- This simple example is intended for local development. For production:
  - Add authentication to the proxy endpoint and rate-limiting
  - Use HTTPS
  - Validate and sanitize inputs
  - Monitor usage and handle model-specific response shapes

If you'd like, I can also update `beta1.html` to call a different server endpoint or wire in a particular model or provider you prefer. 
