# prompts/chain_of_thought.py
def build_chain_of_thought_prompt(question: str) -> str:
    """
    Wraps a question with step-by-step reasoning instructions.
    Forces the model to reason out loud before answering.
    """

    prompt = f"""Please reason through this step by step.
Show your thinking process clearly before giving 
your final answer.

Question: {question}

Let's think step by step:"""

    return prompt