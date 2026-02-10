import os
from retrieve import retrieve_code  # Importing our retrieval function
import anthropic

# --- CONFIGURATION ---
# Set ANTHROPIC_API_KEY environment variable to enable generation
# Optionally set ANTHROPIC_MODEL to use a different model
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

def generate_solution(user_request):
    print(f"\nProcessing Request: '{user_request}'...")
    
    # 1. RETRIEVE relevant snippets
    # We get the top 2 matches to give the LLM enough context
    context_snippets = retrieve_code(user_request, k=2)
    
    if not context_snippets:
        print("No relevant code found in knowledge base.")
        return None

    # 2. AUGMENT the prompt
    # We build a prompt that includes the retrieved code as "reference material"
    
    prompt = f"""
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

    # 3. GENERATE (Call the LLM)
    print("\n" + "="*60)
    print("      GENERATED PROMPT (What gets sent to the LLM)")
    print("="*60)
    print(prompt)
    print("="*60)

    if ANTHROPIC_API_KEY:
        print(f"\nCalling {ANTHROPIC_MODEL}...")
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        generated_code = message.content[0].text
        print("\n" + "="*60)
        print("      GENERATED CODE")
        print("="*60)
        print(generated_code)
        print("="*60)
        return generated_code
    else:
        print("\n[SIMULATION MODE] ANTHROPIC_API_KEY not set.")
        print("Set the environment variable to enable generation:")
        print("  export ANTHROPIC_API_KEY='your-api-key'")
        print("\nOptionally set a different model:")
        print("  export ANTHROPIC_MODEL='claude-haiku-3-5-20241022'")
        return None

if __name__ == "__main__":
    print("--- RAG Generation Demo ---")
    
    while True:
        req = input("\nWhat code do you want to generate? (or 'exit'): ")
        if req.lower() == 'exit':
            break
            
        generate_solution(req)