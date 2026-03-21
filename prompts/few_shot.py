# prompts/few_shot.py
# ─────────────────────────────────────────────────────────────
# WHAT THIS FILE DOES:
# Builds few-shot prompts by prepending examples to a question.
# This teaches the model the exact response FORMAT we want.
#
# BEST PRACTICE: Separation of Concerns
# Few-shot logic lives here, separate from other prompt types.
# ─────────────────────────────────────────────────────────────


def build_few_shot_prompt(examples: list, question: str) -> str:
    """
    Takes a list of example pairs and a question,
    builds a few-shot prompt string.

    WHY THIS FUNCTION:
    Instead of manually writing examples every time,
    just pass in a list of (input, output) pairs and
    your question — get a ready prompt back.

    Args:
        examples: list of dicts with 'input' and 'output' keys
        question: the actual question to ask

    Example:
        examples = [
            {"input": "A body found in the library",
             "output": "I observe the dust..."},
        ]
    """

    # Build the examples section
    # WHY THIS FORMAT: Clear Input/Output labels help the
    # model understand the pattern we want it to follow
    prompt = "Here are some examples of how to respond:\n\n"

    for i, example in enumerate(examples, 1):
        prompt += f"Example {i}:\n"
        prompt += f"Input: {example['input']}\n"
        prompt += f"Output: {example['output']}\n\n"

    # Add the actual question at the end
    # WHY AT THE END: Model reads examples first, learns
    # the pattern, then applies it to the new question
    prompt += f"Now respond to this in the same style:\n"
    prompt += f"Input: {question}\n"
    prompt += f"Output:"

    return prompt