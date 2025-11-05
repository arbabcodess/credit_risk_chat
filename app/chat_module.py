import os
import requests
import json

# ✅ Updated to use the correct v1 chat completions endpoint
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
API_URL = "https://router.huggingface.co/v1/chat/completions"
API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not API_TOKEN:
    print("❌ ERROR: Environment variable HUGGINGFACEHUB_API_TOKEN is not set.")
    print("Please set it using: export HUGGINGFACEHUB_API_TOKEN='your_token_here'")
    exit(1)

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def get_recommendation(segment_name, ecl_value, pd_value, lgd_value, avg_interest=8.5):
    """
    Generate credit-risk recommendations via Hugging Face router inference API.
    """

    prompt = f"""You are a credit risk analyst. Analyze the following segment and provide a formal, 2-sentence recommendation.

Segment: {segment_name}
Expected Credit Loss (ECL): {ecl_value:.2f}
Probability of Default (PD): {pd_value:.2%}
Loss Given Default (LGD): {lgd_value:.2%}
Average Interest Rate: {avg_interest:.2f}%

Recommend one:
1. Increase interest rate
2. Reduce new disbursements
3. Maintain current policy

Provide reasoning briefly."""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 150,
        "temperature": 0.6
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        # Extract the response from OpenAI-compatible format
        if "choices" in data and len(data["choices"]) > 0:
            message = data["choices"][0].get("message", {})
            content = message.get("content", "")
            return content.strip()

        return str(data)

    except requests.exceptions.HTTPError as e:
        return f"⚠️ API request failed: {e}\nResponse: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"⚠️ API request failed: {e}"