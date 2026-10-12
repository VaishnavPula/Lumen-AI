"""The chat page and the endpoint that sends messages to Gemini."""
import re
import sqlite3

from flask import (Blueprint, current_app, jsonify, render_template,
                   request, session)

from database.db import get_db, now_utc
from routes.auth import login_required
from services.gemini_service import GeminiError, get_ai_reply

chat_bp = Blueprint("chat", __name__)

# Words we drop from the start of a message when making a chat title.
FILLER_WORDS = {
    "explain", "help", "me", "please", "can", "you", "could", "tell", "what", "is",
    "are", "how", "do", "does", "to", "the", "a", "an", "about", "with", "my",
    "i", "need", "want", "show", "give", "write", "make", "of", "in", "on", "for",
}


def make_title(message):
    """'Explain Flask routing' -> 'Flask Routing'."""
    words = re.findall(r"[A-Za-z0-9+#.']+", message)
    useful = [w for w in words if w.lower() not in FILLER_WORDS] or words
    title = " ".join(useful[:5]).title()
    return title[:50] or "New Chat"


@chat_bp.route("/chat")
@login_required
def chat_page():
    return render_template("chat.html", username=session.get("username", "User"))


@chat_bp.route("/api/chat", methods=["POST"])
@login_required
def send_message():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    conversation_id = data.get("conversation_id")
    max_length = current_app.config["MAX_MESSAGE_LENGTH"]

    if not message:
        return jsonify({"error": "Please type a message first."}), 400
    if len(message) > max_length:
        return jsonify({"error": f"Messages can be up to {max_length} characters long."}), 400

    try:
        db = get_db()
        history = []

        if conversation_id is not None:
            # Make sure this conversation belongs to the logged-in user.
            conversation = db.execute(
                "SELECT * FROM conversations WHERE id = ? AND user_id = ?",
                (conversation_id, session["user_id"]),
            ).fetchone()
            if conversation is None:
                return jsonify({"error": "That conversation was not found."}), 404

            rows = db.execute(
                "SELECT sender, message FROM messages WHERE conversation_id = ? ORDER BY id DESC LIMIT ?",
                (conversation["id"], current_app.config["MAX_HISTORY_MESSAGES"]),
            ).fetchall()
            history = [dict(row) for row in reversed(rows)]

        # Ask Gemini first. If it fails, nothing half-finished is saved.
        try:
            reply = get_ai_reply(history, message)
        except GeminiError as error:
            return jsonify({"error": error.user_message}), error.status_code

        timestamp = now_utc()
        if conversation_id is None:
            cursor = db.execute(
                "INSERT INTO conversations (user_id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (session["user_id"], make_title(message), timestamp, timestamp),
            )
            conversation_id = cursor.lastrowid
        elif not history:
            # An empty chat from the "New Chat" button gets its title from the first message.
            db.execute("UPDATE conversations SET title = ? WHERE id = ?", (make_title(message), conversation_id))

        db.execute(
            "INSERT INTO messages (conversation_id, sender, message, timestamp) VALUES (?, 'user', ?, ?)",
            (conversation_id, message, timestamp),
        )
        reply_time = now_utc()
        db.execute(
            "INSERT INTO messages (conversation_id, sender, message, timestamp) VALUES (?, 'bot', ?, ?)",
            (conversation_id, reply, reply_time),
        )
        db.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (reply_time, conversation_id))
        db.commit()

        title = db.execute("SELECT title FROM conversations WHERE id = ?", (conversation_id,)).fetchone()["title"]
        return jsonify({
            "reply": reply,
            "timestamp": reply_time,
            "user_timestamp": timestamp,
            "conversation_id": conversation_id,
            "title": title,
        })

    except sqlite3.Error:
        current_app.logger.exception("Database error in /api/chat")
        return jsonify({"error": "Sorry, something went wrong. Please try again."}), 500
