# Sally Candidate Screening Webapp

Sally is a FastAPI-powered web application that screens candidate resumes against
role-specific knockout criteria. Recruiters upload a candidate spreadsheet,
resume documents, and screening preferences to generate pass/fail outcomes and
scored leaderboards exportable as CSV or Excel files.

## Features

- Upload CSV or Excel spreadsheets with candidate metadata.
- Attach matching PDF/DOCX resumes for contextual evaluation.
- Configure required keywords and minimum years of experience per run.
- Generate timestamped CSV and Excel outputs with pass/fail rationale.
- Render an in-browser summary for quick triage.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Navigate to <http://localhost:8000> and follow the on-screen instructions.

## Deployment Notes

- Works with container platforms (Docker, Azure App Service for Containers) or
  directly on Azure App Service using `requirements.txt`.
- Outputs are stored under the `outputs/` directory; mount this to persistent
  storage or sync to OneDrive/SharePoint for collaboration.
- Add authentication (Azure AD, OAuth) before exposing to the internet.

## Documentation

Detailed architecture and operational notes live in
[`docs/webapp_overview.md`](docs/webapp_overview.md).
