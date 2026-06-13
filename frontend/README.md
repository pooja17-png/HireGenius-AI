# HireGenius AI — Frontend

An interactive, market-style React + Vite frontend for the **HireGenius AI** FastAPI
backend. Upload a resume PDF and get a live ATS score, detected skills, skill-gap
analysis, and a job-description match calculator.

## Stack
- **React 18** + **Vite 6** (plain `npm`, no extra framework)
- Talks to the FastAPI backend via a dev proxy (`/api` → `http://127.0.0.1:8000`)

## Run it

### 1. Start the backend (from the repo root, one level up)
```bash
# Windows PowerShell
..\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```
The API serves at http://127.0.0.1:8000 (Swagger docs at `/docs`).

### 2. Start the frontend
```bash
cd frontend
npm install      # first time only
npm run dev
```
Open the printed URL (default **http://localhost:5173**).

## How it integrates with the backend
| UI feature            | Source |
|-----------------------|--------|
| Resume upload, text extraction, skills, ATS score, skill gap | **Backend** `POST /upload_resume` |
| Job-description match | **Client-side** keyword match over the backend's extracted skills (the backend has no JD route yet — see `src/api.js → matchAgainstJD`) |
| API online/offline badge | **Backend** `GET /` health check |

The proxy is configured in `vite.config.js`. In production, build with `npm run build`
and serve `dist/` behind the same origin as the API (or set `BASE` in `src/api.js`).

## Project layout
```
frontend/
├─ index.html
├─ vite.config.js          # /api proxy → FastAPI
├─ src/
│  ├─ api.js               # backend client + client-side JD matcher
│  ├─ App.jsx              # nav, hero, features, analyze flow
│  ├─ styles.css           # dark, glassy, animated theme
│  └─ components/
│     ├─ Uploader.jsx      # drag-and-drop PDF uploader
│     ├─ ScoreRing.jsx     # animated ATS score ring
│     └─ Results.jsx       # skills, gap, JD match, extracted text
```
