# Literacy Resource Hub

A hub for literacy resources, with a Python API backend and a web frontend.

## Structure

- `backend/` — FastAPI API (Python)
- `frontend/` — React/Next.js client
- `docs/` — architecture notes and meeting notes

## Backend

```bash
cd backend
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Docs

See [docs/architecture.md](docs/architecture.md) for a high-level overview and [docs/meeting-notes/](docs/meeting-notes/) for notes from project meetings.
