import React, {useEffect, useState} from 'react'
import axios from 'axios'

const API = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

export default function SHAP(){
  const [images, setImages] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(()=>{
    setLoading(true)
    axios.get(`${API}/images/list`).then(r=> setImages(r.data.images || [])).catch(()=>{}).finally(()=> setLoading(false))
  },[])

  const find = (name) => images.find(x=> x.toLowerCase().includes(name))

  return (
    <div>
      <section className="card">
        <h2 className="text-2xl font-semibold mb-2">SHAP Explainability Analysis</h2>
        <p className="mb-4 text-gray-700">SHAP (SHapley Additive exPlanations) values explain how each feature contributes to the model's predictions. These plots show the global model behavior across all matches in the dataset.</p>

        {loading ? (
          <div className="text-center py-8 text-gray-600">Loading SHAP plots...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="border rounded-lg p-4 bg-gray-50">
              <h3 className="font-semibold mb-2 text-gray-800">SHAP Summary Plot</h3>
              <p className="text-xs text-gray-600 mb-3">Shows the impact of each feature on model output. Points colored by feature value (red=high, blue=low).</p>
              {find('shap_summary') ? (
                <img src={`${API}/images/${find('shap_summary')}`} alt="shap summary" className="w-full rounded border border-gray-300" />
              ) : <div className="text-sm text-gray-500 py-8 text-center">Plot not available</div>}
            </div>

            <div className="border rounded-lg p-4 bg-gray-50">
              <h3 className="font-semibold mb-2 text-gray-800">SHAP Bar Plot (Feature Importance)</h3>
              <p className="text-xs text-gray-600 mb-3">Shows mean absolute SHAP values - the most important features for predictions are at the top.</p>
              {find('shap_bar') ? (
                <img src={`${API}/images/${find('shap_bar')}`} alt="shap bar" className="w-full rounded border border-gray-300" />
              ) : <div className="text-sm text-gray-500 py-8 text-center">Plot not available</div>}
            </div>

            <div className="border rounded-lg p-4 bg-gray-50 md:col-span-2">
              <h3 className="font-semibold mb-2 text-gray-800">Crowd Presence Impact on SHAP Values</h3>
              <p className="text-xs text-gray-600 mb-3">Analysis of how the crowd presence feature affects model predictions and feature importance rankings.</p>
              {find('shap_crowd') ? (
                <img src={`${API}/images/${find('shap_crowd')}`} alt="shap crowd" className="w-full rounded border border-gray-300" />
              ) : <div className="text-sm text-gray-500 py-8 text-center">Plot not available</div>}
            </div>
          </div>
        )}

        <div className="mt-8 p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
          <h4 className="font-semibold text-blue-900 mb-2">How to Interpret SHAP Values</h4>
          <ul className="text-sm text-blue-800 space-y-2">
            <li><strong>Red points (Summary plot):</strong> High feature values push prediction toward Home (H)</li>
            <li><strong>Blue points (Summary plot):</strong> Low feature values push prediction toward Away (A)</li>
            <li><strong>Horizontal position:</strong> The magnitude of the SHAP value (impact on prediction)</li>
            <li><strong>Bar length:</strong> Mean absolute SHAP value indicates feature importance</li>
            <li><strong>Crowd impact:</strong> Shows how matches with/without crowds differ in feature importance</li>
          </ul>
        </div>
      </section>
    </div>
  )
}
