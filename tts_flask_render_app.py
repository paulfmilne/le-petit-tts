
from flask import Flask, request, Response
import openai
import os
import io

app = Flask(__name__)

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
