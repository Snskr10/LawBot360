# LawBot 360

LawBot 360 is an AI-powered legal contract and compliance assistant designed for Indian law (extensible to other jurisdictions). It drafts contracts, verifies legal documents for risks, checks financial/statutory compliance, retrieves legal knowledge, and supports secure e-signatures with audit trails.

## Features
- Natural-language contract generation with templates (NDA, Employment, Service, etc.)
- Document verification: mandatory clauses, risk scoring, hedge/vague language detection
- Compliance checker covering GST, TDS, Companies Act, MSME, IT Act/DPDP
- Knowledge retrieval via FAISS/ChromaDB-backed embeddings
- Plain-language clause explanations with RAG context
- OCR pipeline for scanned PDFs (Tesseract/EasyOCR)
- Mock DocuSign-style e-signature flow with audit logging
- Multilingual (English/Hindi) UI toggle and voice pipeline hooks
- Dashboard analytics with risk trends, missing clause frequency, compliance metrics

## Tech Stack
- Backend: Flask, SQLAlchemy, Pydantic
- Frontend: Jinja2 templates, Bootstrap 5, vanilla JS
- Embeddings & RAG: sentence-transformers, ChromaDB/FAISS
- NLP/LLM: OpenAI API (pluggable), Whisper (voice), EasyOCR/Tesseract (OCR)
- Storage: SQLite/Postgres (configurable), file system for uploads/exports

## Project Structure
```
LawBot360/
├── app.py
├── config.py
├── requirements.txt
├── routers/
├── services/
├── models/
├── templates/
├── static/
├── data/
│   ├── laws/
│   ├── templates/
│   ├── uploads/
│   ├── exports/
│   └── vector_store/
├── scripts/
└── tests/
```

## Getting Started
1. **Clone & Install**
   ```powershell
   git clone <repo-url>
   cd LawBot360
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. **Environment Variables**
   - Copy `.env.example` to `.env` and update keys (OpenAI, DocuSign sandbox, etc.)
3. **Database Setup**
   - Default SQLite auto-initializes via `db.create_all()` on first run
   - For Postgres, set `DATABASE_URL` and run migrations (future Alembic)
4. **Run the App**
   ```powershell
   flask --app app.py run
   ```
5. **Optional Services**
   - Install Tesseract CLI for OCR accuracy
   - Configure Whisper/voice endpoints if voice Q&A is needed

## Law Corpus Ingestion
1. Maintain `data/laws/sources.json` with one entry per statute, pointing to the API endpoint you are licensed to consume (see sample placeholders in the repo).
2. Provide credentials through environment variables:
   - `LAW_API_BASE` (optional): base URL prepended to relative endpoints
   - `LAW_API_KEY`, `LAW_API_KEY_HEADER`, `LAW_API_KEY_SCHEME`: authentication details if the API requires them
3. Pull the latest sections into CSVs:
   ```powershell
   python scripts/ingest_laws.py                # fetch all configured acts
   python scripts/ingest_laws.py --source it_act_2000  # fetch a specific act
   ```
4. Rebuild embeddings after ingestion so RAG responses pick up the new content:
   ```powershell
   python scripts/reindex_vector_store.py
   ```
5. Each CSV is written into `data/laws/<source_id>.csv` and is immediately available to the verifier and explainer modules once reindexed.

## Testing
- Unit tests planned under `tests/`
- Roadmap includes golden file tests for templates and fuzz tests for uploads

## Roadmap
- **Phase 1 (MVP):** contract generation, verification, basic RAG, PDF export, deterministic risk scoring
- **Phase 2:** Compliance checker, dashboard, clause library, OCR polishing
- **Phase 3:** DocuSign sandbox integration, audit trail diff view, voice features, multi-jurisdiction profiles
- **Phase 4:** Security hardening, external DMS integrations, optional blockchain timestamping

## Disclaimer
All outputs are educational drafting aids, not legal advice. Users must seek professional legal counsel for final review.
