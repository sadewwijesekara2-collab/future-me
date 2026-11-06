# -*- coding: utf-8 -*-
"""Future Me – Career Navigator (Flask backend)."""
import json
import os
import re

import requests as http
from dotenv import load_dotenv
from flask import Flask, Response, request, send_from_directory

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

# ── Configuration (all from environment / .env) ──────────────────────────────
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
PORT = int(os.getenv("PORT", "5000"))
DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

# Comma-separated list in .env; tried in order until one works.
DEFAULT_MODELS = [
    "google/gemini-2.0-flash-001",
    "google/gemini-2.0-flash-lite-001",
    "meta-llama/llama-3.3-70b-instruct:free",
    "deepseek/deepseek-chat:free",
]
MODELS = [m.strip() for m in os.getenv("OPENROUTER_MODELS", "").split(",") if m.strip()] or DEFAULT_MODELS

# Input limits (protects your API credit if the app is ever hosted publicly)
MAX_INTERESTS = 15
MAX_TEXT_LEN = 1500
MAX_MESSAGE_LEN = 1000


def json_response(data, status=200):
    return Response(
        json.dumps(data, ensure_ascii=False),
        status=status,
        mimetype="application/json; charset=utf-8",
    )


def ask(messages, temperature=0.7):
    """Call OpenRouter, falling back through MODELS until one succeeds."""
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set. Copy .env.example to .env and add your key.")
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": f"http://localhost:{PORT}",
        "X-Title": "Future Me - Career Navigator",
    }
    last_error = None
    for model in MODELS:
        try:
            print(f"  -> Trying {model}...")
            r = http.post(
                OPENROUTER_URL,
                headers=headers,
                json={"model": model, "messages": messages, "temperature": temperature},
                timeout=60,
            )
            r.raise_for_status()
            content = r.json()["choices"][0]["message"]["content"]
            if not content:
                raise ValueError("empty response")
            print(f"  OK with {model}")
            return content
        except Exception as e:  # noqa: BLE001
            print(f"  FAILED {model}: {str(e)[:80]}")
            last_error = e
    raise RuntimeError(f"All models failed. Last error: {last_error}")


def extract_json(text):
    """Parse JSON from model output, tolerating code fences and surrounding prose."""
    text = re.sub(r"```(?:json)?", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    starts = [i for i in (text.find("["), text.find("{")) if i != -1]
    if not starts:
        raise ValueError("No JSON found in model output")
    start = min(starts)
    end = max(text.rfind("]"), text.rfind("}"))
    return json.loads(text[start : end + 1])


def get_body():
    body = request.get_json(silent=True)
    return body if isinstance(body, dict) else {}


def clean_list(items, max_items, max_len):
    if not isinstance(items, list):
        return []
    return [str(i).strip()[:max_len] for i in items if str(i).strip()][:max_items]


SYSTEM_JSON = "Always return ONLY raw valid JSON — no markdown, no backticks, no explanation."


# ── Frontend ─────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/static/<path:name>")
def static_files(name):
    return send_from_directory(os.path.join(BASE_DIR, "static"), name)


@app.route("/health")
def health():
    return json_response({"status": "ok", "api_key_configured": bool(OPENROUTER_API_KEY)})


# ── /predict ─────────────────────────────────────────────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    interests = clean_list(get_body().get("interests"), MAX_INTERESTS, MAX_TEXT_LEN)
    if not interests:
        return json_response({"error": "No interests provided"}, 400)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a world-class career advisor with knowledge of every profession on Earth — "
                "traditional roles (medicine, law, engineering) and emerging fields (AI/ML, space tech, "
                "game dev, sustainable energy, biotech, digital art, esports, culinary arts, fashion, "
                "social work, trades, aviation, maritime, academia, and thousands more). " + SYSTEM_JSON
            ),
        },
        {
            "role": "user",
            "content": f"""Based on these interests: {", ".join(interests)}

Suggest 6-9 specific real career options. Think broadly across ALL global industries.
Include both well-known AND niche/emerging roles. Vary suggestions across different industries.

Return ONLY a raw JSON array. Each object must have exactly these keys:
{{
  "career":         "<Job title>",
  "score":          <integer 60-99>,
  "reason":         "<2-3 sentences why this fits the interests>",
  "salary":         "<Annual salary range e.g. LKR 1.2M-3.8M/year or $60,000-$120,000/year>",
  "companies":      ["<Co1>","<Co2>","<Co3>","<Co4>"],
  "qualifications": ["<Qual1>","<Qual2>","<Qual3>","<Qual4>"],
  "path":           "<3-4 step roadmap to enter this career>"
}}""",
        },
    ]
    try:
        data = extract_json(ask(messages, 0.7))
        if not isinstance(data, list):
            raise ValueError("Expected a JSON array")
        return json_response(data)
    except Exception as e:  # noqa: BLE001
        print(f"[predict] ERROR: {e}")
        return json_response({"error": str(e)}, 502)


