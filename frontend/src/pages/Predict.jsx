import React, {useState} from 'react'
import axios from 'axios'

const API = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

export default function Predict(){
  const [form, setForm] = useState({
    crowd_present: 1,
    HS: 10, AS:10, HST:5, AST:5, HF:10, AF:10, HC:4, AC:4, HY:1, AY:1, HR:0, AR:0
  })
  const [result, setResult] = useState(null)
  const [shap, setShap] = useState(null)
  const [shapImage, setShapImage] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [shapOptions, setShapOptions] = useState({
    sortBy: 'abs', // 'abs' | 'value' | 'feature'
    direction: 'desc', // 'asc' | 'desc'
    topK: 12,
    query: '',
    absolute: true,
  })

  const getPredictionLabel = (code) => {
    const labelMap = { 'H': 'Home Win', 'D': 'Draw', 'A': 'Away Win' }
    return labelMap[code] || code
  }

  const getPredictionColor = (code) => {
    if (code === 'H') return 'text-green-700'
    if (code === 'D') return 'text-yellow-700'
    if (code === 'A') return 'text-red-700'
    return 'text-blue-700'
  }

  const getPredictionBgColor = (code) => {
    if (code === 'H') return 'from-green-50 to-emerald-50 border-green-500'
    if (code === 'D') return 'from-yellow-50 to-amber-50 border-yellow-500'
    if (code === 'A') return 'from-red-50 to-rose-50 border-red-500'
    return 'from-blue-50 to-indigo-50 border-blue-500'
  }

  const getBarColor = (code) => {
    if (code === 'H') return 'bg-green-600'
    if (code === 'D') return 'bg-yellow-500'
    if (code === 'A') return 'bg-red-600'
    return 'bg-blue-600'
  }

  function onChange(e){
    const {name, value} = e.target
    setForm(s => ({...s, [name]: value}))
  }

  async function submit(e){
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    setShap(null)
    setShapImage(null)

    try{
      const resp = await axios.post(`${API}/predict`, form)
      setResult(resp.data)

      // request SHAP explanation
      try{
        const sresp = await axios.post(`${API}/shap`, form)
        setShap(sresp.data)
      }catch(sErr){
        setShap({error: sErr.response?.data || sErr.message})
      }

      // request SHAP plot image (optional)
      try{
        const presp = await axios.post(`${API}/shap_plot`, form, { responseType: 'blob' })
        const url = URL.createObjectURL(presp.data)
        setShapImage(url)
      }catch(pErr){
        // plot generation optional, don't error
      }

    }catch(err){
      const errMsg = err.response?.data?.error || err.message
      setError(errMsg)
      setResult({error: err.response?.data || err.message})
    }finally{
      setLoading(false)
    }
  }

  const renderShap = () => {
    if(!shap) return null
      if(shap.error) return <div className="mt-4 p-4 bg-yellow-50 border border-yellow-300 rounded text-yellow-800 text-sm">⚠ SHAP contributions unavailable. See plot below.</div>
    const items = shap.feature_names.map((f,i)=> ({feature:f, val: parseFloat(shap.shap_values[i]) || 0}))

    // filter by query
    const q = shapOptions.query.trim().toLowerCase()
    let filtered = items.filter(it => !q || it.feature.toLowerCase().includes(q))

    // sort
    if(shapOptions.sortBy === 'abs'){
      filtered.sort((a,b)=> Math.abs(b.val) - Math.abs(a.val))
    } else if(shapOptions.sortBy === 'value'){
      filtered.sort((a,b)=> b.val - a.val)
    } else {
      filtered.sort((a,b)=> a.feature.localeCompare(b.feature))
    }
    if(shapOptions.direction === 'asc') filtered.reverse()

    // top K
    filtered = filtered.slice(0, shapOptions.topK)

    const max = Math.max(...filtered.map(i=> Math.abs(i.val)), 0.0001)

    return (
      <div className="mt-4 p-4 bg-gray-50 rounded border">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-semibold text-sm text-gray-800">SHAP Contributions (pred: {shap.predicted_label || shap.predicted_class_index})</h3>
          <div className="flex items-center space-x-2 text-xs flex-wrap gap-2">
            <input placeholder="Search feature" value={shapOptions.query} onChange={e=> setShapOptions(s=>({...s, query: e.target.value}))} className="border border-gray-300 p-1 rounded" />
            <select value={shapOptions.sortBy} onChange={e=> setShapOptions(s=>({...s, sortBy: e.target.value}))} className="border border-gray-300 p-1 rounded text-xs">
              <option value="abs">|SHAP|</option>
              <option value="value">SHAP</option>
              <option value="feature">Name</option>
            </select>
            <select value={shapOptions.direction} onChange={e=> setShapOptions(s=>({...s, direction: e.target.value}))} className="border border-gray-300 p-1 rounded text-xs">
              <option value="desc">↓</option>
              <option value="asc">↑</option>
            </select>
            <input type="number" min={1} max={shap.feature_names.length} value={shapOptions.topK} onChange={e=> setShapOptions(s=>({...s, topK: Math.max(1, Number(e.target.value)||1)}))} className="w-12 border border-gray-300 p-1 rounded text-xs" />
            <label className="text-xs"><input type="checkbox" checked={shapOptions.absolute} onChange={e=> setShapOptions(s=>({...s, absolute: e.target.checked}))} className="mr-1" /> Abs</label>
          </div>
        </div>

        <div className="space-y-2 max-h-80 overflow-y-auto">
          {filtered.map(it=> (
            <div key={it.feature} className="flex items-center space-x-2">
              <div className="w-32 text-xs text-gray-700 truncate">{it.feature}</div>
              <div className="flex-1 bg-gray-200 rounded h-4 relative overflow-hidden">
                <div className={`h-4 ${it.val>=0? 'bg-green-500':'bg-red-500'}`} style={{width: `${(shapOptions.absolute? Math.abs(it.val): it.val)/max*100}%`}} />
              </div>
              <div className="w-16 text-xs text-gray-700 text-right">{it.val.toFixed(3)}</div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <form onSubmit={submit} className="card">
        <h2 className="text-xl font-semibold mb-2">Match Prediction Form</h2>
        <p className="text-sm text-gray-600 mb-4">Enter match statistics to predict the outcome and see SHAP explanations.</p>

        <label className="block mb-4">
          <span className="block text-sm font-semibold text-gray-700 mb-1">Crowd Present</span>
          <select name="crowd_present" value={form.crowd_present} onChange={onChange} className="block w-full border border-gray-300 p-2 rounded hover:border-primary-600" aria-label="Crowd Present">
            <option value={1}>Yes</option>
            <option value={0}>No</option>
          </select>
        </label>

        <div className="grid grid-cols-3 gap-2 mb-6">
          {['HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR'].map(k => (
            <label className="block" key={k}>
              <span className="block text-xs font-semibold text-gray-700 mb-1">{k}</span>
              <input name={k} value={form[k]} onChange={onChange} type="number" className="block w-full border border-gray-300 p-2 rounded text-sm hover:border-primary-600" aria-label={k} />
            </label>
          ))}
        </div>

        <button disabled={loading} className="btn-primary w-full flex items-center justify-center" aria-busy={loading}>
          {loading && <div className="inline-block animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>}
          {loading ? 'Predicting...' : 'Predict Match'}
        </button>
      </form>

      <div className="card">
        <h2 className="text-xl font-semibold mb-2">Prediction Result</h2>
        {loading ? (
          <div className="text-center py-12 text-gray-600">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-3"></div>
            <p className="text-sm">Computing prediction and SHAP explanation...</p>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-300 rounded p-4 text-red-800">
            <p className="font-semibold text-sm mb-1">Error occurred</p>
            <p className="text-xs">{error}</p>
          </div>
        ) : result ? (
          result.error ? (
            <div className="bg-red-50 border border-red-300 rounded p-4 text-red-800">
              <pre className="text-xs overflow-x-auto">{JSON.stringify(result, null, 2)}</pre>
            </div>
          ) : (
            <div>
              <div className={`mb-4 p-4 bg-gradient-to-r ${getPredictionBgColor(result.predicted)} border-l-4 rounded`}>
                <p className="text-xs text-gray-700 font-semibold uppercase tracking-wide">Predicted Outcome</p>
                <p className={`text-3xl font-bold ${getPredictionColor(result.predicted)} mt-1`}>{getPredictionLabel(result.predicted)}</p>
                <p className="text-sm text-gray-600 mt-2">Confidence: <span className="font-bold text-lg">{(result.confidence*100).toFixed(1)}%</span></p>
              </div>

              <div className="mb-4 p-4 bg-gray-50 rounded border">
                <h3 className="font-semibold mb-3 text-sm text-gray-800">Match Outcome Probabilities</h3>
                <div className="space-y-3">
                  {Object.entries(result.probabilities).map(([label, prob])=> (
                    <div key={label} className="flex items-center space-x-3">
                      <div className="w-24 text-sm font-bold text-gray-700">{getPredictionLabel(label)}</div>
                      <div className="flex-1 bg-gray-200 rounded h-5 relative overflow-hidden">
                        <div className={`${getBarColor(label)} h-5 rounded transition-all`} style={{width: `${prob*100}%`}} />
                      </div>
                      <div className="w-12 text-sm font-semibold text-gray-700 text-right">{(prob*100).toFixed(1)}%</div>
                    </div>
                  ))}
                </div>
              </div>

              {renderShap()}

              {shapImage ? (
                <div className="mt-4">
                  <h4 className="font-semibold mb-3 text-sm text-gray-800">SHAP Feature Importance Plot</h4>
                  <img src={shapImage} alt="shap plot" className="w-full border border-gray-300 rounded" />
                  <div className="mt-2">
                    <a href={shapImage} download="shap_plot.png" className="text-xs text-blue-600 hover:underline">📥 Download PNG</a>
                  </div>
                </div>
              ) : null}
            </div>
          )
        ) : <p className="text-gray-600 text-center py-8">Submit match statistics above to see predictions and explanations.</p>}
      </div>
    </div>
  )
}
