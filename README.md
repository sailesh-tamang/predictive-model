# EPL Crowd Impact — Full Stack Thesis Project

This repository contains the existing thesis research files and the deployed web-application workflow:

- `model.py` — binary research model for `home_win` (Home Win vs No Home Win) as a research/comparison task.
- `backend/model/save_model.py` — production multiclass model for `FTR` (Home / Draw / Away) used by the Flask app.
- `backend/` — Flask backend, trained model artifacts and API endpoints.
- `frontend/` — React + Vite frontend that consumes the production multiclass prediction API.

Important distinction:

- Binary research model: target `home_win`, used for exploratory comparisons and crowd-impact analysis.
- Production web model: target `FTR`, used for the deployed Home/Draw/Away prediction interface.

The two tasks are separate and should not be mixed when reporting results.

Next steps:
1. Create a Python virtualenv and install backend requirements (see `backend/README.md`).
2. Run `python backend/model/save_model.py` to train and save the production model and metrics.
3. Start backend: `python backend/app.py`.
4. Start frontend: `cd frontend && npm install && npm run dev`.
