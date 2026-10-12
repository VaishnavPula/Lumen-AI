from flask import Flask, jsonify, render_template, request, session

from config import Config
from database.db import init_db
from routes.auth import auth_bp
from routes.chat import chat_bp
from routes.history import history_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)  # creates instance/chatbot.db the first time you run the app

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(history_bp)

    @app.route("/")
    def index():
        return render_template("index.html", logged_in="user_id" in session)

    # Friendly errors instead of raw Python error pages.
    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Not found."}), 404
        return render_template("index.html", logged_in="user_id" in session), 404

    @app.errorhandler(500)
    def server_error(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Sorry, something went wrong. Please try again."}), 500
        return "Sorry, something went wrong. Please try again.", 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
