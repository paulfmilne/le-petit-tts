from flask import Flask, request, Response
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # 🔓 Enable CORS for all incoming requests

# Load your OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    wine_term = data.get("wine_term", "")

    if not wine_term:
        return {"error": "Missing wine_term"}, 400

    try:
        response = openai.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=wine_term
        )

        return Response(
            response.content,
            mimetype="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=pronunciation.mp3"}
        )

    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/", methods=["GET"])
def health():
    return {"status": "OK"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
