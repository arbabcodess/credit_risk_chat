import os
import requests
import json
import sys

# --------------------------
# Configuration
# --------------------------
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
# Correct API URL for Hugging Face router with OpenAI-compatible endpoint
API_URL = "https://router.huggingface.co/v1/chat/completions"

# Make sure you have your token set in the environment:
#   export HUGGINGFACEHUB_API_TOKEN="your_token_here"
API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not API_TOKEN:
    print("❌ ERROR: Environment variable HUGGINGFACEHUB_API_TOKEN is not set.")
    print("Please set it using: export HUGGINGFACEHUB_API_TOKEN='your_token_here'")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# OpenAI-compatible chat completion format
payload = {
    "model": MODEL_NAME,
    "messages": [
        {
            "role": "user",
            "content": "Say hello in one word."
        }
    ],
    "temperature": 0.7,
    "max_tokens": 10
}

# --------------------------
# Send Request
# --------------------------
try:
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    print("Status:", response.status_code)
    
    if response.status_code == 200:
        try:
            parsed = response.json()
            print("Body:", json.dumps(parsed, indent=2))
            
            # Extract and print the generated text from OpenAI-style response
            if "choices" in parsed and len(parsed["choices"]) > 0:
                message = parsed["choices"][0].get("message", {})
                content = message.get("content", "")
                print("\n✅ Generated text:", content)
        except Exception as e:
            print("Body:", response.text)
            print("❌ Error parsing JSON:", e)
    else:
        print("❌ Request failed with status:", response.status_code)
        print("Body:", response.text)
        
except requests.exceptions.RequestException as e:
    print("❌ Request failed:", e)