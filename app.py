from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

FEW_SHOT = """
Example 1
Input:
Intent: Follow up after a workshop
Key Facts:
- thank the team for attending on Monday
- share that the deck is attached
- request feedback by Thursday
Tone: professional

Output:
Subject: Follow-Up After Monday's Workshop

Dear Team,

Thank you for attending the workshop on Monday. I appreciate your time and engagement during the session.

Please find the presentation deck attached for your reference. I would be grateful if you could share your feedback by Thursday so we can incorporate it into the next phase.

Best regards,
Your Name

Example 2
Input:
Intent: Apologize for a delayed response
Key Facts:
- acknowledge delay
- explain travel schedule caused backlog
- confirm detailed reply will be sent tomorrow
Tone: empathetic

Output:
Subject: Apology for the Delayed Response

Dear [Name],

I apologize for the delay in getting back to you. My recent travel schedule created a backlog, and I appreciate your patience.

I will send a detailed response by tomorrow.

Warm regards,
Your Name
"""

def build_advanced_prompt(intent, key_facts, tone):
    facts_block = "\n".join([f"- {fact}" for fact in key_facts])
    return f"""
You are a senior executive communications assistant.
Write a polished professional email.

Requirements:
- Include a clear subject line.
- Use an appropriate greeting.
- Naturally incorporate every key fact without copying the bullets mechanically.
- Match the requested tone exactly.
- Keep the email concise but complete.
- End with a professional sign-off.
- Before finalizing, verify internally that every fact has been included.

{FEW_SHOT}

Now write the email.

Input:
Intent: {intent}
Key Facts:
{facts_block}
Tone: {tone}
"""

def build_baseline_prompt(intent, key_facts, tone):
    facts_block = "\n".join([f"- {fact}" for fact in key_facts])
    return f"Write a {tone} email for this intent: {intent}. Include these facts:\n{facts_block}"

def generate_email(prompt, model=None):
    model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    response = client.responses.create(
        model=model,
        input=prompt
    )
    return response.output_text.strip()

def main():
    intent = input("Intent: ").strip()
    tone = input("Tone: ").strip()
    print("Enter key facts one per line. Submit an empty line to finish.")
    key_facts = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        key_facts.append(line)

    advanced = generate_email(build_advanced_prompt(intent, key_facts, tone))
    baseline = generate_email(build_baseline_prompt(intent, key_facts, tone))

    print("\n=== Strategy A: Advanced Prompt ===\n")
    print(advanced)
    print("\n=== Strategy B: Baseline Prompt ===\n")
    print(baseline)

if __name__ == "__main__":
    main()
