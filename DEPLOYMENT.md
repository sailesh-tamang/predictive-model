# Deployment Guide — EPL Crowd Impact Web Application

Complete instructions for deploying the thesis project to production on Render (backend) and Vercel (frontend).

---

## Table of Contents
1. [Local Development](#local-development)
2. [Production Deployment](#production-deployment)
3. [Architecture Overview](#architecture-overview)
4. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites
- Python 3.10+ (with pip)
- Node.js 16+ (with npm)
- Git

### Backend Setup

1. **Navigate to backend folder:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment:**
   - **Windows (PowerShell):**
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Train and save the model:**
   ```bash
   python model/save_model.py
   ```
   This generates:
   - `model/xgb_model.pkl` — Trained XGBoost classifier
   - `model/scaler.pkl` — Feature scaler
   - `model/features.json` — Feature names list
   - `model/labels.json` — Label mappings (H/D/A ↔ 0/1/2)

6. **Start backend server:**
   ```bash
   python app.py
   ```
   Server runs on `http://127.0.0.1:5000`

### Frontend Setup

1. **Navigate to frontend folder:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   Frontend runs on `http://localhost:5173`

4. **Build for production:**
   ```bash
   npm run build
   ```
   Output: `frontend/dist/` directory

### Verify Setup

- Navigate to `http://localhost:5173/`
- Enter match statistics and click **Predict Match**
- Verify:
  - ✓ Prediction displays with H/D/A label
  - ✓ Probability bars show for all 3 outcomes
  - ✓ SHAP contributions table displays
  - ✓ SHAP matplotlib plot loads
  - ✓ PNG download link works

---

## Production Deployment

### Backend Deployment (Render)

#### Step 1: Prepare Backend for Production

1. **Update `backend/requirements.txt` if needed:**
   ```
   Flask==3.1.3
   Flask-CORS==6.0.2
   XGBoost==3.2.0
   SHAP==0.51.0
   scikit-learn==1.8.0
   pandas==3.0.2
   numpy==2.4.4
   matplotlib==3.10.9
   joblib==1.5.3
   Gunicorn==25.3.0
   ```

2. **Create `backend/Procfile` (if not present):**
   ```
   web: gunicorn app:app
   ```

3. **Ensure `backend/app.py` uses environment variables:**
   ```python
   import os
   
   app = Flask(__name__)
   CORS(app)
   app.config['JSON_SORT_KEYS'] = False
   
   # Routes and blueprints...
   
   if __name__ == '__main__':
       port = int(os.environ.get('PORT', 5000))
       app.run(host='0.0.0.0', port=port, debug=False)
   ```

#### Step 2: Push to GitHub

1. **Initialize git repository (if not done):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - EPL Crowd Impact web app"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/epl-crowd-impact.git
   git push -u origin main
   ```

#### Step 3: Deploy on Render

1. **Sign up at** [render.com](https://render.com)

2. **Connect GitHub account** to Render

3. **Create new Web Service:**
   - Select repository: `epl-crowd-impact`
   - Build command: `cd backend && pip install -r requirements.txt && python model/save_model.py`
   - Start command: `cd backend && gunicorn app:app`
   - Environment: Python 3.11

4. **Add Environment Variables** (if needed):
   ```
   FLASK_ENV=production
   ```

5. **Deploy:**
   - Render automatically rebuilds on every push to `main`
   - Your backend will be available at `https://epl-crowd-impact.onrender.com`

#### Step 4: Verify Backend Deployment

```bash
# Test prediction endpoint
curl -X POST https://epl-crowd-impact.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "crowd_present": 1,
    "HS": 10, "AS": 10, "HST": 5, "AST": 5,
    "HF": 10, "AF": 10, "HC": 4, "AC": 4,
    "HY": 1, "AY": 1, "HR": 0, "AR": 0
  }'
```

---

### Frontend Deployment (Vercel)

#### Step 1: Prepare Frontend Configuration

1. **Create `frontend/.env.production`:**
   ```
   VITE_API_URL=https://epl-crowd-impact.onrender.com/api
   ```

2. **Update `frontend/vite.config.js` (if needed):**
   ```javascript
   import { defineConfig } from 'vite'
   import react from '@vitejs/plugin-react'
   
   export default defineConfig({
     plugins: [react()],
     server: {
       proxy: {
         '/api': {
           target: process.env.VITE_API_URL || 'http://localhost:5000',
           changeOrigin: true,
         }
       }
     }
   })
   ```

#### Step 2: Deploy on Vercel

1. **Sign up at** [vercel.com](https://vercel.com)

2. **Connect GitHub account** to Vercel

3. **Create new project:**
   - Select repository: `epl-crowd-impact`
   - Framework preset: Vite
   - Build command: `npm run build`
   - Output directory: `dist`
   - Root directory: `frontend`

4. **Add Environment Variables:**
   ```
   VITE_API_URL=https://epl-crowd-impact.onrender.com/api
   ```

5. **Deploy:**
   - Vercel automatically deploys on push to `main`
   - Your frontend will be available at `https://epl-crowd-impact.vercel.app`

#### Step 3: Verify Frontend Deployment

- Open `https://epl-crowd-impact.vercel.app/`
- Test all pages:
  - ✓ Home page loads with hero section
  - ✓ Predict form works and calls backend
  - ✓ Dashboard displays KPI cards and charts
  - ✓ SHAP page shows explanations
  - ✓ About page displays methodology

---

## Architecture Overview

### Technology Stack

**Frontend (Vercel):**
- React 18.2.0 with React Router 6.14.1
- Vite (module bundler)
- Tailwind CSS 3.4.7 (styling)
- Axios 1.4.0 (HTTP client)

**Backend (Render):**
- Flask 3.1.3 (REST API)
- XGBoost 3.2.0 (multiclass classifier)
- SHAP 0.51.0 (explainability)
- scikit-learn 1.8.0 (preprocessing)
- Gunicorn 25.3.0 (WSGI server)
- Matplotlib 3.10.9 (SHAP visualizations)

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predict` | Get match prediction with probabilities |
| POST | `/api/shap` | Compute SHAP values for prediction |
| POST | `/api/shap_plot` | Generate SHAP matplotlib plot (PNG) |
| GET | `/api/images/list` | List available research chart images |
| GET | `/api/images/<filename>` | Serve research chart image |

### Data Flow

```
Frontend Form Input
  ↓
POST to /api/predict (match statistics JSON)
  ↓
Backend: Prepare Input (scale features)
  ↓
XGBoost Model: predict_proba()
  ↓
Return: {probabilities: {H, D, A}, predicted: 'H', confidence: X%}
  ↓
(Optional) POST to /api/shap (compute explanations)
  ↓
SHAP Explainer: explain(X)
  ↓
Return: {shap_values: [...], base_value, feature_names: [...]}
  ↓
(Optional) POST to /api/shap_plot (generate visualization)
  ↓
Matplotlib: Create feature importance bar plot
  ↓
Return: PNG blob (image/png)
  ↓
Frontend: Display prediction, SHAP table, SHAP plot
```

---

## Troubleshooting

### Backend Issues

**1. "ModuleNotFoundError: No module named 'flask'"**
- **Solution:** Activate virtual environment before running
  ```bash
  .venv\Scripts\Activate.ps1  # Windows
  source .venv/bin/activate  # macOS/Linux
  ```

**2. "No such file or directory: 'EPL_cleaned.csv'"**
- **Solution:** Ensure `EPL_cleaned.csv` is in `backend/` folder
  ```bash
  cp ../EPL_cleaned.csv ./
  ```

**3. "CORS policy: No 'Access-Control-Allow-Origin' header"**
- **Solution:** Verify Flask-CORS is installed and app initialized with CORS:
  ```python
  from flask_cors import CORS
  app = Flask(__name__)
  CORS(app)
  ```

**4. "Model prediction returns 0 confidence"**
- **Solution:** Verify model artifacts exist:
  ```bash
  ls model/xgb_model.pkl model/scaler.pkl model/features.json model/labels.json
  ```

### Frontend Issues

**1. "Failed to fetch from http://localhost:5000/api"**
- **Solution:** Verify backend is running on port 5000
- **Verify:** `curl http://localhost:5000/api/predict` returns something

**2. "SHAP plot image not loading (404)"**
- **Solution:** Check backend logs for `/api/shap_plot` endpoint errors
- **Verify:** `curl -X POST http://localhost:5000/api/shap_plot` returns PNG

**3. "Dashboard charts not showing"**
- **Solution:** Verify research PNG files are in backend root directory:
  ```bash
  ls ../season_analysis.png ../team_analysis.png ../crowd_impact.png ../team_scatter.png
  ```

### Production Deployment Issues

**1. Render backend stuck on "building"**
- Check build logs in Render dashboard
- Ensure `backend/Procfile` exists
- Verify `requirements.txt` has all dependencies

**2. Vercel frontend shows "API_URL undefined"**
- Verify `.env.production` has correct `VITE_API_URL`
- Environment variables must be set in Vercel project settings
- Redeploy after setting env vars

**3. CORS errors in production**
- **Solution:** Ensure backend CORS is configured for production domain:
  ```python
  CORS(app, resources={
      r"/api/*": {
          "origins": ["https://epl-crowd-impact.vercel.app"],
          "methods": ["GET", "POST"],
          "allow_headers": ["Content-Type"]
      }
  })
  ```

---

## Performance Optimization

### Backend Optimization

1. **Model Loading:**
   - Models are loaded once at startup (not per request)
   - Consider caching SHAP explainer for large datasets

2. **Matplotlib Warning (tkinter):**
   - Normal on Linux servers; use Agg backend:
     ```python
     import matplotlib
     matplotlib.use('Agg')
     import matplotlib.pyplot as plt
     ```

3. **Response Time:**
   - `/api/predict`: ~50-100ms
   - `/api/shap`: ~200-500ms (SHAP computation)
   - `/api/shap_plot`: ~500-1000ms (matplotlib rendering)

### Frontend Optimization

1. **Build size:**
   - Run `npm run build` and check `dist/` size
   - Use `npm run build -- --analyze` to identify large chunks

2. **Lazy loading:**
   - Dashboard and SHAP pages load images on demand
   - SHAP plot is computed server-side to reduce frontend computation

---

## Monitoring & Maintenance

### Logs

**Backend (Render):**
- View logs in Render dashboard
- Stream with: `render logs <app-id>`

**Frontend (Vercel):**
- View logs in Vercel dashboard
- Check browser console for client-side errors

### Updating the Application

1. **Make changes locally**
2. **Test thoroughly:**
   ```bash
   # Backend
   cd backend
   .venv\Scripts\Activate.ps1
   python app.py
   
   # Frontend (in another terminal)
   cd frontend
   npm run dev
   ```
3. **Commit and push to main:**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
4. **Automatic deployment:**
   - Render redeploys backend within ~2 minutes
   - Vercel redeploys frontend within ~1 minute

---

## Verification Checklist

Before considering production deployment complete, verify:

- [ ] Backend API endpoints respond with 200 status
- [ ] Frontend navigates through all 5 pages without errors
- [ ] Prediction form submits and displays results
- [ ] SHAP values compute and display
- [ ] SHAP plot image renders
- [ ] Dashboard KPI cards show correct values
- [ ] All research charts (PNG) display
- [ ] Browser console has no red errors
- [ ] Mobile responsiveness works on phones/tablets
- [ ] API URL is correctly configured for production domain

---

## Support & Additional Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **XGBoost Documentation:** https://xgboost.readthedocs.io/
- **SHAP Documentation:** https://shap.readthedocs.io/
- **React Documentation:** https://react.dev/
- **Render Documentation:** https://render.com/docs
- **Vercel Documentation:** https://vercel.com/docs

---

**Last Updated:** April 30, 2026  
**Project:** EPL Crowd Impact — Analyzing Home Field Advantage with Machine Learning
