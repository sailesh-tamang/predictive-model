# MCP Document: EPL Crowd Impact Project

## 1. Project Overview

This project is a full-stack machine learning application built around a research question in football analytics:

"How does crowd presence affect home field advantage in the English Premier League?"

The application combines:
- historical Premier League data from 2018-2022,
- a trained multiclass machine learning model,
- an explainable AI layer using SHAP,
- a Flask API backend,
- a React + Vite frontend dashboard and prediction interface.

This project acts as both:
1. a research thesis artifact, and
2. a working web application that allows users to input match statistics and get AI-based predictions with explanations.

The core idea is to determine whether the presence or absence of a crowd changes the probability of a home win, draw, or away win, using actual match statistics as model inputs.

---

## 2. What the Application Does

The app allows a user to:
- open a web dashboard,
- view research insights and season-level analysis,
- enter in-match statistics for a hypothetical or real football match,
- receive a prediction from a machine-learning model for the match outcome,
- inspect probability scores for Home Win / Draw / Away Win,
- see SHAP feature contributions that explain which inputs pushed the prediction,
- analyze charts explaining crowd effects over seasons and teams.

The app is designed to answer a thesis-style question:
- Does crowd presence materially influence match outcomes?
- Is the impact measurable and explainable using AI?

---

## 3. Business and Research Context

The project uses the COVID-19 period as a natural experiment:
- normal matches with crowds,
- ghost matches without crowds,
- comparison between home win rates, goals, and other indicators.

This helps estimate how fans affect home advantage. In football, home field advantage is often attributed to a mix of travel fatigue, familiarity, referee bias, crowd energy, and psychological support. This project focuses on the crowd effect as a measurable variable.

The research uses machine learning not only for prediction but also for explainability. The model is not just a black box; it shows why a prediction happened.

---

## 4. High-Level Architecture

The project has a classic data-science + web-app structure:

1. Data preparation scripts
   - merge raw season CSVs into one master file
   - clean and engineer features
   - generate the final dataset used for modeling

2. Model training and artifact generation
   - train a multiclass XGBoost model
   - save the model, scaler, and feature metadata

3. Flask API backend
   - load trained artifacts
   - accept JSON input from frontend
   - return labels, probabilities, SHAP values, and images

4. React frontend
   - present the app UI
   - allow predictions
   - show dashboards and visual analysis

5. Static analysis assets
   - charts and visualizations are saved as PNG images
   - served through the Flask API and displayed inside the frontend

---

## 5. Main Project Structure

### Root folder
- README.md
  - basic setup and project summary
- DEPLOYMENT.md
  - production deployment instructions for Render and Vercel
- merge_data.py
  - merges the four EPL CSV files into one master dataset
- clean_data.py
  - filters to relevant columns and creates crowd_present, home_win, and derived metrics
- crowd_impact.py
  - measures how crowd presence affects home win rate, goals, referee actions, and feature importance
- season_analysis.py
  - analyzes results by season and creates season-level charts
- team_analysis.py
  - compares crowd impact by club and generates team-level plots
- model.py
  - exploratory model comparison script (Logistic Regression, Random Forest, XGBoost)
- EPL_master.csv
  - combined dataset across seasons
- EPL_cleaned.csv
  - cleaned and engineered dataset for modeling
- EPL_2018_19.csv through EPL_2021_22.csv
  - raw season-specific data files

### Backend folder
- app.py
  - Flask app factory and route registration
- requirements.txt
  - Python dependencies for backend
- Procfile
  - deployment command for gunicorn
- README.md
  - backend-specific setup instructions
- routes/
  - prediction API, SHAP endpoint, image serving
- model/
  - trained model artifacts and metadata

### Frontend folder
- package.json
  - React app dependencies and scripts
- src/
  - app UI and pages
- public/
  - static assets (if any)
- vite.config.js
  - Vite settings
- tailwind.config.js
  - Tailwind styling configuration
- index.html
  - app HTML shell

---

## 6. Data Pipeline

### 6.1 Raw Data Sources
The project uses individual season files:
- EPL_2018_19.csv
- EPL_2019_20.csv
- EPL_2020_21.csv
- EPL_2021_22.csv

These are standard football match datasets containing match-level statistics and results.

### 6.2 Merge Stage
The script merge_data.py does this:
- loads each season CSV,
- adds a season column,
- concatenates all rows into one master dataset,
- saves it as EPL_master.csv.

This creates a unified dataset across multiple seasons.

### 6.3 Cleaning Stage
The script clean_data.py does the following:
- reads EPL_master.csv,
- keeps only relevant columns such as:
  - Date
  - HomeTeam
  - AwayTeam
  - FTHG
  - FTAG
  - FTR
  - HS, AS
  - HST, AST
  - HF, AF
  - HC, AC
  - HY, AY
  - HR, AR
  - Referee
  - season
