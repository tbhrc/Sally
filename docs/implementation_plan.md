# Sally Development Plan

## 1. Vision & Scope
Deliver a self-contained FastAPI application that ingests recruiter-provided CSV or Excel exports, applies configurable knockout and scoring policies, and produces auditable ranked shortlists with transparent rationales. The MVP targets on-premise or single-container deployments for Talent Bridge teams.

## 2. High-Level Architecture
- **API Layer:** FastAPI application exposing REST endpoints for health checks and screening (`GET /`, `POST /screen/csv`, `POST /screen/records`).
- **Ingestion Layer:** File upload handler validating CSV/Excel schemas, applying configurable field mappings (`fieldmap.yml`), and normalizing candidate records.
- **Knockout Engine:** Rule processor loading knockout policies from `policy.yml` and annotating candidates with failure reasons.
- **Scoring Engine:** Weighted scoring module reading `weights.yml`, calculating fit scores (0–100), recommendations, and confidence levels.
- **Rationale Generator:** Template- or LLM-assisted explanation builder summarizing KO reasons and positive signals.
- **Output Layer:** Writers that persist CSV and JSON artifacts with timestamps under `/outputs/` and log run metadata for audit trails.
- **Configuration Layer:** Repository of YAML templates per role, versioned for traceability, with overrides provided via CLI or request payload.
- **Optional Services:** PDF text extraction pipeline (pypdf) and notification integrations (email/Slack) for future releases.

## 3. Milestones & Timeline
1. **Foundations (Week 1)**
   - Scaffold FastAPI project structure and dependency management.
   - Implement health endpoint and configuration loading utilities.
   - Define data models for candidates, KO results, and scoring outputs.
2. **Ingestion & Validation (Week 2)**
   - Build CSV/Excel ingestion with schema mapping and validation.
   - Implement file storage strategy and size safeguards.
   - Provide sample datasets and mapping templates.
3. **Knockout Engine (Week 3)**
   - Parse `policy.yml` into executable rules.
   - Execute KO checks for each policy category with rationale capture.
   - Add unit tests covering edge cases and false-positive prevention.
4. **Scoring Engine (Week 4)**
   - Implement weighted scoring logic and confidence calculation.
   - Produce recommendation tiers (SHORTLIST, MAYBE, REJECT).
   - Generate per-candidate explanations combining KO and positive signals.
5. **Output & Reporting (Week 5)**
   - Write CSV/JSON outputs with metadata headers.
   - Ensure deterministic ordering and rounding conventions.
   - Deliver sample run demonstrating full pipeline.
6. **Deployment & QA (Week 6)**
   - Create Dockerfile and compose configuration.
   - Document setup in README and provide CLI examples.
   - Conduct end-to-end tests and performance benchmarking against sample datasets.

## 4. Workstreams & Owners
- **Backend Engineering:** FastAPI endpoints, KO/scoring modules, integration tests.
- **Data Engineering:** Field mapping logic, CSV/Excel normalization, PDF parsing.
- **Product & QA:** Policy template definition, acceptance criteria, manual verification of sample outputs.
- **DevOps:** Containerization, CI configuration, deployment scripts.

## 5. Technical Backlog
- Implement Pydantic models for candidate inputs and screening responses.
- Add configurable logging with correlation IDs per screening run.
- Support policy versioning and change history.
- Introduce pluggable KO rule definitions (Python callables) for advanced logic.
- Develop scoring weight optimizer script fed by historical hiring outcomes.
- Integrate optional caching for repeated policy evaluations.
- Provide admin CLI for generating new role templates from base config.

## 6. Risks & Mitigations
- **Data Quality Variability:** Mitigate with strict validation, clear error reporting, and editable field maps.
- **Policy Drift:** Enforce versioning of YAML configs and embed policy hash in outputs.
- **Explainability:** Use structured rationale templates and allow recruiter overrides in output CSV.
- **Performance:** Benchmark on large CSVs; optimize pandas operations and consider chunked processing.
- **Security:** Default to local storage; document procedures for handling personally identifiable information (PII).

## 7. Testing Strategy
- **Unit Tests:** KO rules, scoring calculations, configuration parsing.
- **Integration Tests:** End-to-end pipeline with sample dataset.
- **Regression Tests:** Baseline outputs snapshot to detect scoring drift.
- **Performance Tests:** Large dataset ingestion and processing time targets.
- **User Acceptance:** Recruiter walkthrough using Talent Bridge policies.

## 8. Documentation & Handover
- Maintain comprehensive README with setup, configuration, and troubleshooting.
- Document policy and weight schema formats with examples.
- Provide onboarding guide for creating new role templates and interpreting outputs.
- Capture known limitations and future roadmap alignment with PRD.

## 9. Future Enhancements
- LLM summarization of candidate achievements and rationale narratives.
- ATS integrations (e.g., Manatal API connector) for automated ingestion.
- Web dashboard for run management, overrides, and reporting.
- Role-based access control and audit log exports.
- Multilingual output support (English and Arabic) with localization files.
