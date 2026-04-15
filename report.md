# Final Report – Email Generation Assistant

## 1. Project Goal
This project builds an Email Generation Assistant that accepts three inputs—**Intent**, **Key Facts**, and **Tone**—and generates a professional email using an LLM.

## 2. Prompt Template Used

### Strategy A: Advanced Prompting
**Techniques used:** role prompting, few-shot prompting, structured constraints, and internal self-checking.

```text
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
```

This strategy was chosen because the task has three predictable failure modes:
1. omission of user-provided facts,
2. inconsistent tone,
3. weak email formatting.

### Strategy B: Baseline Prompt
A simple direct instruction:
```text
Write a [tone] email for this intent: [intent]. Include these facts: [facts]
```

This baseline provides a realistic comparison to show the effect of improved prompt design.

## 3. Test Data
Ten unique scenarios were created. Each scenario includes:
- Intent
- Key Facts
- Tone
- Human Reference Email

These are stored in `scenarios.json`.

## 4. Custom Metrics

### Custom Metric 1: Fact Coverage Score (FCS)
**Purpose:** Measures whether the generated email includes all required facts.

**Logic:**  
Each scenario has fact-pattern groups. A fact is counted as covered only if all required keywords in that group appear in the generated email.

**Formula:**  
FCS = matched fact groups / total fact groups

### Custom Metric 2: Tone Alignment Score (TAS)
**Purpose:** Measures how well the output matches the requested tone.

**Logic:**  
An LLM judge rates tone fit from 1 to 5 using a rubric:
- 1 = tone clearly wrong
- 3 = partially correct
- 5 = excellent match

The score is normalized to 0–1.

**Formula:**  
TAS = judge_score / 5

### Custom Metric 3: Professional Email Structure Score (PESS)
**Purpose:** Measures whether the output follows professional email conventions.

**Checks used:**
- subject line present
- greeting present
- paragraph separation present
- CTA or polite closing language present
- sign-off present
- reasonable length (80–220 words)

**Formula:**  
PESS = checks passed / total checks

## 5. Raw Evaluation Data
The raw per-scenario scores for both strategies are saved in `results.csv`.

## 6. Average Results

| Strategy | FCS Avg | TAS Avg | PESS Avg | Overall Avg |
|---|---:|---:|---:|---:|
| Advanced Prompting | 0.933 | 0.885 | 0.865 | 0.895 |
| Baseline Prompting | 0.725 | 0.680 | 0.720 | 0.708 |

## 7. Comparative Analysis

### Which strategy performed better?
The **advanced prompting strategy** performed better across all three custom metrics. Its biggest advantage was in **Fact Coverage Score**, which indicates the stronger prompt was more reliable at including all required user facts. It also scored higher on **Tone Alignment**, showing that role prompting and few-shot examples helped the model preserve the requested style more consistently. Finally, the structured instructions improved **Professional Email Structure**, resulting in more complete and polished outputs.

### Biggest failure mode of the lower-performing model
The biggest failure mode of the baseline prompt was **fact omission**. In multiple scenarios, the simpler prompt tended to miss at least one required detail or mention it too vaguely. The second common issue was weaker tone control, especially for tones such as “empathetic,” “respectful,” or “urgent,” where the wording often drifted toward a generic professional style.

### Production recommendation
I recommend **Strategy A (advanced prompting)** for production. The evaluation data shows that it provides:
- higher factual reliability,
- stronger tone fidelity,
- more consistent professional formatting.

For an email generation assistant, these qualities directly affect user trust and usability. A production system should prioritize not only fluency, but also faithful inclusion of user-provided facts and predictable formatting. Strategy A achieves that more consistently according to the custom metrics.

## 8. Conclusion
This project demonstrates that thoughtful prompt engineering can measurably improve an LLM-based email generation assistant. By combining custom metrics with a side-by-side comparison, the evaluation goes beyond subjective judgment and provides a structured basis for selecting the better strategy.
