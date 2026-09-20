from flask import Flask, render_template, request, jsonify
from analyzer import analyze_password

app = Flask(__name__)


@app.after_request
def add_security_headers(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}

    password = data.get("password", "")

    if not isinstance(password, str):
        return jsonify({
            "error": "Invalid password input."
        }), 400

    result = analyze_password(password)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)