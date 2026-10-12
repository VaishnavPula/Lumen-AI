# Lumen – AI Chatbot Web App

A modern AI chatbot built with **Flask**, the **Gemini API** and **SQLite**.
Users can register, log in, chat with the AI, and come back to their saved conversations later.

## Features
- Homepage with hero section, feature cards and footer
- Register, login and logout (passwords are hashed with Werkzeug)
- Chat page with sidebar, chat history, and a "+ New chat" button
- Typing animation while Gemini is answering
- Messages saved in SQLite, grouped by day in the sidebar
- Auto chat titles, delete chat, copy reply, character counter
- Enter to send, Shift + Enter for a new line
- Light and dark theme (remembered in your browser)
- Responsive layout for desktop, tablet and mobile
- Friendly error messages (no raw Python errors)

## Technologies
| Part | Technology |
|------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| AI | Gemini API (`google-genai`) |
| Database | SQLite |

## Folder structure
```text
AI-Chatbot/
├── app.py                 # starts the app, connects everything
├── config.py              # settings (reads the .env file)
├── requirements.txt
├── .env.example           # copy to .env and add your key
├── database/db.py         # SQLite tables and connection
├── routes/
│   ├── auth.py            # register, login, logout
│   ├── chat.py            # chat page + /api/chat (sends to Gemini)
│   └── history.py         # list, open, create, delete conversations
├── services/gemini_service.py   # all Gemini API code
├── templates/             # HTML pages
├── static/css/            # style.css, auth.css, chat.css
├── static/js/             # main.js (theme), auth.js, chat.js
└── instance/chatbot.db    # created automatically on first run
```

## How to run it

1. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```
   Activate it:
   - Windows: `venv\Scripts\activate`
   - macOS / Linux: `source venv/bin/activate`

2. **Install the packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your Gemini API key**
   - Get a free key at https://aistudio.google.com/apikey
   - Copy `.env.example` to `.env`
   - Open `.env` and replace `your_api_key_here` with your key
   - Never share `.env` or upload it to GitHub (it is already in `.gitignore`)

4. **Create the database**
   Nothing to do. The app creates `instance/chatbot.db` and all tables the first time it starts.

5. **Start the server**
   ```bash
   python app.py
   ```

6. **Open the app** at http://127.0.0.1:5000

## Basic usage
1. Click **Register**, create an account, and you land on the chat page.
2. Click a suggestion or type a message and press **Enter**.
3. Use **+ New chat** for a fresh conversation, or click an old chat in the sidebar to continue it.
4. Use the bin icon to delete a chat, and the moon/sun icon to switch theme.

## Which file does what (handy for your viva)
| Job | File |
|-----|------|
| Frontend pages | `templates/*.html`, `static/css/*.css` |
| Frontend logic (fetch, animation, history) | `static/js/chat.js` |
| Flask backend | `app.py`, `routes/*.py` |
| Gemini API | `services/gemini_service.py` |
| Database | `database/db.py` |

## How a message travels
```text
Browser (chat.js) → POST /api/chat → Flask (routes/chat.py)
  → Gemini (services/gemini_service.py) → Flask saves both messages in SQLite
  → JSON reply → Browser shows the answer
```

## Troubleshooting
- **"The AI is not set up yet"** – you haven't added `GEMINI_API_KEY` to `.env`, or didn't restart the server.
- **"API key looks invalid"** – re-copy the key from Google AI Studio.
- **"AI is busy"** – you hit the free-tier rate limit; wait a minute.
- If a model name stops working, change `GEMINI_MODEL` in `.env`.
