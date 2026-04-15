# 📧 Email Generation Assistant (LLM Project)

## 🚀 Overview
This project builds an AI-powered Email Generation Assistant that generates professional emails from structured inputs:

- **Intent** – purpose of the email  
- **Key Facts** – required information to include  
- **Tone** – writing style (formal, empathetic, etc.)

The system uses **advanced prompt engineering** and a **custom evaluation framework** to ensure high-quality, reliable outputs.

---

## 🧠 Key Features

### ✅ Advanced Prompt Engineering
- Role-based prompting (Executive Assistant persona)
- Few-shot examples for guidance
- Structured output constraints
- Self-verification to ensure fact inclusion

### 📊 Evaluation System
- 10 realistic test scenarios
- Human reference emails
- Custom evaluation metrics

### 🔍 Model Comparison
- Advanced Prompt vs Baseline Prompt
- Quantitative performance comparison using metrics

---

## 📏 Custom Metrics

### 1. Fact Coverage Score (FCS)
Measures how effectively the model includes all required facts.

**Formula:**  
FCS = Matched Facts / Total Facts

---

### 2. Tone Alignment Score (TAS)
Evaluates how well the generated email matches the requested tone.

**Method:**  
LLM-based scoring (1–5 scale, normalized to 0–1)

---

### 3. Professional Email Structure Score (PESS)
Checks adherence to professional email standards:

- Subject line  
- Greeting  
- Clear body  
- Call-to-action  
- Sign-off  
- Appropriate length (80–220 words)

---

## 📈 Results Summary

| Strategy           | FCS  | TAS  | PESS | Overall |
|------------------|------|------|------|--------|
| Advanced Prompt  | High | High | High | ✅ Best |
| Baseline Prompt  | Medium | Medium | Medium | ❌ Lower |

---

## ⚙️ How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
2. Setup Environment

Create a .env file in the root directory:

OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
OPENAI_JUDGE_MODEL=gpt-4.1-mini
▶️ Run the Application
python app.py

You will be prompted to enter:

Intent
Tone
Key facts

The system will generate emails using:

Advanced Prompt Strategy
Baseline Prompt Strategy
📊 Run Evaluation
python evaluate.py

This will generate:

results.csv → raw scores for all scenarios
results_summary.json → average metric scores
🧪 Tech Stack
Python
OpenAI API
Prompt Engineering
LLM Evaluation Framework
🎯 Conclusion

Advanced prompting significantly improves:

Fact inclusion accuracy
Tone consistency
Professional email structure

This demonstrates that combining prompt engineering with evaluation-driven design makes LLM systems more reliable and production-ready.
