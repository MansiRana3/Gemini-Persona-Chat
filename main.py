# main.py
from config import GEMINI_API_KEY, GEMINI_MODEL, MAX_OUTPUT_TOKENS
from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL
from personas.sherlock import SHERLOCK
from personas.yoda import YODA
from personas.lady_whistledown import LADY_WHISTLEDOWN
from personas.phil import PHIL
from personas.barney import BARNEY
from prompts.system_prompt import build_system_prompt


# ── Persona Registry ──────────────────────────────────────────
# WHY A DICTIONARY: To add a new persona, just import it
# and add one line here. Nothing else changes.
PERSONAS = {
    "1": SHERLOCK,
    "2": YODA,
    "3": LADY_WHISTLEDOWN,
    "4": PHIL,
    "5": BARNEY,
}


def show_menu():
    print("\n" + "═" * 50)
    print("🎭 AI PERSONA ROLEPLAY ENGINE")
    print("═" * 50)
    print("Choose your character:\n")
    print("  1. Sherlock Holmes 🔍")
    print("  2. Yoda 🌿")
    print("  3. Lady Whistledown 📜")
    print("  4. Phil Dunphy 🏡")
    print("  5. Barney Stinson 👔")
    print("\n  Type 'quit' to exit")
    print("═" * 50)


def get_persona_choice() -> dict:
    while True:
        show_menu()
        choice = input("\nYour choice: ").strip()

        if choice.lower() == "quit":
            print("\nLegendary farewell! 👋\n")
            exit()

        if choice in PERSONAS:
            return PERSONAS[choice]

        print(f"\n❌ Invalid choice. Please enter 1 to 7.")


def chat_with_persona(persona: dict):
    system_prompt = build_system_prompt(persona)
    client = genai.Client(api_key=GEMINI_API_KEY)
    conversation_history = []

    print("\n" + "═" * 50)
    print(f"🎭 You are now chatting with {persona['name']}")
    print("Type 'quit' to end the conversation")
    print("═" * 50 + "\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print(f"\n{persona['name']}: Farewell! 👋\n")
            break

        if not user_input:
            continue

        conversation_history.append({
            "role": "user",
            "parts": [{"text": user_input}]
        })

        try:
            response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents=conversation_history,
    config={
        "system_instruction": system_prompt,
        # WHY: Limits response length so replies feel
        # like natural conversation not an essay
        "max_output_tokens": MAX_OUTPUT_TOKENS
    }
)

            reply = response.text

            conversation_history.append({
                "role": "model",
                "parts": [{"text": reply}]
            })

            print(f"\n{persona['name']}: {reply}\n")

        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    chosen_persona = get_persona_choice()
    chat_with_persona(chosen_persona)