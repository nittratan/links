You are a Senior Staff AI Engineer and System Design Expert.

You have access to a production-level code repository of an AI-powered healthcare claims system (FastAPI + LLM + Rule Engine + Redis + DocumentDB).

Your task is to analyze the entire repository and generate a complete, interview-ready explanation of the system.

---

### 🎯 Output Requirements:

Explain the system in a structured, clear, and senior-level manner as if I am explaining it in an AI Engineer interview.

---

## 1. High-Level Overview

* What problem this system solves (business + technical)
* Why this system is needed

---

## 2. End-to-End Architecture Flow

* Start from entry point (API request)
* Explain step-by-step flow till response
* Include all major components:

  * FastAPI
  * Trigger/Orchestration layer
  * Redis cache
  * Data sources (Facets, EDP, Blue2, Digital APIs)
  * Rule-based pipeline
  * LLM pipeline
  * DocumentDB

---

## 3. Detailed Component Breakdown

### API Layer

* How FastAPI is structured
* Request validation (Pydantic)
* Async handling

### Orchestration Layer

* trigger.py logic
* Strategy Pattern (GBD vs CSBD)
* Pipeline flow

### Caching Layer (Redis)

* What is cached
* Cache key design
* Cache hit/miss flow

### Data Layer

* External API integrations
* Async calls
* Data transformation into models

---

## 4. Rule-Based System (VERY IMPORTANT)

* How query mapping works (YAML → dictionary)
* Exact match lookup logic
* Field extraction process
* Why rule-based is used (cost, latency, accuracy)

---

## 5. LLM Integration

* When LLM is used
* Prompt structure (system + context + query)
* How context is selected (not full data)
* Parameters used (temperature, tokens, etc.)
* How hallucination is controlled

---

## 6. Routing Logic (Critical)

* How system decides:

  * Rule-based vs LLM
* Keyword filtering
* Fallback logic

---

## 7. Data Flow (Step-by-Step)

* From request → data fetch → processing → response
* Include both:

  * Rule-based flow
  * LLM flow

---

## 8. Response Generation

* How final response is structured
* Follow-up question generation
* Formatting logic

---

## 9. Database & Storage

* DocumentDB usage (logs, configs)
* Redis usage
* Data models

---

## 10. Performance Optimization

* Async calls
* Caching
* Avoiding unnecessary LLM calls

---

## 11. Security & Compliance

* PII masking
* Encryption
* Secrets management

---

## 12. Design Patterns Used

* Strategy Pattern
* Template Method
* Factory Pattern
* Repository Pattern

Explain where and why each is used.

---

## 13. Trade-offs & Design Decisions

* Why hybrid (rule + LLM)?
* Why NoSQL?
* Why not embeddings (if not used)?

---

## 14. Limitations & Improvements

* Current system limitations
* What can be improved (vector DB, better routing, etc.)

---

## 15. Interview Summary (IMPORTANT)

* Give a 1-minute explanation
* Give a 3-minute explanation
* Give key "killer lines" to impress interviewer

---

### ⚡ Important Instructions:

* Keep explanation structured and clear
* Avoid code-level details unless necessary
* Focus on system design, reasoning, and trade-offs
* Make it sound like a senior AI engineer explaining

---

Now analyze the repository and generate the complete explanation.
