from config import GEMINI_API_KEY, GEMINI_MODEL, MAX_OUTPUT_TOKENS
from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL
from personas.sherlock import SHERLOCK
from personas.yoda import YODA
from personas.lady_whistledown import LADY_WHISTLEDOWN
from personas.phil import PHIL
from personas.barney import BARNEY
from prompts.system_prompt import build_system_prompt
from rag import load_pdf, split_into_chunks, create_collection, search_collection


#To add a new persona, just import it
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
    collection = None
    pdf_path = input("\n📄 Enter PDF path to load (or press Enter to skip): ").strip()
    if pdf_path:
        print("⏳ Loading PDF...")
        text = load_pdf(pdf_path)
        chunks = split_into_chunks(text)
        collection = create_collection(chunks)
        print(f"✅ PDF loaded! {len(chunks)} chunks indexed.\n")

    print("\n" + "═" * 50)
    print(f"🎭 You are now chatting with {persona['name']}")
    print("Type 'quit' to end the conversation")
    print("═" * 50 + "\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print(f"\n{persona['name']}: Farewell! 👋\n")
            with open("chat.txt", "w") as f:
                for message in conversation_history:
                    role = message["role"] 
                    if role == "user":
                        label = "You"
                    else:
                        label = persona['name']
                    text = " ".join(part["text"] for part in message["parts"])
                    f.write(f"{label}: {text}\n")
            
                
            break

        if not user_input:
            continue

        if collection:
            relevant_chunks = search_collection(collection, user_input)
            context = "\n\n".join(relevant_chunks)
            augmented_input = f"Context from document:\n{context}\n\nUser question: {user_input}"
        else:
            augmented_input = user_input

        conversation_history.append({
            "role": "user",
            "parts": [{"text": augmented_input}]
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