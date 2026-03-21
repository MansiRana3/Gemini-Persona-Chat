# prompts/system_prompt.py
# ─────────────────────────────────────────────────────────────
# WHAT THIS FILE DOES:
# Takes a persona dictionary and builds a system prompt from it.
#
# BEST PRACTICE: Separation of Concerns
# The LOGIC of building prompts lives here.
# The DEFINITION of personas lives in personas/.
# These two things are kept completely separate.
# ─────────────────────────────────────────────────────────────


def build_system_prompt(persona: dict) -> str:
    """
    Takes a persona dictionary and combines all its fields
    into one clean system prompt string.

    WHY THIS FUNCTION EXISTS:
    Instead of manually writing out the system prompt every time,
    we just pass in a persona dict and get a ready-to-use
    prompt string back. Adding a new persona is just adding
    a new dict — this function works for all of them.
    """

    # Combine all persona fields into one clear instruction block
    # WHY THIS STRUCTURE: Clear sections make it easier for the
    # model to understand each aspect of the persona separately
    system_prompt = f"""
You are roleplaying as {persona['name']}.

ROLE:
{persona['role']}

PERSONALITY:
{persona['personality']}

RULES:
{persona['rules']}

EXAMPLE PHRASES TO USE:
{persona['example_phrases']}

Remember: Never break character. You ARE {persona['name']}.
""".strip()

    return system_prompt