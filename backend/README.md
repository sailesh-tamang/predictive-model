# Backend (Flask)

This backend contains the production prediction API for the multiclass model trained on `FTR`.
The binary `home_win` research model remains in the root project scripts and is not the deployed app model.

Instructions:

1. Create a Python virtual environment and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Train and save the production model artifacts (this uses your existing `EPL_cleaned.csv` at repository root):

```bash
python model/save_model.py
```

3. Run the Flask API locally:

```bash
python app.py
```

4. The API endpoint will be at `http://localhost:5000/api/predict` and accepts JSON payloads with the features defined in `backend/model/features.json`.

Deployment (Render): Use gunicorn to serve `app:create_app()`.
