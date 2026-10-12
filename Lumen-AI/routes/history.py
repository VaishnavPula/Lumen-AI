"""Conversation history routes."""

import sqlite3

from flask import Blueprint, current_app, jsonify, session

from database.db import get_db, now_utc
from routes.auth import login_required


history_bp = Blueprint("history", __name__)


DB_ERROR = {
    "error": "Sorry, something went wrong. Please try again."
}


def find_conversation(conversation_id):
    """Find a conversation belonging to the logged-in user."""

    return get_db().execute(
        """
        SELECT *
        FROM conversations
        WHERE id = ? AND user_id = ?
        """,
        (conversation_id, session["user_id"])
    ).fetchone()


@history_bp.route("/api/conversations", methods=["GET"])
@login_required
def list_conversations():

    try:
        rows = get_db().execute(
            """
            SELECT id, title, created_at, updated_at
            FROM conversations
            WHERE user_id = ?
            ORDER BY updated_at DESC, id DESC
            """,
            (session["user_id"],)
        ).fetchall()

        return jsonify({
            "conversations": [dict(row) for row in rows]
        })

    except sqlite3.Error:
        current_app.logger.exception("Database error")
        return jsonify(DB_ERROR), 500


@history_bp.route("/api/conversations/new", methods=["POST"])
@login_required
def new_conversation():

    try:
        db = get_db()

        timestamp = now_utc()

        cursor = db.execute(
            """
            INSERT INTO conversations
            (user_id, title, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                session["user_id"],
                "New Chat",
                timestamp,
                timestamp
            )
        )

        db.commit()

        return jsonify({
            "conversation_id": cursor.lastrowid
        }), 201

    except sqlite3.Error:
        current_app.logger.exception("Database error")
        return jsonify(DB_ERROR), 500


@history_bp.route("/api/conversations/<int:conversation_id>", methods=["GET"])
@login_required
def get_conversation(conversation_id):

    try:
        conversation = find_conversation(conversation_id)

        if conversation is None:
            return jsonify({
                "error": "That conversation was not found."
            }), 404

        rows = get_db().execute(
            """
            SELECT sender, message, timestamp
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id
            """,
            (conversation_id,)
        ).fetchall()

        return jsonify({
            "conversation": {
                "id": conversation["id"],
                "title": conversation["title"]
            },
            "messages": [dict(row) for row in rows]
        })

    except sqlite3.Error:
        current_app.logger.exception("Database error")
        return jsonify(DB_ERROR), 500


@history_bp.route("/api/conversations/<int:conversation_id>", methods=["DELETE"])
@login_required
def delete_conversation(conversation_id):

    try:
        db = get_db()

        conversation = find_conversation(conversation_id)

        if conversation is None:
            return jsonify({
                "error": "That conversation was not found."
            }), 404

        db.execute(
            "DELETE FROM conversations WHERE id = ?",
            (conversation_id,)
        )

        db.commit()

        return jsonify({
            "deleted": True
        })

    except sqlite3.Error:
        current_app.logger.exception("Database error")
        return jsonify(DB_ERROR), 500

