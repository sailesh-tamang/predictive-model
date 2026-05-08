import React from 'react'
import { Link, useNavigate } from 'react-router-dom'

export default function Home(){
  const navigate = useNavigate()
  return (
    <div>
      {/* Hero Section */}
      <section className="card mb-6 bg-gradient-to-r from-primary to-primary-600 text-white overflow-hidden">
        <div className="md:flex md:items-center md:justify-between">
          <div className="max-w-3xl py-10">
            <h1 className="text-4xl md:text-5xl font-bold mb-3">Analyzing the Impact of Crowd Presence on Home Field Advantage</h1>
            <p className="text-lg mb-6 text-blue-100">A machine learning study exploring how stadium crowds influence Premier League match outcomes, including the COVID-19 no-crowd period.</p>
            <div className="flex space-x-4">
              <Link to="/predict" className="btn-primary" aria-label="Try prediction">Try Prediction</Link>
              <Link to="/about" className="px-4 py-2 rounded bg-white bg-opacity-10 border border-white text-white hover:bg-opacity-20" aria-label="Learn more">Learn More</Link>
            </div>
          </div>
          <div className="hidden md:block w-1/3">
            {/* Stadium illustration */}
            <svg viewBox="0 0 300 200" className="w-full h-auto max-h-40" xmlns="http://www.w3.org/2000/svg">
              {/* Outer stadium structure */}
              <rect x="30" y="20" width="240" height="160" rx="8" fill="none" stroke="#e0e7ff" strokeWidth="2"/>
              
              {/* Crowd areas - top and bottom */}
              <rect x="35" y="25" width="230" height="25" fill="#dbeafe" opacity="0.6"/>
              <rect x="35" y="145" width="230" height="30" fill="#dbeafe" opacity="0.6"/>
              
              {/* Crowd areas - left and right */}
              <rect x="35" y="50" width="20" height="90" fill="#dbeafe" opacity="0.6"/>
              <rect x="245" y="50" width="20" height="90" fill="#dbeafe" opacity="0.6"/>
              
              {/* Playing field */}
              <rect x="60" y="55" width="180" height="90" fill="#dbeafe" opacity="0.3" stroke="#e0e7ff" strokeWidth="1.5"/>
              
              {/* Center line */}
              <line x1="150" y1="55" x2="150" y2="145" stroke="#e0e7ff" strokeWidth="1.5"/>
              
              {/* Center circle */}
              <circle cx="150" cy="100" r="12" fill="none" stroke="#e0e7ff" strokeWidth="1.5"/>
              <circle cx="150" cy="100" r="2" fill="#e0e7ff"/>
              
              {/* Goal areas */}
              <rect x="60" y="75" width="25" height="50" fill="none" stroke="#e0e7ff" strokeWidth="1"/>
              <rect x="215" y="75" width="25" height="50" fill="none" stroke="#e0e7ff" strokeWidth="1"/>
              
              {/* Penalty areas */}
              <rect x="55" y="65" width="35" height="70" fill="none" stroke="#e0e7ff" strokeWidth="1" opacity="0.5"/>
              <rect x="210" y="65" width="35" height="70" fill="none" stroke="#e0e7ff" strokeWidth="1" opacity="0.5"/>
              
              {/* Corner arcs */}
              <path d="M 35 55 Q 35 45 45 45" fill="none" stroke="#e0e7ff" strokeWidth="1" opacity="0.4"/>
              <path d="M 265 55 Q 265 45 255 45" fill="none" stroke="#e0e7ff" strokeWidth="1" opacity="0.4"/>
              <path d="M 35 145 Q 35 155 45 155" fill="none" stroke="#e0e7ff" strokeWidth="1" opacity="0.4"/>
              <path d="M 265 145 Q 265 155 255 155" fill="none" stroke="#e0e7ff" strokeWidth="1" opacity="0.4"/>
            </svg>
          </div>
        </div>
      </section>

      {/* Key Findings */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="card">
          <h3 className="font-semibold text-lg mb-2">Crowd Impact on Win Probability</h3>
          <p className="text-gray-700">Presence of crowd increases home win probability significantly across most seasons, with measurable statistical differences.</p>
        </div>
        <div className="card">
          <h3 className="font-semibold text-lg mb-2">COVID Period Effect</h3>
          <p className="text-gray-700">No-crowd seasons (2020-21) showed measurable drops in home advantage, providing natural experiment evidence for crowd influence.</p>
        </div>
        <div className="card">
          <h3 className="font-semibold text-lg mb-2">AI Explainability</h3>
          <p className="text-gray-700">SHAP analysis reveals crowd presence as a key feature for match outcome prediction, with quantifiable contribution values.</p>
        </div>
      </section>

      {/* Key Findings Stats */}
      <section className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="p-6 rounded-lg bg-gradient-to-br from-blue-50 to-blue-100 border border-blue-200 hover:shadow-lg transition-shadow">
          <div className="text-4xl font-bold text-blue-700">5.5%</div>
          <p className="text-sm text-blue-600 mt-3 font-medium">Home Win Rate Drop Without Crowd</p>
        </div>
        <div className="p-6 rounded-lg bg-gradient-to-br from-red-50 to-red-100 border border-red-200 hover:shadow-lg transition-shadow">
          <div className="text-4xl font-bold text-red-700">32.2%</div>
          <p className="text-sm text-red-600 mt-3 font-medium">Liverpool's HFA Drop (Biggest)</p>
        </div>
        <div className="p-6 rounded-lg bg-gradient-to-br from-green-50 to-green-100 border border-green-200 hover:shadow-lg transition-shadow">
          <div className="text-4xl font-bold text-green-700">9.5%</div>
          <p className="text-sm text-green-600 mt-3 font-medium">Prediction Drop Without Crowd (SHAP)</p>
        </div>
        <div className="p-6 rounded-lg bg-gradient-to-br from-purple-50 to-purple-100 border border-purple-200 hover:shadow-lg transition-shadow">
          <div className="text-4xl font-bold text-purple-700">74.3%</div>
          <p className="text-sm text-purple-600 mt-3 font-medium">Model Accuracy</p>
        </div>
      </section>

      {/* Problem Statement */}
      <section className="card mb-6 bg-gray-50">
        <h2 className="text-2xl font-bold mb-4">Problem Statement</h2>
        <p className="text-gray-700 mb-4">
          Home field advantage (HFA) is a well-documented phenomenon in sports where teams playing at home win more frequently than expected. The COVID-19 pandemic provided a unique natural experiment: Premier League matches were played without crowds for an entire season.
        </p>
        <p className="text-gray-700">
          This thesis uses machine learning and SHAP explainability to quantify the specific contribution of crowd presence to match outcomes, controlling for team quality, match statistics, and temporal factors.
        </p>
      </section>

      {/* Technology Stack */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-bold mb-3">Data & Model</h2>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>📊 Dataset: Premier League 2018-2022 (4 seasons)</li>
            <li>🤖 Model: XGBoost (multiclass classification)</li>
            <li>📈 Features: 14 match statistics + crowd presence</li>
            <li>🔍 Explainability: SHAP values</li>
          </ul>
        </div>
        <div className="card">
          <h2 className="text-xl font-bold mb-3">Web Application</h2>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>⚛️ Frontend: React + Vite + Tailwind CSS</li>
            <li>🐍 Backend: Flask + XGBoost</li>
            <li>🎯 Prediction: REST API with SHAP explanations</li>
            <li>📦 Deployment: Vercel (frontend), Render (backend)</li>
          </ul>
        </div>
      </section>

      {/* How It Works */}
      <section className="mb-6">
        <h2 className="text-3xl font-bold mb-6 text-center">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="card bg-gradient-to-br from-blue-50 to-transparent">
            <div className="text-3xl font-bold text-blue-600 mb-3">1️⃣</div>
            <h3 className="font-semibold mb-2">Enter Match Stats</h3>
            <p className="text-sm text-gray-600">Input home and away team statistics for any match</p>
          </div>
          <div className="card bg-gradient-to-br from-green-50 to-transparent">
            <div className="text-3xl font-bold text-green-600 mb-3">2️⃣</div>
            <h3 className="font-semibold mb-2">AI Prediction</h3>
            <p className="text-sm text-gray-600">XGBoost model predicts match outcome (H/D/A)</p>
          </div>
          <div className="card bg-gradient-to-br from-purple-50 to-transparent">
            <div className="text-3xl font-bold text-purple-600 mb-3">3️⃣</div>
            <h3 className="font-semibold mb-2">SHAP Explanation</h3>
            <p className="text-sm text-gray-600">See exactly which factors influenced the prediction</p>
          </div>
          <div className="card bg-gradient-to-br from-orange-50 to-transparent">
            <div className="text-3xl font-bold text-orange-600 mb-3">4️⃣</div>
            <h3 className="font-semibold mb-2">Crowd Impact</h3>
            <p className="text-sm text-gray-600">Understand crowd's contribution to home advantage</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="card bg-gradient-to-r from-blue-600 to-blue-700 text-white mb-6">
        <div className="text-center py-8">
          <h2 className="text-3xl font-bold mb-3">Ready to Predict?</h2>
          <p className="text-blue-100 mb-6 max-w-2xl mx-auto">Enter match statistics and discover how crowd presence influences Premier League outcomes with AI-powered predictions and SHAP explainability.</p>
          <Link to="/predict" className="inline-block px-8 py-3 rounded-lg bg-white text-blue-600 font-semibold hover:bg-blue-50 transition-colors">
            Get Started with Predictions
          </Link>
        </div>
      </section>

      {/* Resources */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="card hover:shadow-lg hover:border-blue-300 transition-all cursor-pointer" onClick={() => navigate('/dashboard')}>
          <h3 className="font-semibold text-lg mb-2 flex items-center">
            <span className="text-2xl mr-2">📊</span>
            Dashboard
          </h3>
          <p className="text-sm text-gray-600">View season analysis, team statistics, and crowd impact metrics</p>
        </div>
        <div className="card hover:shadow-lg hover:border-blue-300 transition-all cursor-pointer" onClick={() => navigate('/shap')}>
          <h3 className="font-semibold text-lg mb-2 flex items-center">
            <span className="text-2xl mr-2">🔍</span>
            SHAP Analysis
          </h3>
          <p className="text-sm text-gray-600">Explore feature importance and individual prediction explanations</p>
        </div>
        <div className="card hover:shadow-lg hover:border-blue-300 transition-all cursor-pointer" onClick={() => navigate('/about')}>
          <h3 className="font-semibold text-lg mb-2 flex items-center">
            <span className="text-2xl mr-2">📚</span>
            Research
          </h3>
          <p className="text-sm text-gray-600">Deep dive into the thesis methodology and research findings</p>
        </div>
      </section>
    </div>
  )
}
