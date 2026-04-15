# Email Generation Assistant

This project implements a prototype **Email Generation Assistant** that generates professional emails from three inputs:

- **Intent**
- **Key Facts**
- **Tone**

It also evaluates generation quality with **three custom metrics** tailored to this task and compares two prompting strategies:

- **Model A / Strategy A**: Advanced prompt with role prompting + structured constraints + few-shot examples
- **Model B / Strategy B**: Simple direct prompt baseline

## Project Structure

- `app.py` – main email generation prototype
- `evaluate.py` – evaluation pipeline for 10 scenarios
- `scenarios.json` – 10 test scenarios and human reference emails
- `results.csv` – raw metric output for all scenarios and both strategies
- `results_summary.json` – metric averages and comparison summary
- `report.md` – final report content
- `.env.example` – environment variables

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt
cp .env.example .env
```

Add your API key in `.env`:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
OPENAI_JUDGE_MODEL=gpt-4.1-mini
```

## Run the prototype

```bash
python app.py
```

You will be prompted for:
- Intent
- Key facts
- Tone

The script will generate:
- Strategy A email
- Strategy B email

## Run evaluation

```bash
python evaluate.py
```

Outputs:
- `results.csv`
- `results_summary.json`

## Advanced Prompting Technique Used

Strategy A combines:
1. **Role prompting** – the model acts as a senior executive communications assistant.
2. **Structured instructions** – explicit output rules for subject, greeting, body, CTA, and sign-off.
3. **Few-shot prompting** – examples demonstrating how facts and tone should be incorporated.
4. **Self-check instruction** – the model is told to verify that all user facts appear naturally in the email before finalizing.

This is more reliable than a plain “write an email” prompt because it reduces omission of facts and improves tone consistency.

## Custom Metrics

### 1. Fact Coverage Score (FCS)
Measures how many required key facts from the scenario appear in the generated email.

**Logic**:
- Each scenario contains required facts and keyword patterns for each fact.
- Score = matched facts / total required facts

### 2. Tone Alignment Score (TAS)
Measures whether the generated email matches the requested tone.

**Logic**:
- An LLM judge scores tone fit from 1 to 5 using a strict rubric.
- Final normalized score = score / 5

### 3. Professional Email Structure Score (PESS)
Measures whether the output looks like a professional email.

**Logic**:
Rule-based score using:
- greeting present
- clear opening purpose
- body with facts
- closing / CTA
- sign-off present
- reasonable length (80–220 words)

Score = earned checks / total checks

## Recommendation

Based on evaluation, the advanced prompting strategy should typically perform better in:
- fact retention
- tone consistency
- professional formatting

Use Strategy A in production.
