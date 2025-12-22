import os
import json
from retrieve import retrieve_code  # Importing our retrieval function

# --- CONFIGURATION ---
# If you have an OpenAI or Gemini API Key, set it here to make it real.
# Otherwise, leave as None to see the "Simulation" output.
API_KEY = None  
MODEL_NAME = "gpt-4" # or "gemini-pro"

def generate_solution(user_request):
    print(f"\nProcessing Request: '{user_request}'...")
    
    # 1. RETRIEVE relevant snippets
    # We get the top 2 matches to give the LLM enough context
    context_snippets = retrieve_code(user_request, k=2)
    
    if not context_snippets:
        print("No relevant code found in knowledge base.")
        return

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

    if API_KEY:
        # Placeholder for actual API call (e.g., using openai or google-generativeai)
        # client = OpenAI(api_key=API_KEY)
        # response = client.chat.completions.create(...)
        # print(response.choices[0].message.content)
        pass
    else:
        print("\n[SIMULATION MODE] API Key not set.")
        print("Copy the prompt above and paste it into ChatGPT/Gemini to see the magic!")
        print("To automate this, uncomment the API call section in generate.py.")

if __name__ == "__main__":
    print("--- RAG Generation Demo ---")
    
    while True:
        req = input("\nWhat code do you want to generate? (or 'exit'): ")
        if req.lower() == 'exit':
            break
            
        generate_solution(req)