import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types
from chatbot_config import CHATBOT_TITLE, SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-3.1-flash-lite"


@app.route("/")
def home():
    return render_template("index.html", chatbot_title=CHATBOT_TITLE)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a question."}), 400

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.4,
            ),
        )
        reply = response.text or "Sorry, I could not generate a response."
    except Exception:
        reply = "Something went wrong while contacting the AI service. Please try again."

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
