from flask import Flask, request, jsonify, redirect
from datetime import datetime, timedelta
import random, string

from LoggingMiddleware.logger import log_request

app = Flask(__name__)
log_request(app)

urls = {}

API_KEY = "mysecretapikey"

def require_auth():
    """Simple auth check with Bearer token"""
    key = request.headers.get("Authorization")
    if key != f"Bearer {API_KEY}":
        return False
    return True

def generate_shortcode():
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if code not in urls:
            return code

@app.route("/shorturls", methods=["POST"])
def create_short_url():
    if not require_auth():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    validity = int(data.get("validity", 30))  # default 30 minutes
    shortcode = data.get("shortcode")

    if shortcode:
        if shortcode in urls:
            return jsonify({"error": "Shortcode already exists"}), 409
    else:
        shortcode = generate_shortcode()

    expiry_time = datetime.utcnow() + timedelta(minutes=validity)
    entry = {
        "shortcode": shortcode,
        "originalUrl": url,
        "expiry": expiry_time,
        "createdAt": datetime.utcnow(),
        "clicks": []
    }
    urls[shortcode] = entry

    return jsonify({
        "shortLink": f"http://localhost:5000/{shortcode}",
        "expiry": expiry_time.isoformat(),
        "validityMinutes": validity
    }), 201

@app.route("/shorturls/<shortcode>", methods=["GET"])
def get_stats(shortcode):
    if not require_auth():
        return jsonify({"error": "Unauthorized"}), 401

    url_doc = urls.get(shortcode)
    if not url_doc:
        return jsonify({"error": "Shortcode not found"}), 404

    now = datetime.utcnow()
    remaining_seconds = (url_doc["expiry"] - now).total_seconds()
    remaining_minutes = max(0, int(remaining_seconds // 60))

    return jsonify({
        "originalUrl": url_doc["originalUrl"],
        "createdAt": url_doc["createdAt"],
        "expiry": url_doc["expiry"],
        "timeLeftMinutes": remaining_minutes,
        "clickCount": len(url_doc["clicks"]),
        "clicks": url_doc["clicks"]
    }), 200

@app.route("/<shortcode>", methods=["GET"])
def redirect_url(shortcode):
    url_doc = urls.get(shortcode)
    if not url_doc:
        return jsonify({"error": "Shortcode not found"}), 404
    if datetime.utcnow() > url_doc["expiry"]:
        return jsonify({"error": "Link expired"}), 410

    click = {
        "timestamp": datetime.utcnow(),
        "referrer": request.referrer,
        "ip": request.remote_addr,
        "userAgent": request.headers.get("User-Agent")
    }
    url_doc["clicks"].append(click)
    return redirect(url_doc["originalUrl"])

if __name__ == "__main__":
    app.run(debug=True)