- creates crowd_present
  - 1 = crowd present
  - 0 = no crowd
- creates home_win
  - 1 if home team won
  - 0 if draw or away win
- adds derived columns:
  - goal_diff
  - total_goals
  - total_yellow
  - total_shots
- checks missing values
- saves the cleaned version to EPL_cleaned.csv

### 6.4 Why the crowd_present column matters
The key natural experiment is:
- matches from 2020-06-17 to 2021-05-23 were played behind closed doors,
- all of those are marked as crowd_present = 0,
- all other matches are crowd_present = 1.

This allows the research to compare home advantage under normal crowd conditions vs. no-crowd conditions.

---

## 7. Dataset Columns and Meaning

The model uses a subset of features from the cleaned matches dataset:

- crowd_present
  - whether fans were present
- HS
  - home shots
- AS
  - away shots
- HST
  - home shots on target
- AST
  - away shots on target
- HF
  - home fouls
- AF
  - away fouls
- HC
  - home corners
- AC
  - away corners
- HY
  - home yellow cards
- AY
  - away yellow cards
- HR
  - home red cards
- AR
  - away red cards

Target variable:
- FTR = Full Time Result
  - H = Home Win
  - D = Draw
  - A = Away Win

Derived classification target used in model training:
- H -> 0
- D -> 1
- A -> 2

This is stored in labels.json.

---

## 8. AI Model Details

### 8.1 Model Type
The final deployed model is a multiclass XGBoost classifier.

The training script is located at:
- backend/model/save_model.py

It does the following:
- reads EPL_cleaned.csv from the repository root,
- defines the feature list,
- maps target labels to numeric classes,
- fills missing values with zeros,
- uses StandardScaler to normalize the input features,
- performs stratified train/test split,
- trains an XGBoost model using objective='multi:softprob',
- saves the trained artifact to backend/model/model.pkl

### 8.2 Exact Model Configuration
The model is trained with:
- objective: multi:softprob
- num_class: 3
- n_estimators: 200
- learning_rate: 0.05
- use_label_encoder: False
- eval_metric: mlogloss
- random_state: 42

This means the model predicts probabilities for each class (Home/Draw/Away) and the output is a multiclass probability distribution.

### 8.3 Why XGBoost
XGBoost was selected because it is highly effective on tabular data like match statistics. It usually performs very well for structured sports data and is robust for outcome prediction tasks.

### 8.4 Additional Exploratory Models
The root file model.py tests multiple models:
- Logistic Regression
- Random Forest Classifier
- XGBoost Classifier

It compares them using:
- Accuracy
- ROC-AUC
- Classification report

This script served as the experimental comparison to justify the final deployed XGBoost model.

### 8.5 Model Artifacts
The backend model folder contains:
- model.pkl
  - trained XGBoost classifier
- scaler.pkl
  - StandardScaler fitted on training data
- features.json
  - ordered list of feature names used by the model
- labels.json
  - mapping between class names and numeric labels

The loaded artifacts are used at runtime by the backend.

---

## 9. Model Input and Output

### Input features
The model takes a JSON payload shaped like this:

```json
{
  "crowd_present": 1,
  "HS": 11,
  "AS": 9,
  "HST": 5,
  "AST": 4,
  "HF": 12,
  "AF": 10,
  "HC": 6,
  "AC": 4,
  "HY": 1,
  "AY": 2,
  "HR": 0,
  "AR": 0
}
```

### Output from prediction API
The API returns:
- probabilities
- predicted outcome label
- confidence score

Example response:

```json
{
  "probabilities": {
    "H": 0.48,
    "D": 0.22,
    "A": 0.30
  },
  "predicted": "H",
  "confidence": 0.48
}
```

The actual backend code converts numeric class indices back into labels H/D/A using labels.json.

---

## 10. Explainable AI: SHAP

### 10.1 What SHAP means
SHAP stands for SHapley Additive exPlanations.

SHAP is used to explain the contribution of each feature to the model’s prediction. It answers questions like:
- Which variables pushed the decision toward home win?
- Did crowd presence matter strongly?
- Was a bad performance caused by low shots or high fouls?

### 10.2 SHAP Integration in this Project
The backend exposes:
- /api/shap
  - returns SHAP values for a given prediction as JSON
- /api/shap_plot
  - returns a PNG image of the top feature contributions

The SHAP logic uses:
- shap.Explainer(MODEL)
- MODEL.predict_proba(X)
- extraction of the predicted class index
- flattening SHAP values per feature

### 10.3 SHAP value behavior
For multiclass predictions, SHAP values are class-specific. The code calculates the predicted class and then extracts the SHAP contributions for that class only.

This means the explanation is tied to the actual class the model chose. For example:
- if the model predicts Home Win, SHAP values are extracted for the Home class contribution

