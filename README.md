<div align="center">

<img src="static/favicon.png" alt="Future Me logo" width="96" />

# 🚀 Future Me — AI Career Navigator

**Discover careers that fit who you are. Take a quick quiz or list your interests, and get personalised career matches, salary ranges, roadmaps and an AI mentor — in seconds.**

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![OpenRouter](https://img.shields.io/badge/AI-OpenRouter-6467F2)
![License](https://img.shields.io/badge/License-MIT-green)


### 🌐 [**Live Site (interface preview) → https://sadewwijesekara2-collab.github.io/future-me/**](https://sadewwijesekara2-collab.github.io/future-me/)

*AI features run locally — see [Getting Started](#-getting-started).*

</div>

---

## 🎓 About This Project

**Future Me** is my **final project for the Rysera STEM AI Course**.

**About Rysera STEM:** Rysera STEM is the education arm of [Rysera Innovations](https://www.linkedin.com/company/rysera-innovations), a Sri Lankan technology and engineering company focused on product development, IoT and STEM education. Rysera STEM teaches practical technical skills — AI, robotics, Python and C++ — to school-leaver students, particularly after O/L and A/L.

**About the course:** The AI course is *AIM261 – AI Essentials: From Data to Agents*, an online module for post-A-Level students with basic Python knowledge. It runs for 8 weeks at 2 hours per week (16 hours in total) and takes students from working with data to building AI-powered applications.

**The idea:** Choosing a career is one of the hardest decisions students face, especially when they don't know which fields exist beyond the usual doctor/engineer/lawyer options. This was **my own idea** — a friendly website that turns a person's personality and interests into clear career suggestions with salary ranges, roadmaps and an AI mentor to ask follow-up questions.

**How it was built:** I came up with the concept, features and design direction myself, and used **[Claude](https://claude.ai) (an AI assistant by Anthropic)** as a coding assistant to help build, debug and polish the application.

> *Course details are summarised from publicly available information and may differ from the current Rysera STEM syllabus.*

---

## ✨ Features

| | Feature | What it does |
|---|---|---|
| 🧠 | **Personality Quiz** | 5 quick questions (pick up to 2 answers each) map your personality to careers |
| ⌨️ | **Interest Matching** | Type any interests (e.g. *gaming, biology, design*) and get live career suggestions |
| 🎯 | **Match Scores** | Every career comes with a compatibility %, the reason it fits, salary range and top hiring companies |
| 🗺️ | **Career Roadmap** | Required qualifications and a step-by-step entry path |
| 📅 | **Career Timeline** | See how a role progresses from Year 1 to Year 10+ with salary growth |
| ⚡ | **Skill Gap Analyser** | Enter your current skills and see your readiness % plus what you still need |
| 🤖 | **CareerBot** | A built-in AI career advisor for CVs, degrees, certifications and interview tips |
| 🔗 | **LinkedIn Jobs** | One-click job search for any suggested career |

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **AI:** [OpenRouter](https://openrouter.ai) API with automatic model fallback
- **Frontend:** Vanilla HTML, CSS and JavaScript (single file, no build step)

## 🚀 Getting Started

> 🌐 The [live site](https://sadewwijesekara2-collab.github.io/future-me/) shows the interface only. To use the AI features, run the project locally:

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/future-me.git
cd future-me
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your API key

Get a free key at [openrouter.ai/keys](https://openrouter.ai/keys), then:

```bash
cp .env.example .env        # Windows: copy .env.example .env
```

Open `.env` and set:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

> 🔒 `.env` is listed in `.gitignore`, so your key is never committed.

### 4. Run

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser. 🎉

**Windows shortcut:** just double-click `start.bat` — it installs dependencies, creates `.env` for you and launches the app.

## 🌐 Live Demo Note

The live site on GitHub Pages shows the **interface only**. GitHub Pages can't run the Python backend, so the AI features (career results, CareerBot, timeline, skill-gap analyser) **need the app to be run locally** — see [Getting Started](#-getting-started) above. It takes about two minutes.

## ⚙️ Configuration

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENROUTER_API_KEY` | ✅ | — | Your OpenRouter API key |
| `OPENROUTER_MODELS` | ❌ | built-in list | Comma-separated models, tried in order until one responds |
| `ALLOWED_ORIGINS` | ❌ | GitHub Pages + localhost | Websites allowed to call the API |
| `RATE_LIMIT_PER_HOUR` | ❌ | `60` | Max AI requests per visitor per hour |
| `PORT` | ❌ | `5000` | Port to run the server on |
| `FLASK_DEBUG` | ❌ | `false` | Set to `true` for auto-reload while developing |

## 📡 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/predict` | Career suggestions from interests / quiz answers |
| `POST` | `/chat` | CareerBot conversation |
| `POST` | `/timeline` | Year-by-year progression for a career |
| `POST` | `/skillgap` | Readiness and missing skills for chosen careers |
| `GET` | `/health` | Server status and whether an API key is configured |

## 📁 Project Structure

```
future-me/
├── app.py             # Flask backend + AI calls
├── index.html         # Frontend (UI, quiz, chat)
├── static/            # Favicon / assets
├── requirements.txt   # Python dependencies
├── start.bat          # One-click launcher (Windows)
├── .env.example       # Environment template (safe to commit)
└── .gitignore         # Keeps secrets out of Git
```

## 🔐 Security Notes

- API keys live **only** in `.env` — never hard-code them.
- If a key was ever committed or shared, **revoke it and create a new one**.
- Inputs are length-limited, each visitor is rate-limited, and only the allowed website can call the API — this protects your API credits on a public site.
- Set a low spending limit on your OpenRouter key.

## 🗺️ Roadmap

- [ ] Save and compare career results
- [ ] Export results as PDF
- [ ] Multi-language support
- [ ] Country-specific salary data
- [ ] User accounts

## 🤝 Contributing

Contributions, issues and feature requests are welcome! Fork the repo, create a branch, and open a pull request.

## 📄 License

Released under the [MIT License](LICENSE).

---

<div align="center">

Final project for the **Rysera STEM AI Course** · Idea by me, built with the help of Claude AI

Built with ❤️ to help people find careers they'll love.

</div>
