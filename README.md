# 🤖 Lumen – AI Chatbot Web App

Lumen is an AI-powered chatbot web application developed using Python, Flask, Google Gemini API, and SQLite.

The application allows users to register, log in, interact with AI, and manage their conversation history through a modern and responsive web interface.

## 🚀 Run

1. Open this folder in VS Code.

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

4. Install the required packages:

```bash
pip install -r requirements.txt
```

5. Configure the Gemini API key:

- Get an API key from Google AI Studio.
- Copy `.env.example` and rename the copy to `.env`.
- Add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

6. Run the Flask application:

```bash
python app.py
```

7. Open your browser and visit:

```text
http://127.0.0.1:5000/
```

## ✨ Features

- Modern and interactive homepage
- User registration and login
- Secure password hashing using Werkzeug
- AI-powered chatbot using Google Gemini API
- Real-time AI responses
- Typing animation
- Multiple chat conversations
- Automatic conversation titles
- Chat history stored in SQLite
- Create and delete conversations
- Copy AI-generated responses
- Character counter
- Enter to send messages
- Shift + Enter for a new line
- Light and dark mode
- Responsive HTML, CSS, and JavaScript interface
- User-friendly error handling

## 🛠️ Technologies Used

- Python
- Flask
- Google Gemini API
- Google GenAI SDK
- SQLite
- HTML
- CSS
- JavaScript

## 📁 Project Structure

```text
Lumen-AI-Chatbot/
│
├── app.py
├── config.py
├── requirements.txt
├── .env.example
│
├── database/
│   └── db.py
│
├── routes/
│   ├── auth.py
│   ├── chat.py
│   └── history.py
│
├── services/
│   └── gemini_service.py
│
├── templates/
│   └── HTML files
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── auth.css
│   │   └── chat.css
│   │
│   └── js/
│       ├── main.js
│       ├── auth.js
│       └── chat.js
│
├── instance/
│   └── chatbot.db
│
├── .gitignore
└── README.md
```

Note: The SQLite database is automatically created when the application starts.

## 🧠 AI Integration

The application uses the Google Gemini API to generate AI-powered responses.

The Gemini API integration is handled through:

```text
services/gemini_service.py
```

The API key is securely loaded from environment variables.

## 🗄️ Database

SQLite is used to manage application data.

The database stores:

- Registered users
- User authentication information
- Chat conversations
- User messages
- AI-generated responses
- Conversation history

Passwords are stored as secure hashes using Werkzeug.

## 🔄 How It Works

1. Users register or log in to the application.
2. The user enters a message in the chat interface.
3. JavaScript sends the message to the Flask backend.
4. Flask forwards the request to the Gemini API.
5. Gemini generates an AI response.
6. The application saves the conversation in SQLite.
7. The generated response is displayed in the chat interface.
8. Users can revisit previous conversations.

## 🎯 Project Objective

The objective of Lumen is to develop an interactive AI chatbot application that combines artificial intelligence, web development, user authentication, and database management.

The project demonstrates the integration of a large language model into a full-stack web application.

## 🔮 Future Enhancements

- Voice-based conversations
- Image and document uploads
- AI-powered document analysis
- Multiple AI model support
- Chat export functionality
- Advanced conversation search
- Multilingual chatbot support
- Cloud deployment

## 🔧 Troubleshooting

**AI is not configured**
- Check whether `GEMINI_API_KEY` is present in `.env`.
- Restart the Flask application.

**Invalid API key**
- Verify your Gemini API key.
- Generate a new key if necessary.

**AI is busy**
- The API may be experiencing high demand or rate limits.
- Try again later.

**Model unavailable**
- Check the model configured using `GEMINI_MODEL`.
- Select a currently supported Gemini model.

## 🔒 Security

- Passwords are hashed using Werkzeug.
- API keys are stored in environment variables.
- User conversations are stored in SQLite.
- The `.env` file should never be uploaded to GitHub.
- The local SQLite database should be excluded from GitHub if it contains user information.

## 👨‍💻 Author

**Vaishnav Pula**

B.Tech – Artificial Intelligence Engineering