### 10.4 Visual outputs
The project also serves static SHAP plots and dashboard screenshots, including:
- SHAP summary plot
- SHAP bar plot
- crowd-specific SHAP analysis

These are displayed in the frontend SHAP page and dashboard page.

---

## 11. Backend Architecture

### 11.1 Framework
The backend is built with Flask.

The main app file is backend/app.py.

It registers three blueprints:
- predict
- images
- shap

This keeps the endpoints organized and modular.

### 11.2 App entry point
The root app logic:
- creates a Flask app using create_app()
- enables CORS
- imports blueprints
- registers them under /api
- exposes a root endpoint returning status

### 11.3 Route files

#### routes/predict.py
This is the main prediction endpoint.

It does:
- load trained model artifacts from backend/model,
- accept user JSON payload,
- prepare input using prepare_input,
- transform features with scaler if available,
- run MODEL.predict_proba,
- map numeric outputs back to H/D/A labels,
- return probabilities and confidence.

#### routes/shap_explain.py
This file handles explainability.

It provides:
- /api/shap
  - returns feature names and SHAP contribution values
- /api/shap_plot
  - creates and returns a PNG of SHAP contributions

The plot is generated using matplotlib and the saved figure is sent as a static image.

#### routes/images.py
This file serves image assets from the project root.

It provides:
- /api/images/list
  - returns a list of available plot files
- /api/images/<filename>
  - returns an image file from the project folder

This allows the frontend to display charts generated from research analysis.

---

## 12. Backend Utility Functions

The file backend/model/model_utils.py contains the core loading and transformation code.

### Function: load_artifacts
This function:
- locates model.pkl, scaler.pkl and features.json inside backend/model,
- loads the trained XGBoost model and StandardScaler,
- loads labels.json if available,
- returns model, scaler, features and labels.

### Function: prepare_input
This function:
- takes user payload JSON,
- iterates through feature names in order,
- maps missing fields to 0,
- converts values to float,
- builds a pandas DataFrame,
- applies scaler transform if scaler is provided,
- returns a DataFrame ready for model input.

This is important because the model expects consistent features in exact order.

---

## 13. Frontend Architecture

The frontend is built with React and Vite.

### Main files
- App.jsx
  - navigation and page routing
- src/api.js
  - API base URL logic
- pages/Home.jsx
  - landing page with summary and CTA
- pages/Predict.jsx
  - match prediction form with probability bars and SHAP results
- pages/Dashboard.jsx
  - charts and visual analysis of crowd impact
- pages/SHAP.jsx
  - SHAP explainability visualizations
- pages/About.jsx
  - methodology and thesis content

### Styling
The frontend uses Tailwind CSS to create a clean dashboard aesthetic.

### Navigation
Routes include:
- /
- /predict
- /dashboard
- /shap
- /about

### Main user flows
1. User visits Home page
2. User clicks Predict or enters match stats
3. Frontend posts to /api/predict
4. Backend returns predicted class and probabilities
5. Frontend also calls /api/shap and /api/shap_plot
6. UI displays prediction plus explainability
7. User can navigate to research dashboards and charts

---

## 14. Frontend Prediction Page Behavior

The Predict page allows the user to fill in:
- crowd_present
- HS, AS
- HST, AST
- HF, AF
- HC, AC
- HY, AY
- HR, AR

After submission:
- prediction request goes to the API,
- result is displayed with a label and probability bars,
- explanation request retrieves SHAP values,
- SHAP plot image may be generated and shown,
- model confidence is displayed as a percentage.

Visual logic in the frontend:
- Home Win = green styling
- Draw = yellow styling
- Away Win = red styling

This helps the end user quickly understand predictions.

---

## 15. Dashboard and Research Visualization

The app includes the following analysis charts:

- season_analysis.png
  - compares home win rates by season
- team_analysis.png
  - team-by-team crowd impact visualizations
- crowd_impact.png
  - overall effect of crowd presence on match outcomes
- team_scatter.png
  - scatter plot comparing home win rates with and without crowd

These are served by the backend and shown in the Dashboard and SHAP pages.

These visuals are essential to the thesis narrative because they provide empirical evidence that crowd impact is real and measurable.

---

## 16. Project Scripts and Their Roles

### merge_data.py
Purpose:
- combine the four season datasets
- generate a master compilation for research

### clean_data.py
Purpose:
- prepare the cleaned dataset for modeling
- engineer crowd and home-win variables

### crowd_impact.py
Purpose:
- analyze average home win rate with vs without crowd
- compare goals and yellow cards
- fit a RandomForest model to estimate important features
- save a crowd impact chart

### season_analysis.py
Purpose:
- report home win rate, goals, and cards by season
- visualize season-level patterns and COVID ghost season effect

