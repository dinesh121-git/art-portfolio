import os
import threading
from datetime import datetime, timezone

import requests
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# ── MongoDB ──────────────────────────────────────────────────────────────────
MONGO_URI = os.environ.get("MONGO_URI", "")  # set in Render environment vars

def get_db():
    if not MONGO_URI:
        return None
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        return client["art_portfolio"]["profile_visits"]
    except Exception:
        return None


# ── IP Intelligence (runs in background so visitor feels no delay) ───────────
def fetch_ip_intel(ip: str) -> dict:
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=city,regionName,isp,country",
                         timeout=2)
        if r.status_code == 200:
            data = r.json()
            return {
                "city":    data.get("city", "Unknown"),
                "region":  data.get("regionName", "Unknown"),
                "country": data.get("country", "Unknown"),
                "isp":     data.get("isp", "Unknown"),
            }
    except Exception:
        pass
    return {"city": "Unknown", "region": "Unknown", "country": "Unknown", "isp": "Unknown"}


def save_visit(ip, user_agent, referrer):
    """Runs in a background thread — visitor never waits for this."""
    try:
        col = get_db()
        if col is None:
            return

        intel = fetch_ip_intel(ip)

        # Simple device detection from User-Agent
        ua = user_agent.lower()
        if "iphone" in ua:
            device = "iPhone"
        elif "ipad" in ua:
            device = "iPad"
        elif "android" in ua:
            device = "Android"
        elif "windows" in ua:
            device = "Windows PC"
        elif "mac" in ua:
            device = "Mac"
        elif "linux" in ua:
            device = "Linux"
        else:
            device = "Unknown Device"

        col.insert_one({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ip":        ip,
            "device":    device,
            "user_agent": user_agent,
            "referrer":  referrer or "Direct",
            "city":      intel["city"],
            "region":    intel["region"],
            "country":   intel["country"],
            "isp":       intel["isp"],
        })
    except Exception:
        pass  # Never crash the app because of analytics


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    # Extract visitor info
    forwarded = request.headers.get("X-Forwarded-For", "")
    ip = forwarded.split(",")[0].strip() if forwarded else request.remote_addr
    user_agent = request.headers.get("User-Agent", "")
    referrer   = request.headers.get("Referer", "")

    # Fire-and-forget analytics (background thread)
    thread = threading.Thread(target=save_visit, args=(ip, user_agent, referrer))
    thread.daemon = True
    thread.start()

    # Serve the gallery immediately
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
