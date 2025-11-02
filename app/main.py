from __future__ import annotations

import io
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from .services import resume_parser, screening

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Sally Screening Webapp", version="0.1.0")

templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/screen", response_class=HTMLResponse)
async def screen_candidates(
    request: Request,
    candidate_sheet: UploadFile = File(...),
    resumes: List[UploadFile] = File(...),
    job_description: str = Form(...),
    required_keywords: str = Form(""),
    min_experience: float = Form(0.0),
) -> HTMLResponse:
    if not candidate_sheet.filename:
        raise HTTPException(status_code=400, detail="Candidate sheet is required")

    try:
        candidates_df = await _load_candidate_sheet(candidate_sheet)
    except ValueError as exc:  # pragma: no cover - defensive guard
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    resume_texts = await _load_resumes(resumes)

    keyword_list = [kw.strip() for kw in required_keywords.split(",") if kw.strip()]

    results = screening.evaluate_candidates(
        candidates_df=candidates_df,
        resume_texts=resume_texts,
        job_description=job_description,
        required_keywords=keyword_list,
        min_years_experience=min_experience,
    )

    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    base_name = f"screening-results-{timestamp}"
    csv_path = OUTPUT_DIR / f"{base_name}.csv"
    excel_path = OUTPUT_DIR / f"{base_name}.xlsx"

    results_df = pd.DataFrame(results)
    results_df.to_csv(csv_path, index=False)
    results_df.to_excel(excel_path, index=False)

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "results": results,
            "csv_filename": csv_path.name,
            "excel_filename": excel_path.name,
            "summary": screening.summarize_results(results),
        },
    )


@app.get("/download/{filename}")
async def download_file(filename: str) -> FileResponse:
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename=filename)


async def _load_candidate_sheet(upload: UploadFile) -> pd.DataFrame:
    suffix = Path(upload.filename).suffix.lower()
    content = await upload.read()
    if suffix == ".csv":
        buffer = io.StringIO(content.decode("utf-8"))
        df = pd.read_csv(buffer)
    elif suffix in {".xls", ".xlsx"}:
        buffer = io.BytesIO(content)
        df = pd.read_excel(buffer)
    else:
        raise ValueError("Candidate sheet must be a CSV or Excel file")

    required_columns = {"candidate_id", "full_name", "email", "years_experience", "resume_filename"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        raise ValueError(
            "Candidate sheet missing required columns: " + ", ".join(sorted(missing_columns))
        )
    return df


async def _load_resumes(resume_files: List[UploadFile]) -> Dict[str, str]:
    resume_texts: Dict[str, str] = {}
    for file in resume_files:
        if not file.filename:
            continue
        content = await file.read()
        text = resume_parser.extract_text(file.filename, content)
        resume_texts[file.filename] = text
    return resume_texts