### team_analysis.py
Purpose:
- analyze which teams are most affected by crowd removal
- visualize team-level home win rate shifts

### model.py
Purpose:
- compare production candidate models
- evaluate prediction quality

### backend/model/save_model.py
Purpose:
- final model training pipeline for deployment
- saves XGBoost artifact used in API

---

## 17. Technical Dependencies

### Python dependencies from backend/requirements.txt
- flask
- flask-cors
- pandas
- numpy
- scikit-learn
- xgboost
- joblib
- gunicorn
- shap
- matplotlib

### Frontend dependencies from frontend/package.json
- react
- react-dom
- react-router-dom
- axios
- vite
- tailwindcss
- postcss
- autoprefixer

These dependencies collectively support:
- data handling,
- AI model execution,
- API serving,
- visual analysis,
- frontend routing,
- styling.

---

## 18. Runtime Workflows

### Local backend workflow
1. Create a virtual environment
2. Install requirements from backend/requirements.txt
3. Run python backend/model/save_model.py
4. Start backend with python backend/app.py
5. API becomes available at http://localhost:5000/api

### Local frontend workflow
1. Go to frontend/
2. Run npm install
3. Run npm run dev
4. Access frontend at http://localhost:5173

### Typical user interaction
1. User enters match stats in the prediction form
2. Frontend sends POST to /api/predict
3. Flask loads model artifacts and scales input
4. XGBoost predicts class probabilities
5. API sends result back to frontend
6. Frontend also requests SHAP explanations
7. User sees the predicted outcome, confidence, and feature importance

---

## 19. Deployment Overview

The project is intended to be deployed in two components:

### Backend deployment
- likely hosted on Render
- uses gunicorn
- served through app:create_app or wsgi

### Frontend deployment
- likely hosted on Vercel
- uses Vite build output
- connects to backend API through VITE_API_URL

The deployment guide in DEPLOYMENT.md includes:
- local dev commands,
- Render configuration,
- Vercel environment variable setup,
- verification steps for prediction endpoints.

---

## 20. AI / ML Interpretation of the Project

This project is not a generic chatbot or LLM application.

It is a classical machine learning project with:
- structured tabular input,
- supervised classification,
- XGBoost learning from historical match features,
- probability-based prediction,
- SHAP-based interpretability.

In plain terms:
"The app learns from historical Premier League matches and predicts likely game outcomes using features like shots, corners, fouls, cards, and crowd status. It explains its prediction by showing which factors contributed the most."

This is a strong example of applied AI in sports analytics and research.

---

## 21. Key Research Findings Reflected in the App

The product and UI are built around the thesis findings:
- crowd presence changes home win probability,
- home advantage is diminished without crowd support,
- seasons with ghost matches show altered outcomes,
- clubs differ in how strongly crowd presence affects them,
- SHAP values show crowd presence as a meaningful contributor to model explanations,
- AI helps quantify and visualize that relationship.

These findings are represented in the landing page, dashboard, SHAP section, and the overall narrative of the project.

---

## 22. Important Implementation Notes

- The final production model is trained in backend/model/save_model.py, not in the root model.py file.
- The backend loads artifacts at import time for the blueprint routes.
- If model artifacts are missing, the prediction endpoint returns a helpful error message.
- Input features must match the exact feature order saved in features.json.
- SHAP is optional at runtime; if not installed, the SHAP endpoint returns an error.
- Model labels are mapped from H/D/A to numeric values internally and back again for the API.

---

## 23. Example of Full Data Flow

1. Data is merged and cleaned.
2. Crowd presence is added via date logic.
3. A CSV dataset is created.
4. Training script loads the dataset.
5. Features are scaled.
6. XGBoost trains a multiclass classifier.
7. Model and scaler are saved.
8. Flask app loads these artifacts.
9. User posts match statistics.
10. Backend prepares the input.
11. Model predicts probabilities for Home/Draw/Away.
12. SHAP explains the prediction.
13. Frontend shows result and charts.
14. User views a dashboard explaining the broader crowd impact.

---

## 24. Summary

This project is a complete machine-learning and explainability application for analyzing the effect of crowd presence on Premier League home field advantage.

It combines:
- sports research,
- data engineering,
- supervised learning,
- XGBoost modeling,
- SHAP explainability,
- Flask API backend,
- React frontend,
- dashboard visualizations,
- deployment-ready architecture.

Anyone reading this document should be able to understand:
- what the app does,
- how the data is prepared,
- how the model is trained and saved,
- how the backend APIs work,
- how the frontend consumes the model,
- why the project matters as both a research and product example.

---

## 25. Final One-Line Description

EPL Crowd Impact is a football analytics and AI-powered prediction app that studies how crowd presence changes home field advantage in the Premier League, using XGBoost for multiclass outcome prediction and SHAP for explainable insights.
