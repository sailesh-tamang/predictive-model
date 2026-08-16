# MCP Document: EPL Crowd Impact Project

## 1. Project Overview

This project investigates how crowd presence is associated with home field advantage in the English Premier League. It combines:

- historical EPL match data from the 2018/19 to 2021/22 seasons,
- a binary research pipeline using home_win as the target,
- a deployed multiclass production model using FTR (Home / Draw / Away),
- SHAP-based explainability,
- a Flask backend API,
- a React + Vite frontend.

The project has two distinct analytical tasks:

1. Binary research task: home_win vs no home win
2. Production web-app task: FTR = H / D / A

The project is therefore both a research artifact and a working predictive application, but the two tasks must be reported separately.

---

## 2. Project Purpose and Scope

The overall research question is:

"How is crowd presence associated with home advantage in the Premier League?"

The application supports this by:
- comparing match outcomes under crowd-present vs no-crowd conditions,
- training a machine-learning model for Home / Draw / Away prediction,
- explaining model decisions using SHAP,
- presenting analysis dashboards and predictions through a web app.

This is not a causal-inference study and should not be described as proving causation. The project is observational and descriptive, with supervised prediction and explainability.

---

## 3. Two Separate ML Tasks

### 3.1 Binary Research Model

Target:
- home_win

Meaning:
- 1 = home win
- 0 = draw or away win

Purpose:
- exploratory model comparison,
- crowd-impact analysis,
- descriptive research scripts.

This is the task used in root research scripts such as model.py and crowd_impact.py.

### 3.2 Production Multiclass Model

Target:
- FTR

Classes:
- H = Home Win
- D = Draw
- A = Away Win

Purpose:
- deployed web-app prediction,
- Home / Draw / Away probability output,
- frontend prediction flow.

This is the model trained in backend/model/save_model.py and used by the API.

The project must clearly distinguish these tasks. Their metrics must not be mixed.

---

## 4. Data Pipeline

### 4.1 Raw Data Sources
The repository includes season-level files:
- EPL_2018_19.csv
- EPL_2019_20.csv
- EPL_2020_21.csv
- EPL_2021_22.csv

These are combined into a master dataset and then cleaned for modeling.

### 4.2 Merge Stage
The script merge_data.py combines the season files into one master dataset.

### 4.3 Cleaning Stage
The script clean_data.py:
- keeps the match-level features used in the project,
- creates a crowd_present flag,
- creates a home_win binary target,
- derives additional fields such as goal_diff, total_goals, total_yellow, and total_shots,
- saves the cleaned dataset as EPL_cleaned.csv.

### 4.4 Key Research Variable: crowd_present
The current project uses a binary crowd flag:
- crowd_present = 1 means crowd present
- crowd_present = 0 means no crowd

The value is currently generated using the COVID ghost-match window:

- matches from 2020-06-17 to 2021-05-23 are treated as no-crowd matches,
- all other matches are treated as crowd-present matches.

This methodology is a reproducible binary proxy, not a true attendance measurement.

### 4.5 verified crowd data counts
The cleaned dataset currently contains:
- Total matches: 1520
- Crowd present: 1048
- No crowd: 472
- Missing crowd values: 0
- Invalid crowd values: 0

This means crowd_present is internally valid as a binary field in {0, 1}.

However, it remains a date-based proxy, not exact attendance or stadium occupancy data.

---

## 5. Dataset Feature Set and Labels

The production model uses the following features:

- crowd_present
- HS
- AS
- HST
- AST
- HF
- AF
- HC
- AC
- HY
- AY
- HR
- AR

These are the 13 input variables used in the deployed model.

The production target is FTR:
- H = Home Win
- D = Draw
- A = Away Win

The numeric mapping in the model is:
- H -> 0
- D -> 1
- A -> 2

This mapping is stored in labels.json and used for model training and runtime prediction.

---

## 6. Mandatory fix: Train/Test Leakage

A leakage issue was identified in the production training workflow. The incorrect pattern was:

- fit scaler on the full dataset,
- then split into train/test,
- then train the model.

This was corrected.

The current production workflow is now:

1. define X and y
2. split into train/test with stratification
3. fit StandardScaler only on X_train
4. transform X_train and X_test using the fitted scaler
5. train the XGBoost model
6. evaluate on X_test

This is the technically correct workflow and prevents information leakage from the test set into preprocessing.

The production artifacts were regenerated after this correction.

---

## 7. Production Model Details

### 7.1 Model Type
The final deployed production model is a multiclass XGBoost classifier trained on FTR.

### 7.2 Training Script
The model is trained in:
- backend/model/save_model.py

### 7.3 Hyperparameters
The model is trained with:
- objective = multi:softprob
- num_class = 3
- n_estimators = 200
- learning_rate = 0.05
- use_label_encoder = False
- eval_metric = mlogloss
- random_state = 42

### 7.4 Production Artifacts
The backend/model folder contains:
- model.pkl
- scaler.pkl
- features.json
- labels.json
- model_metrics.json

These artifacts are used by the Flask backend at runtime.

---

## 8. Production Model Performance (Verified)

The trained production model was evaluated on the hold-out test set after the leakage fix.

Key metrics:
- Accuracy: 0.6151
- Macro F1: 0.5409
- Weighted F1: 0.5920
- ROC-AUC (macro OVR): 0.7452

Per-class metrics:

Home (H)
- Precision: 0.6460
- Recall: 0.7879
- F1: 0.7099

Draw (D)
- Precision: 0.3611
- Recall: 0.1940
- F1: 0.2524