# ── /chat ────────────────────────────────────────────────────────────────────
CHAT_PROMPT = """You are CareerBot, an expert AI career advisor inside the "Future Me" platform.
You know every career on Earth — traditional, trades, creative, tech, sports, military, arts, academia, emerging fields.
ONLY answer career-related questions: jobs, salaries, degrees, certifications, career paths, interview tips, CV advice.
If asked anything unrelated, politely decline and redirect to career topics.
Be encouraging, accurate, and concise. Use bullet points for lists. Keep replies under 200 words."""


@app.route("/chat", methods=["POST"])
def chat():
    body = get_body()
    message = str(body.get("message", "")).strip()[:MAX_MESSAGE_LEN]
    history = body.get("history", [])
    if not message:
        return json_response({"error": "Empty message"}, 400)

    messages = [{"role": "system", "content": CHAT_PROMPT}]
    if isinstance(history, list):
        # The frontend already includes the newest message in history; drop it to avoid duplicating.
        if history and isinstance(history[-1], dict) and history[-1].get("role") == "user" \
                and str(history[-1].get("text", "")).strip()[:MAX_MESSAGE_LEN] == message:
            history = history[:-1]
        for turn in history[-12:]:
            if not isinstance(turn, dict):
                continue
            role = "user" if turn.get("role") == "user" else "assistant"
            messages.append({"role": role, "content": str(turn.get("text", ""))[:MAX_MESSAGE_LEN]})
    messages.append({"role": "user", "content": message})

    try:
        return json_response({"reply": ask(messages, 0.8).strip()})
    except Exception as e:  # noqa: BLE001
        print(f"[chat] ERROR: {e}")
        return json_response({"error": str(e), "reply": "Sorry, the AI service is unavailable right now. Please try again."}, 502)


# ── /timeline ────────────────────────────────────────────────────────────────
@app.route("/timeline", methods=["POST"])
def timeline():
    career = str(get_body().get("career", "")).strip()[:120]
    if not career:
        return json_response({"error": "No career specified"}, 400)
    messages = [
        {"role": "system", "content": "You are an expert career counsellor. " + SYSTEM_JSON},
        {
            "role": "user",
            "content": f"""Give a career timeline for "{career}" from Year 1 to Year 10+.
Return ONLY a raw JSON array of exactly 5 objects with keys:
{{"year":"<e.g. Year 1-2>","role":"<Job title>","salary":"<e.g. LKR 800K/yr>","desc":"<1 sentence>"}}""",
        },
    ]
    try:
        data = extract_json(ask(messages, 0.5))
        if not isinstance(data, list):
            raise ValueError("Expected a JSON array")
        return json_response(data)
    except Exception as e:  # noqa: BLE001
        print(f"[timeline] ERROR: {e}")
        return json_response({"error": str(e)}, 502)


# ── /skillgap ────────────────────────────────────────────────────────────────
@app.route("/skillgap", methods=["POST"])
def skillgap():
    body = get_body()
    skills = clean_list(body.get("skills"), 30, 60)
    careers = clean_list(body.get("careers"), 6, 120)
    if not skills or not careers:
        return json_response({"error": "skills and careers are required"}, 400)
    messages = [
        {"role": "system", "content": "You are an expert career counsellor. " + SYSTEM_JSON},
        {
            "role": "user",
            "content": f"""I have these skills: {", ".join(skills)}.
Analyse my skill gap for these careers: {", ".join(careers)}.
Return ONLY a raw JSON array, one object per career:
{{"career":"<name>","readiness":<0-100>,"have":["skill1","skill2"],"need":["skill3","skill4"]}}
List only skills relevant to each career. Max 4 items per list.""",
        },
    ]
    try:
        data = extract_json(ask(messages, 0.4))
        if not isinstance(data, list):
            raise ValueError("Expected a JSON array")
        return json_response(data)
    except Exception as e:  # noqa: BLE001
        print(f"[skillgap] ERROR: {e}")
        return json_response({"error": str(e)}, 502)


if __name__ == "__main__":
    if not OPENROUTER_API_KEY:
        print("\n  [WARNING] OPENROUTER_API_KEY not set. Copy .env.example to .env and add your key.\n")
    app.run(host="127.0.0.1", port=PORT, debug=DEBUG)
