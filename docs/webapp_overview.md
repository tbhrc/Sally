# Sally Screening Web Application

This document explains the structure, design decisions, and usage of the FastAPI web
application that powers the Sally candidate screening workflow.

## Goals

* Support recruiters who want a lightweight, Microsoft-friendly solution without
  managing backend infrastructure.
* Accept requisition packages consisting of a candidate spreadsheet, individual
  resume documents, and textual screening guidance.
* Produce auditable CSV and Excel outputs that can be synced to OneDrive or
  shared via Microsoft 365 tools.

## Tech Stack

| Layer | Choice | Rationale |
| --- | --- | --- |
| Web Framework | **FastAPI** | Modern, async-friendly, excellent request validation, easy to deploy on Azure App Service or container platforms. |
| UI | **Jinja2 + Pico.css** | Keeps the interface server-rendered (no complex frontend build). |
| Data Processing | **pandas** | Reliable CSV/Excel parsing, flexible data wrangling. |
| Resume Extraction | **pdfplumber**, **python-docx** | Pure-Python libraries that work in containerized environments. |
| Packaging | `requirements.txt` | Enables deployment to Azure Web Apps, App Service, or container builds. |

## Repository Layout

```
app/
├── main.py                 # FastAPI application and routing
├── services/
│   ├── __init__.py
│   ├── resume_parser.py    # Extracts text from PDF/DOCX resumes
│   └── screening.py        # Business logic for knockouts and scoring
└── templates/
    ├── index.html          # Upload form and instructions
    └── results.html        # Summary and downloadable outputs
outputs/                    # Generated CSV/Excel artifacts
```

## Workflow

1. Recruiter visits `/` and uploads the candidate sheet (CSV/XLSX), resumes, job
   description, and screening thresholds.
2. `main.py` validates the spreadsheet columns, normalizes keywords, and loads
   resumes through `resume_parser.extract_text`.
3. `screening.evaluate_candidates` applies knockout rules (minimum years of
   experience, required keywords) and computes heuristic scores combining keyword
   coverage, experience, and job description overlap.
4. Results are persisted into timestamped CSV and Excel files under `outputs/`.
5. The `results.html` page renders a pass/fail table and exposes download links.

## Candidate Sheet Schema

The upload must contain the following columns:

* `candidate_id`
* `full_name`
* `email`
* `years_experience`
* `resume_filename`

The `resume_filename` column must match the uploaded resume's filename (including
extension). Additional columns are ignored but preserved in the exported
artifacts by pandas.

## Running Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open <http://localhost:8000> to access the interface.

## Extensibility Notes

* **Custom Criteria** – Extend `screening.evaluate_candidates` with additional
  checks (e.g., certifications, locations) by appending to the `reasons` list.
* **Integrations** – Sync the generated artifacts to OneDrive/SharePoint via
  Microsoft Graph or run the app inside Azure Container Apps for low-ops
  hosting.
* **Security** – Add Azure AD authentication by wiring a middleware such as
  `msal` or enabling App Service authentication for enterprise environments.
* **Observability** – Plug in structured logging (e.g., `structlog`) or
  Application Insights for auditing and monitoring.

## Known Limitations

* Resume parsing focuses on text extraction; semantic scoring can be swapped for
  Azure OpenAI or another ML model in future iterations.
* The job description similarity metric is token overlap; this is intentionally
  simple for MVP but can be replaced with embeddings.
* Large resume batches may increase response times; move heavy processing to a
  background task queue (Celery, Azure Functions) when scaling beyond 50 files.
