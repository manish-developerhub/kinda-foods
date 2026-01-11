# Running the Kinda Foods site + AI chatbot

This document explains how to run the frontend and backend (with optional OpenAI integration) locally.

Prerequisites
- Node.js (14+)
- Python 3 (optional, only for `chatbot.py` console tool)

1) Start the backend (serves frontend + API)

```powershell
cd "c:\kinda foods\backend"
npm install
npm start
```

The backend serves static files from the project root and exposes API endpoints on port 3001 (default).

2) Enable OpenAI (optional)

Set your OpenAI API key as an environment variable before starting the server, for example in PowerShell:

```powershell
$env:OPENAI_API_KEY = 'sk-...'
npm restart
```

Or add a `.env` file in the `backend` folder containing:

```
OPENAI_API_KEY=sk-...
```

3) Open the site

Open http://localhost:3001/index.html in your browser and click the chat button at the bottom-right.

4) Console chatbot (admin/debug)

Install Python deps and run the console chatbot:

```powershell
python -m pip install -r requirements.txt
python chatbot.py
```

Notes
- Do not commit your API keys to source control.
- This setup is intended for local development only.
