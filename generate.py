import os
from retrieve import retrieve_code  # Importing our retrieval function
import anthropic

# --- CONFIGURATION ---
# Set ANTHROPIC_API_KEY environment variable to enable generation
# Optionally set ANTHROPIC_MODEL to use a different model
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")


def generate_code(user_request: str, k: int = 2) -> dict:
    """Core generation logic. Returns dict with generated_code, retrieved_functions, prompt."""
    context_snippets = retrieve_code(user_request, k=k)

    if not context_snippets:
        return {"generated_code": None, "retrieved_functions": [], "prompt": None}

    prompt = _build_prompt(user_request, context_snippets)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Set the environment variable to enable generation."
        )

    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    generated_code = message.content[0].text

    return {
        "generated_code": generated_code,
        "retrieved_functions": context_snippets,
        "prompt": prompt,
    }


def _build_prompt(user_request: str, context_snippets: list) -> str:
    """Build the LLM prompt from retrieved snippets."""
    prompt = """
You are an expert developer in the 'AVP' Pseudocode language.
Here is the strict syntax definition based on existing codebase examples:

--- REFERENCE CODE START ---
"""
    for snippet in context_snippets:
        prompt += f"\n// From file: {snippet['function_name']}\n"
        prompt += snippet['code'] + "\n"

    prompt += f"""
--- REFERENCE CODE END ---

Using the syntax and style from the reference code above, write a new AVP function to solve this task:
TASK: {user_request}

Rules:
1. Use strict 4-space indentation.
2. Use 'fun name(args): ... end fun' syntax.
3. Only use standard keywords (if, while, for, etc.) seen in the reference.
4. Do not explain, just output the code.
"""
    return prompt


def generate_solution(user_request):
    print(f"\nProcessing Request: '{user_request}'...")

    # Show prompt even in simulation mode
    context_snippets = retrieve_code(user_request, k=2)
    if not context_snippets:
        print("No relevant code found in knowledge base.")
        return None

    prompt = _build_prompt(user_request, context_snippets)
    print("\n" + "=" * 60)
    print("      GENERATED PROMPT (What gets sent to the LLM)")
    print("=" * 60)
    print(prompt)
    print("=" * 60)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\n[SIMULATION MODE] ANTHROPIC_API_KEY not set.")
        print("Set the environment variable to enable generation:")
        print("  export ANTHROPIC_API_KEY='your-api-key'")
        print("\nOptionally set a different model:")
        print("  export ANTHROPIC_MODEL='claude-haiku-3-5-20241022'")
        return None

    try:
        result = generate_code(user_request)
    except RuntimeError as e:
        print(f"\nError: {e}")
        return None

    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
    print(f"\nCalling {model}...")

    print("\n" + "=" * 60)
    print("      GENERATED CODE")
    print("=" * 60)
    print(result["generated_code"])
    print("=" * 60)
    return result["generated_code"]

if __name__ == "__main__":
    print("--- RAG Generation Demo ---")
    
    while True:
        req = input("\nWhat code do you want to generate? (or 'exit'): ")
        if req.lower() == 'exit':
            break
            
        generate_solution(req)