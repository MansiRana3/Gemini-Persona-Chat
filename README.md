# 🎭 AI Persona Roleplay Engine

A CLI app where you can chat with fictional characters in your terminal — powered by Google's Gemini AI.

I built this as my first hands-on GenAI project to actually understand how LLMs work, not just use them.

---

## What it does

Pick a character from the menu and just... talk to them. They stay in character, remember what you said earlier in the conversation, and respond in their own style and personality.

Current characters:
- Sherlock Holmes 🔍
- Yoda 🌿
- Lady Whistledown 📜
- Phil Dunphy 🏡
- Barney Stinson 👔

---

## How to run it

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/ai-persona-engine.git
cd ai-persona-engine
```

**2. Create virtual environment**
```bash
py -m venv venv
.\venv\Scripts\Activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your API key**

Create a `.env` file in the root folder:
```
GEMINI_API_KEY=your_key_here
```
Get a free key at [aistudio.google.com](https://aistudio.google.com)

**5. Run**
```bash
py main.py
```

---

## What I actually learned building this

I wanted to understand GenAI from the ground up so I built everything the hard way first.

**LLM basics** — what tokens are, how context windows work, why LLMs are stateless and have no memory of their own

**Two ways to call the same API** — I built the Gemini connection twice on purpose. Once using raw HTTP requests where I manually wrote the URL, headers, and JSON body. Then again using Google's official SDK which does all that in 3 lines. Doing it both ways meant I actually understood what the SDK was hiding from me.

**Prompting techniques** — zero-shot, few-shot, system prompting, role prompting, chain-of-thought, and temperature tuning. Each one is implemented separately so I could see exactly how they behave differently.

**Conversation memory** — LLMs don't remember anything between requests. The way memory works is you maintain a list of every message sent and received, then send the full list every single time. Gemini isn't remembering — you're reminding it. This is how ChatGPT works too.

---

## Project structure
```
ai_persona_engine/
├── .env                    # API key — never committed
├── config.py               # All constants in one place
├── gemini_rest.py          # Gemini via raw HTTP
├── gemini_sdk.py           # Gemini via official SDK
├── main.py                 # The chat loop
├── personas/               # One file per character
└── prompts/                # Prompting logic
```

I kept things separated on purpose — personas know nothing about API calls, API files know nothing about characters. Each file has one job.

---

## Things I want to add later

- Save chat history so characters remember across sessions
- Web UI instead of CLI
- RAG so characters can reference custom documents
- More characters

---

## Tech used

Python, Google Gemini API (gemini-2.5-flash), google-genai SDK, requests, python-dotenv
