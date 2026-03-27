# config.py
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

GEMINI_REST_BASE_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)

if not GEMINI_API_KEY:
    raise EnvironmentError(
        "\n❌ GEMINI_API_KEY not found!\n"
        "Make sure you have a .env file with: GEMINI_API_KEY=your_key_here\n"
        "Get your key at: https://aistudio.google.com"
    )

DEFAULT_TEMPERATURE = 1.0
MAX_OUTPUT_TOKENS = 1024

print("✅ config.py loaded — API key found, constants ready.")
# ── Temperature Presets ───────────────────────────────────────
# WHY PRESETS: Instead of remembering numbers, use named
# presets that describe what each temperature actually does.
# This is more readable and easier to change later.

TEMPERATURE_PRECISE = 0.2   # factual, consistent, low creativity
TEMPERATURE_BALANCED = 1.0  # natural, default for conversation
TEMPERATURE_CREATIVE = 1.8  # highly creative, dramatic, expressive