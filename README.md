# EPL Crowd Impact — Full Stack Thesis Project

This repository contains your existing thesis research files and a new production-ready web app scaffold:

- `existing_research_files/` — (placeholder) reference to your original research files (left untouched in root).
- `backend/` — Flask backend, model training script and API endpoints.
- `frontend/` — React + Vite + Tailwind frontend scaffold.

Important: I did not modify your original research files. They remain at repository root (e.g., `model.py`, `EPL_cleaned.csv`, analysis scripts and PNGs`).

Next steps:
1. Create a Python virtualenv and install backend requirements (see `backend/README.md`).
2. Run `python backend/model/save_model.py` to train and save `model.pkl` (requires `EPL_cleaned.csv`).
3. Start backend: `python backend/app.py`.
4. Start frontend: `cd frontend && npm install && npm run dev`.
