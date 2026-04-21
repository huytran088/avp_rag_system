from providers import call_llm, get_provider_name, is_provider_configured
from retrieve import retrieve_code


def _build_prompt(user_request: str, context_snippets: list) -> str:
    """Build the LLM prompt from retrieved snippets."""
    reference_block = "".join(
        f"\n// From file: {s['function_name']}\n{s['code']}\n"
        for s in context_snippets
    )
    return f"""
You are an expert developer in the 'AVP' Pseudocode language.
Here is the strict syntax definition based on existing codebase examples:

--- REFERENCE CODE START ---
{reference_block}
--- REFERENCE CODE END ---

Using the syntax and style from the reference code above, write a new AVP function to solve this task:
TASK: {user_request}

Rules:
1. Use strict 4-space indentation.
2. Use 'fun name(args): ... end fun' syntax.
3. Only use standard keywords (if, while, for, etc.) seen in the reference.
4. Do not explain, just output the code.
"""


def generate_code(user_request: str, k: int = 2) -> dict:
    """Core generation logic. Returns dict with generated_code, retrieved_functions, prompt."""
    context_snippets = retrieve_code(user_request, k=k)

    if not context_snippets:
        return {"generated_code": None, "retrieved_functions": [], "prompt": None}

    prompt = _build_prompt(user_request, context_snippets)
    generated_code = call_llm(prompt)

    return {
        "generated_code": generated_code,
        "retrieved_functions": context_snippets,
        "prompt": prompt,
    }


def _print_simulation_help(provider: str) -> None:
    print(f"\n[SIMULATION MODE] {provider} provider is not configured.")
    hints = {
        "anthropic": "  export ANTHROPIC_API_KEY='your-api-key'",
        "vllm": "  export VLLM_BASE_URL='http://localhost:8080/v1'",
    }
    if provider in hints:
        print("Set the environment variable to enable generation:")
        print(hints[provider])


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

    if not is_provider_configured():
        _print_simulation_help(get_provider_name())
        return None

    try:
        result = generate_code(user_request)
    except RuntimeError as e:
        print(f"\nError: {e}")
        return None

    print(f"\nCalling {get_provider_name()} provider...")

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
