# Day 01 — LLM Basics

## 🔹 What is an LLM?
Large Language Models generate text based on patterns learned from data.

## 🔹 What I learned today
- How to call an LLM using OpenAI API
- Structure of messages:
  - system → behavior
  - user → input
  - assistant → output
- Model used: gpt-4o-mini

## 🔹 Basic Code Flow
1. Take user input
2. Send to LLM
3. Get response
4. Print output

## 🔹 Example

Input:
"What is Python?"

Output:
"Python is a programming language..."

## 🔹 Key Concepts

### 1. Messages format
[
  {"role": "user", "content": "..."}
]

### 2. Temperature
- controls randomness
- low → more accurate
- high → more creative

## 🔹 My Understanding
LLM does not "know" facts, it predicts the next word based on probability.

## 🔹 Questions I still have
- How does memory work?
- How does RAG improve this?