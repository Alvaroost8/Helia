from flask import Flask, render_template, request, jsonify
from app.main import helia
import sys
import os

# Para poder importar app/*
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from app.tool_runner import run_tool

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/helia", methods=["POST"])
def prompt_helia():
    data = request.get_json()
    user_prompt = data.get("prompt", "").strip()

    if not user_prompt:
        return jsonify({"error": "Prompt vacío"}), 400

    return jsonify(helia(user_prompt))


if __name__ == "__main__":
    app.run(debug=True)
