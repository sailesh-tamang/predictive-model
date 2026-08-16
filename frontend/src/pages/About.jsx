import React from 'react'

export default function About(){
  return (
    <div className="space-y-6">
      <section className="card">
        <h2 className="text-3xl font-bold mb-4">Research Methodology</h2>
        <p className="text-gray-700 mb-4">
          This thesis employs a machine learning approach to quantify the impact of crowd presence on home field advantage in Premier League matches. The study leverages historical match data and a unique natural experiment (COVID-19 no-crowd season) to isolate crowd effects.
        </p>
      </section>

      <section className="card">
        <h3 className="text-2xl font-semibold mb-4">Dataset</h3>
        <ul className="space-y-3 text-gray-700">
          <li><strong>Time Period:</strong> August 2018 – May 2022 (4 seasons)</li>
          <li><strong>Sample Size:</strong> ~1,140 Premier League matches</li>
          <li><strong>Features:</strong> 14 in-match statistics (shots, fouls, cards, etc.) + binary crowd presence indicator</li>
          <li><strong>Target Variable:</strong> Final match result (Home Win / Draw / Away Win)</li>
          <li><strong>Data Sources:</strong> Official Premier League records and match statistics</li>
        </ul>
      </section>

      <section className="card">
        <h3 className="text-2xl font-semibold mb-4">Data Preprocessing</h3>
        <ul className="space-y-2 text-gray-700">
          <li>✓ Removal of null values and outliers</li>
          <li>✓ Feature scaling using StandardScaler (for non-tree-based models)</li>
          <li>✓ Stratified train-test split (80/20) to maintain class balance</li>
          <li>✓ Temporal ordering preserved to avoid data leakage</li>
          <li>✓ Categorical encoding of match outcome (H/D/A → 0/1/2)</li>
        </ul>
      </section>

      <section className="card">
        <h3 className="text-2xl font-semibold mb-4">Machine Learning Model</h3>
        <div className="space-y-4">
          <div>
            <h4 className="font-semibold mb-2">Model Choice: XGBoost</h4>
            <p className="text-gray-700 mb-2">
              XGBoost (Extreme Gradient Boosting) was selected for its:
            </p>
            <ul className="text-gray-700 space-y-1 ml-4">
              <li>• High predictive accuracy on tabular data</li>
              <li>• Robustness to class imbalance</li>
              <li>• Built-in feature importance computation</li>
              <li>• Compatibility with SHAP explainability</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Hyperparameters</h4>
            <ul className="text-sm text-gray-700 space-y-1">
              <li>• n_estimators: 200</li>
              <li>• learning_rate: 0.05</li>
              <li>• objective: multi:softprob (multiclass classification)</li>
              <li>• eval_metric: mlogloss</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="card">
        <h3 className="text-2xl font-semibold mb-4">Evaluation Metrics</h3>
        <p className="text-gray-700 mb-4">
          Model performance is evaluated on held-out test set using:
        </p>
        <ul className="space-y-2 text-gray-700">
          <li><strong>Accuracy:</strong> Overall proportion of correct predictions</li>
          <li><strong>Macro-Averaged Precision/Recall/F1:</strong> Per-class performance to account for class imbalance</li>
          <li><strong>ROC-AUC:</strong> Discriminative ability across probability thresholds</li>
          <li><strong>Confusion Matrix:</strong> Breakdown of correct and incorrect predictions by class</li>
        </ul>
      </section>

      <section className="card">
        <h3 className="text-2xl font-semibold mb-4">SHAP Explainability</h3>
        <p className="text-gray-700 mb-4">
          SHAP (SHapley Additive exPlanations) values provide model-agnostic explanations by computing each feature's contribution to individual predictions:
        </p>
        <ul className="space-y-2 text-gray-700">
          <li>• <strong>Waterfall Plots:</strong> Show cumulative feature effects from base value to prediction</li>
          <li>• <strong>Force Plots:</strong> Visualize positive and negative contributions side-by-side</li>
          <li>• <strong>Summary Plots:</strong> Aggregate feature importance across all predictions</li>
          <li>• <strong>Crowd Contribution:</strong> Directly quantifies the SHAP value of crowd presence for each match</li>
        </ul>
      </section>

      <section className="card">
        <h3 className="text-2xl font-semibold mb-4">Key Findings</h3>
        <div className="space-y-3 text-gray-700">
          <p><strong>1. Observed Association:</strong> Crowd presence is associated with a difference in the observed home-win pattern when compared with no-crowd matches in the dataset.</p>
          <p><strong>2. COVID Natural Experiment:</strong> The 2020-21 no-crowd season provides a useful comparison period within the available data, but the crowd variable remains a binary proxy rather than a continuous attendance measure.</p>
          <p><strong>3. Feature Importance:</strong> SHAP analysis shows that crowd presence contributes to model predictions alongside other in-match features, but this remains an association-based interpretation rather than causal proof.</p>
          <p><strong>4. Production Model Performance:</strong> The deployed multiclass model achieved 61.5% accuracy on the held-out test set for Home / Draw / Away prediction.</p>
        </div>
      </section>

      <section className="card">
        <h3 className="text-2xl font-semibold mb-4">Conclusions</h3>
        <p className="text-gray-700 mb-4">
          This project provides an observational and predictive analysis of how crowd presence is associated with home field advantage in Premier League matches. By combining match statistics, a binary crowd indicator, and explainable AI, the research examines patterns within the available dataset without claiming causal proof.
        </p>
        <p className="text-gray-700">
          The application of SHAP values offers interpretable insight into model predictions, while recognising that the analysis remains descriptive and predictive rather than causal.
        </p>
      </section>

      <section className="card">
        <h3 className="text-2xl font-semibold mb-4">Future Recommendations</h3>
        <ul className="space-y-2 text-gray-700">
          <li>• <strong>Real-time Prediction:</strong> Deploy the model for live match forecasting with crowd impact explanations</li>
          <li>• <strong>Other Leagues:</strong> Replicate the analysis across other European leagues (La Liga, Serie A, Bundesliga, Ligue 1)</li>
          <li>• <strong>Crowd Proxy:</strong> Integrate actual attendance figures instead of binary indicator for granular analysis</li>
          <li>• <strong>Temporal Dynamics:</strong> Explore time-series approaches to capture evolving crowd effects post-COVID</li>
          <li>• <strong>Causal Inference:</strong> Apply causal forest or doubly robust methods to isolate causal effects more rigorously</li>
        </ul>
      </section>
    </div>
  )
}
