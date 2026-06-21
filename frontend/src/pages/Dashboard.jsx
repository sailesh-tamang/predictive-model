import React, {useEffect, useState} from 'react'
import axios from 'axios'
import { API } from '../api'

// Image Skeleton Loader
function ImageLoader() {
  return <div className="w-full h-64 bg-gradient-to-r from-gray-200 to-gray-300 rounded animate-pulse"></div>
}

// Image Component with Lazy Loading
function LazyImage({ src, alt, onClick }) {
  const [loaded, setLoaded] = useState(false)
  const [error, setError] = useState(false)

  if (error) {
    return <div className="text-sm text-gray-500 py-8 text-center bg-gray-100 rounded">Image failed to load</div>
  }

  return (
    <>
      {!loaded && <ImageLoader />}
      <img
        src={src}
        alt={alt}
        loading="eager"
        decoding="async"
        onLoad={() => setLoaded(true)}
        onError={() => setError(true)}
        className={`w-full rounded cursor-pointer hover:opacity-90 transition-opacity ${!loaded ? 'hidden' : ''}`}
        onClick={onClick}
      />
    </>
  )
}

export default function Dashboard(){
  const [images, setImages] = useState([])
  const [loading, setLoading] = useState(true)
  const [zoomedImage, setZoomedImage] = useState(null)

  useEffect(()=>{
    setLoading(true)
    axios.get(`${API}/images/list`, { timeout: 10000 })
      .then(r => setImages(r.data.images || []))
      .catch(err => {
        console.error('Failed to load images:', err)
        setImages([])
      })
      .finally(() => setLoading(false))
  },[])

  const find = (name) => images.find(x=> x.toLowerCase().includes(name))

  return (
    <div>
      <section className="card">
        <h2 className="text-2xl font-semibold mb-2">Analytics Dashboard</h2>
        <p className="text-gray-600 mb-6">Season-wise comparisons, pre-COVID vs COVID, team-wise analysis and crowd impact visualizations from your research.</p>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="p-6 rounded border-l-4 border-blue-500 bg-gradient-to-br from-blue-50 to-blue-100">
            <div className="text-xs text-blue-600 font-semibold uppercase tracking-wide">Home Wins (All)</div>
            <div className="text-3xl font-bold text-blue-900 mt-2">47%</div>
            <div className="text-xs text-gray-600 mt-2">2018-2022 average</div>
          </div>

          <div className="p-6 rounded border-l-4 border-green-500 bg-gradient-to-br from-green-50 to-green-100">
            <div className="text-xs text-green-600 font-semibold uppercase tracking-wide">With Crowd</div>
            <div className="text-3xl font-bold text-green-900 mt-2">50%</div>
            <div className="text-xs text-gray-600 mt-2">+3% crowd effect</div>
          </div>

          <div className="p-6 rounded border-l-4 border-red-500 bg-gradient-to-br from-red-50 to-red-100">
            <div className="text-xs text-red-600 font-semibold uppercase tracking-wide">No Crowd (COVID)</div>
            <div className="text-3xl font-bold text-red-900 mt-2">42%</div>
            <div className="text-xs text-gray-600 mt-2">2020-21 season</div>
          </div>
        </div>

        {/* Charts Grid */}
        {loading ? (
          <div className="text-center py-8 text-gray-600">Loading charts...</div>
        ) : (
          <div className="space-y-6">
            <div className="rounded-lg p-4 bg-gray-50">
              <h3 className="font-semibold mb-3 text-gray-800">Season Analysis</h3>
              {find('season') ? (
                <LazyImage src={`${API}/images/${find('season')}`} alt="season" onClick={() => setZoomedImage({src: `${API}/images/${find('season')}`, alt: 'Season Analysis'})} />
              ) : <div className="text-sm text-gray-500 py-8 text-center">Chart not available</div>}
            </div>

            <div className="rounded-lg p-4 bg-gray-50">
              <h3 className="font-semibold mb-3 text-gray-800">Team Analysis</h3>
              {find('team_analysis') ? (
                <LazyImage src={`${API}/images/${find('team_analysis')}`} alt="team" onClick={() => setZoomedImage({src: `${API}/images/${find('team_analysis')}`, alt: 'Team Analysis'})} />
              ) : <div className="text-sm text-gray-500 py-8 text-center">Chart not available</div>}
            </div>

            <div className="rounded-lg p-4 bg-gray-50">
              <h3 className="font-semibold mb-3 text-gray-800">Crowd Impact</h3>
              {find('crowd_impact') ? (
                <LazyImage src={`${API}/images/${find('crowd_impact')}`} alt="crowd impact" onClick={() => setZoomedImage({src: `${API}/images/${find('crowd_impact')}`, alt: 'Crowd Impact'})} />
              ) : <div className="text-sm text-gray-500 py-8 text-center">Chart not available</div>}
            </div>

            <div className="rounded-lg p-4 bg-gray-50">
              <h3 className="font-semibold mb-3 text-gray-800">Team Scatter</h3>
              {find('team_scatter') ? (
                <LazyImage src={`${API}/images/${find('team_scatter')}`} alt="team scatter" onClick={() => setZoomedImage({src: `${API}/images/${find('team_scatter')}`, alt: 'Team Scatter'})} />
              ) : <div className="text-sm text-gray-500 py-8 text-center">Chart not available</div>}
            </div>
          </div>
        )}

        {/* Zoom Modal */}
        {zoomedImage && (
          <div className="fixed inset-0 z-50 bg-black bg-opacity-80 flex items-center justify-center p-4" onClick={() => setZoomedImage(null)}>
            <div className="relative w-full h-full flex items-center justify-center" onClick={(e) => e.stopPropagation()}>
              <button onClick={() => setZoomedImage(null)} className="absolute top-4 right-4 bg-white rounded-full w-10 h-10 flex items-center justify-center shadow-lg hover:bg-gray-100 transition-colors z-10">
                <span className="text-2xl font-bold text-gray-700">&times;</span>
              </button>
              <img src={zoomedImage.src} alt={zoomedImage.alt} className="max-w-full max-h-full object-contain rounded-lg shadow-2xl" />
            </div>
          </div>
        )}

        {/* Interpretation */}
        <div className="mt-6 p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
          <h4 className="font-semibold text-blue-900 mb-2">Interpretation</h4>
          <p className="text-sm text-blue-800">
            The dashboards above reveal the quantifiable impact of crowd presence on home field advantage. The season-wise analysis shows consistent patterns across 2018-2022, with a notable dip during the COVID no-crowd season (2020-21). Team analysis highlights variation in crowd sensitivity across clubs.
          </p>
        </div>
      </section>
    </div>
  )
}
