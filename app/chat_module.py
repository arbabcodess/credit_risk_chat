from transformers import pipeline

# ---------------------------------------------------------
# Lightweight model for Hugging Face Spaces / local testing
# ---------------------------------------------------------
# "facebook/blenderbot-400M-distill" → small, quick, works on CPU
# You can also try "tiiuae/falcon-1b" if you want something a bit smarter (≈1 GB)
# ---------------------------------------------------------

MODEL_NAME = "facebook/blenderbot-400M-distill"

chatbot = pipeline(
    "text-generation",
    model=MODEL_NAME,
    max_new_tokens=120,
    do_sample=True,
    temperature=0.7
)

def get_recommendation(segment_name, ecl_value, pd_value, lgd_value, avg_interest=8.5):
    """
    Generates a short, formal credit-risk recommendation using a lightweight
    Hugging Face model. Runs fully offline on Spaces.
    """

    prompt = f"""
    You are a financial risk analyst at a digital bank.
    Analyze the following loan segment:

    Segment: {segment_name}
    Expected Credit Loss (ECL): {ecl_value:.2f}
    Probability of Default (PD): {pd_value:.2%}
    Loss Given Default (LGD): {lgd_value:.2%}
    Average Interest Rate: {avg_interest:.2f}%

    Based on these values, briefly recommend one of the following:
    1. Increase interest rate to offset higher risk.
    2. Reduce new loan disbursements to this segment.
    3. Maintain current policy if risk is acceptable.

    Provide reasoning in 2 concise sentences.
    """

    # Generate a short text
    response = chatbot(prompt, max_new_tokens=100)
    text = response[0]["generated_text"]

    # Trim duplicated prompt (model tends to echo input)
    if text.startswith(prompt):
        text = text[len(prompt):].strip()

    return text.strip() or "No recommendation generated."
