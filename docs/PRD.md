# Sally – AI Screening & Qualification Assistant

## Document Control
- **Version:** 1.0 (Standalone Release)
- **Owner:** Talent Bridge HR Consultancy
- **Prepared by:** iMPLEMENTAi.ae
- **Date:** 24 October 2025

---

## 1. Product Overview
Sally is an intelligent CV-screening and candidate-qualification system built for Talent Bridge. It automates filtering, ranking, and explaining candidate suitability without relying on external applicant tracking systems (ATS). The system uses knockout rules, weighted scoring, and transparent rationales, running as a small FastAPI or Docker app. Recruiters simply upload a CSV or Excel export, and Sally returns a ranked shortlist.

## 2. Product Mission
Eliminate inconsistent, manual CV screening by giving recruiters an explainable, fast, and auditable AI-driven process that runs locally or in the cloud.

## 3. Core Objectives
1. **Speed:** Cut recruiter screening time by 70%.
2. **Accuracy:** Raise shortlist accuracy to ≥ 90%.
3. **Transparency:** Every accept/reject includes visible rationale.
4. **Scalability:** Works with any CSV export—no ATS dependency.
5. **Auditability:** Every run produces versioned, timestamped output.

## 4. How Sally Works
1. Recruiter uploads CSV or Excel (optional linked CV PDFs).
2. Sally maps fields (location, visa, salary, notice, languages, etc.).
3. The knockout engine filters out unqualified candidates.
4. Remaining candidates are scored 0–100 via a weighted model.
5. Output: `screened_results.csv` with Fit Score, Recommendation (SHORTLIST / MAYBE / REJECT), KO Reasons, Rationale, and Confidence.
6. Recruiter can review, override, and adjust policy templates.

## 5. Key Features
### A. Input & Data
- Accepts CSV or Excel from any system.
- Optional PDF text extraction.
- Configurable field mapping (`fieldmap.yml`).

### B. Knockout Policy Engine
Editable `policy.yml` covering:
- Location / Relocation
- Visa Status
- Notice Period
- Salary Band (+ flex%)
- Nationality (optional)
- Languages (CEFR levels)
- Must-Have Tools / Certs
- Education
- Industry Exposure
- Shift / Travel Rules

### C. Scoring Engine
Weighted model (`weights.yml`) measuring:
- Experience
- Tools & Stack
- Industry alignment
- Language skill
- Education / Cert
- Achievements

Outputs Fit Score 0–100 plus Confidence 0–1.

### D. Output & Reporting
- CSV in `/outputs/`.
- Flags KO'd candidates.
- JSON output for integration.

### E. Configurability
- Edit YAML configs for policies, weights, mappings.
- Maintain per-role templates (Finance, Sales, etc.).

### F. Deployment & Access
- Local `uvicorn` run or Docker container.
- REST API:
  - `GET /` health
  - `POST /screen/csv` upload
  - `POST /screen/records` JSON

### G. Extensibility
- Add LLM summariser (achievements, rationale).
- Optional ATS connectors (e.g., Manatal).
- Web dashboard UI.
- Slack / email summaries.

## 6. Technical Summary
| Component | Tech | Purpose |
|-----------|------|---------|
| Backend | Python 3.11 + FastAPI | Core service |
| Data | pandas + PyYAML | I/O + config |
| Config | YAML files | KO rules / weights |
| KO Logic | `ko_policy.py` | Filters |
| Scoring | `scorer.py` | Weighted fit |
| PDF Parser | pypdf | CV text |
| Deployment | Docker / Railway / Render | Hosting |
| Output | CSV + JSON | Reports |

## 7. Success Metrics
| Metric | Target |
|--------|--------|
| Speed gain | ≥ 70% faster |
| Accuracy vs senior recruiter | ≥ 90% |
| False KO rate | ≤ 5% |
| Recruiter satisfaction | ≥ 8 / 10 |
| Cost per CV | ≤ AED 0.75 |

## 8. Non-Functional Requirements
- **Privacy:** Local-first, no external data calls.
- **Auditability:** Timestamp and policy version in every run.
- **Transparency:** Explainable rules and rationales.
- **Extensibility:** Modular architecture.
- **Portability:** Single Docker image, no external DB.

## 9. Deliverables (MVP)
1. FastAPI app (local and containerized).
2. Default Talent Bridge policy pack and weights.
3. Configurable field mapping.
4. Full input → KO → Score → Output pipeline.
5. README setup guide.
6. Sample dataset and result file.

## 10. Future Roadmap
- OpenAI integration for advanced analysis.
- ATS connectors (Manatal API).
- Web dashboard UI.
- Authentication / RBAC.
- Multilingual reporting (English and Arabic).
