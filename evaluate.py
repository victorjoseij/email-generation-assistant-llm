import json, csv, os, re, statistics
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def build_advanced_prompt(intent, key_facts, tone):
    facts_block = "\n".join([f"- {fact}" for fact in key_facts])
    few_shot = """
Example
Intent: Request a status update
Key Facts:
- project started last week
- waiting for API keys
- request update by Wednesday
Tone: professional

Output:
Subject: Request for Status Update

Dear Team,

I hope you are doing well. I wanted to check in on the current status of the project that began last week. At the moment, we are waiting for the API keys needed to move forward.

Could you please share an update by Wednesday?

Best regards,
Your Name
"""
    return f"""
You are a senior executive communications assistant.
Write a polished professional email.

Requirements:
- Include a clear subject line.
- Use an appropriate greeting.
- Naturally incorporate every key fact.
- Match the requested tone.
- Keep the email concise but complete.
- End with a professional sign-off.
- Internally check that all facts are included before finalizing.

{few_shot}

Intent: {intent}
Key Facts:
{facts_block}
Tone: {tone}
"""

def build_baseline_prompt(intent, key_facts, tone):
    facts_block = "\n".join([f"- {fact}" for fact in key_facts])
    return f"Write a {tone} email for this intent: {intent}. Include these facts:\n{facts_block}"

def generate_email(prompt):
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    resp = client.responses.create(model=model, input=prompt)
    return resp.output_text.strip()

def fact_coverage_score(text, fact_patterns):
    text_low = text.lower()
    matched = 0
    for pattern_group in fact_patterns:
        ok = all(token.lower() in text_low for token in pattern_group)
        matched += 1 if ok else 0
    return matched / len(fact_patterns)

def structure_score(text):
    text_low = text.lower()
    checks = []
    checks.append(1 if "subject:" in text_low else 0)
    checks.append(1 if any(g in text_low for g in ["dear ", "hi ", "hello "]) else 0)
    checks.append(1 if len(re.findall(r'\n\n', text)) >= 2 else 0)
    checks.append(1 if any(c in text_low for c in ["please", "could you", "let me know", "thank you"]) else 0)
    checks.append(1 if any(s in text_low for s in ["best regards", "regards", "sincerely", "warm regards"]) else 0)
    wc = len(text.split())
    checks.append(1 if 80 <= wc <= 220 else 0)
    return sum(checks) / len(checks)

def tone_alignment_score(prompt_tone, generated_email):
    judge_model = os.getenv("OPENAI_JUDGE_MODEL", "gpt-4.1-mini")
    rubric = f"""
You are evaluating only tone alignment for a generated professional email.

Requested tone: {prompt_tone}

Score from 1 to 5:
1 = tone clearly wrong
2 = mostly wrong
3 = partially correct
4 = strong match
5 = excellent match

Return only a single integer 1-5.
"""
    resp = client.responses.create(
        model=judge_model,
        input=f"{rubric}\n\nEmail:\n{generated_email}"
    )
    raw = resp.output_text.strip()
    m = re.search(r'[1-5]', raw)
    score = int(m.group(0)) if m else 3
    return score / 5

def main():
    with open("scenarios.json", "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    rows = []
    for scenario in scenarios:
        for strategy_name, prompt_builder in {
            "advanced": build_advanced_prompt,
            "baseline": build_baseline_prompt
        }.items():
            email = generate_email(prompt_builder(
                scenario["intent"], scenario["key_facts"], scenario["tone"]
            ))
            fcs = fact_coverage_score(email, scenario["fact_patterns"])
            tas = tone_alignment_score(scenario["tone"], email)
            pess = structure_score(email)
            overall = (fcs + tas + pess) / 3

            rows.append({
                "scenario_id": scenario["id"],
                "strategy": strategy_name,
                "intent": scenario["intent"],
                "tone": scenario["tone"],
                "fact_coverage_score": round(fcs, 3),
                "tone_alignment_score": round(tas, 3),
                "professional_email_structure_score": round(pess, 3),
                "overall_score": round(overall, 3),
                "generated_email": email.replace("\n", "\\n")
            })

    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = {}
    for strategy in sorted(set(r["strategy"] for r in rows)):
        subset = [r for r in rows if r["strategy"] == strategy]
        summary[strategy] = {
            "fact_coverage_score_avg": round(statistics.mean(r["fact_coverage_score"] for r in subset), 3),
            "tone_alignment_score_avg": round(statistics.mean(r["tone_alignment_score"] for r in subset), 3),
            "professional_email_structure_score_avg": round(statistics.mean(r["professional_email_structure_score"] for r in subset), 3),
            "overall_score_avg": round(statistics.mean(r["overall_score"] for r in subset), 3)
        }

    output = {
        "metric_definitions": {
            "fact_coverage_score": "Matched required fact groups divided by total required fact groups.",
            "tone_alignment_score": "LLM judge score for requested tone, normalized from 1-5 to 0-1.",
            "professional_email_structure_score": "Rule-based score for subject, greeting, paragraphing, CTA/closing, sign-off, and length."
        },
        "summary": summary
    }

    with open("results_summary.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("Saved results.csv and results_summary.json")

if __name__ == "__main__":
    main()
