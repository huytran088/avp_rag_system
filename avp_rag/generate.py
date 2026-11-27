from typing import Dict, List, Optional, Tuple

from .providers import call_llm, get_provider_name, is_provider_configured
from .retrieve import retrieve_code


def build_prompt(
    user_request: str,
    context_snippets: List[Dict],
    code: Optional[str] = None,
    instructions: Optional[str] = None,
) -> str:
    """Build the LLM prompt from retrieved snippets, plus optional editor code and rules."""
    reference_block = "".join(
        f"\n// From file: {s['function_name']}\n{s['code']}\n" for s in context_snippets
    )
    prompt = f"""
You are an expert developer in the 'AVP' Pseudocode language.
Here is the strict syntax definition based on existing codebase examples:

--- REFERENCE CODE START ---
{reference_block}
--- REFERENCE CODE END ---

Using the syntax and style from the reference code above, write a complete AVP program to solve this task:
TASK: {user_request}

Rules:
1. Use strict 4-space indentation.
2. Use 'fun name(args): ... end fun' syntax.
3. Only use standard keywords (if, while, for, etc.) seen in the reference.
4. The reference code is only an example and is not available to your program: define every function the program calls.
5. Always include a function call after the function definitions (e.g. result = function_name(args)).
6. Do not explain, just output the code with detailed comments.
"""
    if code:
        prompt += (
            "\nThe user's current code (change it if the task asks for a change or a fix):\n"
            f"--- CURRENT CODE START ---\n{code}\n--- CURRENT CODE END ---\n"
        )
    if instructions:
        prompt += f"\nAdditional rules:\n{instructions}\n"
    return prompt


def build_context(
    user_request: str,
    k: int = 2,
    code: Optional[str] = None,
    instructions: Optional[str] = None,
) -> Tuple[List[Dict], Optional[str]]:
    """Retrieve snippets and build the prompt. Prompt is None when nothing was retrieved.

    Retrieval searches with the request plus the editor code; `instructions` only
    go into the prompt, so boilerplate rules don't skew the search.
    """
    search_text = f"{user_request}\n\n{code}" if code else user_request
    snippets = retrieve_code(search_text, k=k)
    if not snippets:
        return [], None
    return snippets, build_prompt(user_request, snippets, code, instructions)


def _complete(snippets: List[Dict], prompt: Optional[str]) -> Dict:
    if prompt is None:
        return {"generated_code": None, "retrieved_functions": [], "prompt": None}
    return {
        "generated_code": call_llm(prompt),
        "retrieved_functions": snippets,
        "prompt": prompt,
    }


def generate_code(
    user_request: str,
    k: int = 2,
    code: Optional[str] = None,
    instructions: Optional[str] = None,
) -> Dict:
    """Core generation logic. Returns dict with generated_code, retrieved_functions, prompt."""
    return _complete(*build_context(user_request, k=k, code=code, instructions=instructions))


def _print_simulation_help(provider: str) -> None:
    print(f"\n[SIMULATION MODE] {provider} provider is not configured.")
    hints = {
        "anthropic": "  export ANTHROPIC_API_KEY='your-api-key'",
        "vllm": "  export VLLM_BASE_URL='http://localhost:8080/v1'",
    }
    if provider in hints:
        print("Set the environment variable to enable generation:")
        print(hints[provider])


def generate_solution(user_request: str) -> Optional[str]:
    """CLI wrapper around generation that prints the prompt and the result."""
    print(f"\nProcessing Request: '{user_request}'...")

    snippets, prompt = build_context(user_request)
    if prompt is None:
        print("No relevant code found in knowledge base.")
        return None

    print("\n" + "=" * 60)
    print("      GENERATED PROMPT (What gets sent to the LLM)")
    print("=" * 60)
    print(prompt)
    print("=" * 60)

    # Show the prompt even in simulation mode
    if not is_provider_configured():
        _print_simulation_help(get_provider_name())
        return None

    print(f"\nCalling {get_provider_name()} provider...")
    try:
        result = _complete(snippets, prompt)
    except RuntimeError as e:
        print(f"\nError: {e}")
        return None

    print("\n" + "=" * 60)
    print("      GENERATED CODE")
    print("=" * 60)
    print(result["generated_code"])
    print("=" * 60)
    return result["generated_code"]


def main() -> None:
    print("--- RAG Generation Demo ---")

    while True:
        req = input("\nWhat code do you want to generate? (or 'exit'): ")
        if req.lower() == "exit":
            break
        generate_solution(req)


if __name__ == "__main__":
    main()
