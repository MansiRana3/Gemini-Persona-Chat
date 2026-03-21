from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL, TEMPERATURE_BALANCED


def call_gemini_sdk(
    prompt: str,
    system_prompt: str = None,
    temperature: float = TEMPERATURE_BALANCED
) -> str:
    """
    Sends a message to Gemini using the official SDK.
    Now supports system prompts AND temperature control.

    Args:
        prompt: your message or question
        system_prompt: optional persona/rules for the model
        temperature: creativity level (0.0 to 2.0)
                     low = precise, high = creative
    """

    client = genai.Client(api_key=GEMINI_API_KEY)

    print(f"\n📤 Sending to Gemini (SDK): {prompt[:60]}...")
    print(f"🌡️  Temperature: {temperature}")

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={
            "system_instruction": system_prompt or "",
            # WHY IN CONFIG: Temperature is a generation
            # parameter — it controls HOW the model generates,
            # not WHAT it generates. Belongs in config block.
            "temperature": temperature,
        }
    )

    gemini_reply = response.text
    print(f"📥 Gemini replied: {gemini_reply}")
    return gemini_reply


if __name__ == "__main__":
    from personas.sherlock import SHERLOCK
    from prompts.system_prompt import build_system_prompt
    from prompts.few_shot import build_few_shot_prompt
    from prompts.chain_of_thought import build_chain_of_thought_prompt
    from config import TEMPERATURE_PRECISE, TEMPERATURE_CREATIVE

    system = build_system_prompt(SHERLOCK)

    # ── TEST 1: Few-Shot Prompting ────────────────────────────
    print("\n" + "═"*50)
    print("TEST 1: Few-Shot Prompting")
    print("═"*50)

    examples = [
        {
            "input": "There are muddy footprints leading to the window",
            "output": "Observe the depth of the heel — our man is heavy set, "
                      "at least fourteen stone. The stride length suggests "
                      "haste. He came from the east, Watson."
        },
        {
            "input": "The victim's watch was found broken at 3:15",
            "output": "The watch stopped at precisely 3:15 — yet the "
                      "housekeeper claims she heard nothing until 4. "
                      "Someone set that watch deliberately, my dear fellow."
        }
    ]

    few_shot = build_few_shot_prompt(
        examples=examples,
        question="A letter was found burnt in the fireplace"
    )

    call_gemini_sdk(
        prompt=few_shot,
        system_prompt=system,
        temperature=TEMPERATURE_PRECISE
    )

    # ── TEST 2: Chain-of-Thought Prompting ───────────────────
    print("\n" + "═"*50)
    print("TEST 2: Chain-of-Thought Prompting")
    print("═"*50)

    cot = build_chain_of_thought_prompt(
        "Holmes, three suspects were in the house. "
        "The butler was in the kitchen at 8pm. "
        "The maid left at 7pm. "
        "The gardener has mud on his boots. "
        "The victim died between 7:30 and 8:30pm. "
        "Who is the most likely suspect?"
    )

    call_gemini_sdk(
        prompt=cot,
        system_prompt=system,
        temperature=TEMPERATURE_PRECISE
    )

    # ── TEST 3: Temperature Comparison ───────────────────────
    print("\n" + "═"*50)
    print("TEST 3: Temperature Comparison")
    print("═"*50)

    question = "Holmes, describe London on a foggy morning."

    print("\n🥶 LOW temperature (precise):")
    call_gemini_sdk(
        prompt=question,
        system_prompt=system,
        temperature=TEMPERATURE_PRECISE
    )

    print("\n🔥 HIGH temperature (creative):")
    call_gemini_sdk(
        prompt=question,
        system_prompt=system,
        temperature=TEMPERATURE_CREATIVE
    )