Away (A)
- Precision: 0.6542
- Recall: 0.6667
- F1: 0.6604

These metrics are stored in backend/model/model_metrics.json and are the real production results for the multiclass prediction task.

---

## 9. Confusion Matrix

The confusion matrix for the production model is:

[[104, 13, 15],
 [32, 13, 22],
 [25, 10, 70]]

Interpretation:
- Home wins are the strongest-performing class.
- Draws are the most difficult class to classify.
- The model struggles most with Draw outcomes, which is visible in the low Draw recall and low Draw F1.

This limitation should be reported honestly rather than hidden.

---

## 10. Binary Research Model vs Production Model

These are separate tasks and should not be reported as the same metric set.

### 10.1 Binary research model
- Target: home_win
- Task: Home Win vs No Home Win
- Purpose: exploratory research, model comparison, crowd-impact analysis

### 10.2 Production web-app model
- Target: FTR
- Task: Home vs Draw vs Away
- Purpose: deployed prediction API and frontend interaction

### 10.3 Reporting rule
The binary model performance and the multiclass production performance must remain separate. The binary model is not the application prediction model.

---

## 11. Explainable AI: SHAP

### 11.1 SHAP purpose
SHAP is used to explain the contribution of each input feature to a prediction.

The deployment uses:
- shap.Explainer(MODEL)
- MODEL.predict_proba(X)
- predicted class selection
- per-feature contribution extraction

### 11.2 SHAP shape for multiclass XGBoost
The project uses a multiclass XGBoost model with 13 features and 3 output classes.

The verified SHAP object shape is:
- (1, 13, 3)

This means:
- 1 sample,
- 13 features,
- 3 classes.

The endpoint must extract the feature contributions for the class actually predicted by the model, not assume the wrong axis.

### 11.3 Correct extraction logic
The corrected logic selects the predicted class and keeps all 13 feature values for that class.

For a single prediction:
- predicted class = H, D, or A
- number of features = 13
- number of SHAP contributions returned = 13

This requirement is now satisfied in the backend.

### 11.4 SHAP endpoints
The backend exposes:
- /api/shap
- /api/shap_plot

Both endpoints are expected to work with the trained multiclass model.

---

## 12. Flask Backend Architecture

The backend is built with Flask.

Key files:
- backend/app.py
- backend/routes/predict.py
- backend/routes/shap_explain.py
- backend/model/model_utils.py

### 12.1 Prediction endpoint
The /api/predict route:
- loads the trained model and scaler,
- prepares the input using feature order from features.json,
- fills missing values with zero,
- applies the scaler,
- predicts probabilities,
- maps numeric outputs back to H/D/A labels,
- returns probabilities, predicted class, and confidence.

### 12.2 SHAP endpoint
The /api/shap route returns:
- base_value,
- feature_names,
- shap_values,
- predicted_class_index,
- predicted_label

### 12.3 SHAP plot endpoint
The /api/shap_plot route generates a PNG and returns it to the frontend.

---

## 13. Frontend Role

The frontend is a React + Vite application.

It consumes the backend for:
- prediction results,
- SHAP explanations,
- SHAP plot image,
- research dashboard visuals.

The frontend is not redesigned in this task. It remains a working interface for the deployed model and the research dashboard.

---

## 14. Causal and Academic Wording

The project uses observational data and predictive modeling. It should not claim causation.

Correct academic wording:
- “Crowd presence was associated with stronger home advantage in the analysed matches.”
- “The observed pattern is consistent with a possible association between crowd presence and referee-related match outcomes.”

The project should describe associations, not proof of causality.

This applies to documentation and explanatory messaging in the project.

---

## 15. Limitations and Future Work

The following are intentionally not implemented in this task:
- other leagues,
- longer time coverage,
- real attendance counts,
- stadium occupancy proportion modeling,
- crowd-noise data,
- difference-in-differences,
- causal inference models,
- live betting or odds integration,
- deep learning or LSTM models,
- user authentication,
- major frontend redesign,
- generative AI features.

These remain limitations or future work items, not part of the current project scope.

---

## 16. Validation and Working Status

The application was validated after the fixes:

- /api/predict: PASS
- /api/shap: PASS
- /api/shap_plot: PASS

Additional verified checks:
- prediction probabilities sum approximately to 1: PASS
- SHAP contribution count matches feature count: PASS

The production pipeline remains functional after retraining and regeneration of model artifacts.

### 16.1 Current Project Status
At this stage, the project is technically complete for the intended final-year submission:
- the leakage issue has been corrected,
- the production model has been retrained and verified,
- the SHAP logic is consistent with the multiclass output shape,
- the deployment pipeline is functional,
- the documentation and wording are aligned with the evidence.

No unresolved technical blockers remain. The only remaining work is optional polishing for presentation, final report formatting, and minor narrative refinement.

---

## 17. Final Summary

This project is a football analytics and predictive modeling application focused on the relationship between crowd presence and home advantage in the Premier League.

It contains:
- a binary research model for home_win,
- a multiclass production model for FTR,
- descriptive analysis of crowd impact,
- SHAP explainability,
- a Flask backend API,
- a React frontend.

The key technical corrections made were:
- fix preprocessing leakage by fitting the scaler only on X_train,
- correct the multiclass SHAP extraction so that it returns all feature contributions for the predicted class,
- regenerate the production model artifacts and metrics,
- separate the binary research task from the deployed multiclass task,
- keep wording academically defensible and avoid causal overstatement.

This is an appropriate final-year project structure for a reproducible, explainable sports analytics result.

