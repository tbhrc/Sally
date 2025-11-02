from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

import pandas as pd


@dataclass
class ScreeningSummary:
    total_candidates: int
    passed: int
    failed: int
    average_score: float


def evaluate_candidates(
    candidates_df: pd.DataFrame,
    resume_texts: Dict[str, str],
    job_description: str,
    required_keywords: Iterable[str],
    min_years_experience: float,
) -> List[Dict[str, object]]:
    keyword_set = {kw.lower() for kw in required_keywords}

    results: List[Dict[str, object]] = []
    for _, row in candidates_df.iterrows():
        resume_filename = row["resume_filename"]
        resume_text = resume_texts.get(resume_filename, "")
        normalized_resume = resume_text.lower()

        reasons: List[str] = []
        passed = True

        years_experience = float(row.get("years_experience", 0))
        if years_experience < min_years_experience:
            passed = False
            reasons.append(
                f"Years of experience {years_experience} is below minimum {min_years_experience}"
            )

        if keyword_set:
            missing_keywords = [kw for kw in keyword_set if kw not in normalized_resume]
            if missing_keywords:
                passed = False
                reasons.append("Missing required keywords: " + ", ".join(missing_keywords))

        # Simple scoring model: base on keyword matches, experience delta, JD similarity placeholder
        keyword_score = _keyword_score(keyword_set, normalized_resume)
        experience_score = _experience_score(years_experience, min_years_experience)
        jd_score = _jd_score(job_description, resume_text)
        total_score = round(keyword_score * 0.4 + experience_score * 0.4 + jd_score * 0.2, 2)

        results.append(
            {
                "candidate_id": row["candidate_id"],
                "full_name": row["full_name"],
                "email": row["email"],
                "resume_filename": resume_filename,
                "passed": passed,
                "score": total_score,
                "reasons": " | ".join(reasons) if reasons else "",
            }
        )

    return results


def summarize_results(results: List[Dict[str, object]]) -> ScreeningSummary:
    total = len(results)
    passed = sum(1 for result in results if result["passed"])
    failed = total - passed
    average_score = round(sum(result["score"] for result in results) / total, 2) if total else 0.0
    return ScreeningSummary(total_candidates=total, passed=passed, failed=failed, average_score=average_score)


def _keyword_score(keyword_set: Iterable[str], resume_text: str) -> float:
    if not keyword_set:
        return 100.0
    present = sum(1 for kw in keyword_set if kw in resume_text)
    return (present / len(keyword_set)) * 100


def _experience_score(years_experience: float, min_years_experience: float) -> float:
    if min_years_experience <= 0:
        return 100.0
    ratio = years_experience / max(min_years_experience, 1e-6)
    capped = min(ratio, 2.0)  # cap at 200%
    return capped / 2.0 * 100


def _jd_score(job_description: str, resume_text: str) -> float:
    if not job_description.strip():
        return 100.0
    jd_keywords = {token.lower() for token in job_description.split() if len(token) > 3}
    if not jd_keywords:
        return 100.0
    resume_tokens = resume_text.lower().split()
    overlap = sum(1 for token in resume_tokens if token in jd_keywords)
    return min(overlap / max(len(resume_tokens), 1), 1.0) * 100
