import os
import requests

# --- Configuration ---
# Set your API keys as environment variables
# export DEEPSEEK_API_KEY='YOUR_DEEPSEEK_API_KEY'
# export OPENAI_API_KEY='YOUR_OPENAI_API_KEY'

DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

# --- Helper Function to call an API ---
def call_api(api_key, url, model_name, prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150 # Limit response length for brevity
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status() # Raise an exception for bad status codes
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.exceptions.RequestException as e:
        return f"Error calling API: {e}"

# --- Main Comparison Logic ---
def compare_models(prompt):
    results = {}

    # Call DeepSeek R1
    if DEEPSEEK_API_KEY:
        print("Calling DeepSeek R1...")
        results['deepseek_r1'] = call_api(
            DEEPSEEK_API_KEY, DEEPSEEK_URL, "deepseek-coder-v2-lite", prompt
        )
    else:
        results['deepseek_r1'] = "DeepSeek API key not set."

    # Call OpenAI o3-mini
    if OPENAI_API_KEY:
        print("Calling OpenAI o3-mini...")
        results['openai_o3_mini'] = call_api(
            OPENAI_API_KEY, OPENAI_URL, "gpt-3.5-turbo", prompt
        )
    else:
        results['openai_o3_mini'] = "OpenAI API key not set."

    return results

# --- Example Usage ---
if __name__ == "__main__":
    example_prompt = "Explain the concept of recursion in programming in simple terms."
    print(f"Prompt: {example_prompt}\n")

    comparison_results = compare_models(example_prompt)

    print("--- Comparison Results ---")
    print(f"DeepSeek R1:\n{comparison_results.get('deepseek_r1', 'N/A')}\n")
    print(f"OpenAI o3-mini:\n{comparison_results.get('openai_o3_mini', 'N/A')}\n")
