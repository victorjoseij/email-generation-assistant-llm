# 📧 Email Generation Assistant (LLM Project)

## 🚀 Overview
This project builds an AI-powered Email Generation Assistant that creates professional emails based on:

- Intent
- Key Facts
- Tone

It uses advanced prompt engineering and a custom evaluation framework to measure output quality.

---

## 🧠 Key Features

✅ Advanced Prompt Engineering  
- Role-based prompting  
- Few-shot examples  
- Structured output constraints  
- Self-verification step  

✅ Evaluation System  
- 10 real-world scenarios  
- Human reference emails  
- 3 custom evaluation metrics  

✅ Model Comparison  
- Advanced Prompt vs Baseline Prompt  
- Quantitative performance comparison  

---

## 📊 Custom Metrics

### 1. Fact Coverage Score (FCS)
Measures how well the model includes required facts.

### 2. Tone Alignment Score (TAS)
LLM-based scoring of tone correctness.

### 3. Professional Email Structure Score (PESS)
Checks formatting: subject, greeting, CTA, sign-off, etc.

---

## 📈 Results Summary

| Strategy | FCS | TAS | PESS | Overall |
|----------|-----|-----|------|--------|
| Advanced Prompt | High | High | High | ✅ Best |
| Baseline Prompt | Medium | Medium | Medium | ❌ Lower |

---

## ⚙️ How to Run

```bash
pip install -r requirements.txt
cp .env.example .env
