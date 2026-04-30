import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Predict from './pages/Predict'
import Dashboard from './pages/Dashboard'
import SHAP from './pages/SHAP'
import About from './pages/About'

export default function App(){
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <nav className="bg-white shadow-sm sticky top-0 z-50">
        <div className="container-max flex items-center justify-between py-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-md bg-gradient-to-br from-primary to-brand flex items-center justify-center text-white font-bold shadow">E</div>
            <div>
              <div className="text-lg font-semibold">EPL Crowd Impact</div>
              <div className="text-xs muted">Research dashboard & predictions</div>
            </div>
          </div>

          <div className="hidden md:flex items-center space-x-3">
            <Link to="/" className="px-3 py-2 rounded hover:bg-gray-100">Home</Link>
            <Link to="/predict" className="px-3 py-2 rounded hover:bg-gray-100">Predict</Link>
            <Link to="/dashboard" className="px-3 py-2 rounded hover:bg-gray-100">Dashboard</Link>
            <Link to="/shap" className="px-3 py-2 rounded hover:bg-gray-100">SHAP</Link>
            <Link to="/about" className="px-3 py-2 rounded hover:bg-gray-100">About</Link>
          </div>

          <div className="md:hidden text-sm muted">Menu</div>
        </div>
      </nav>

      <main className="container-max py-8 flex-1">
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/predict" element={<Predict/>} />
          <Route path="/dashboard" element={<Dashboard/>} />
          <Route path="/shap" element={<SHAP/>} />
          <Route path="/about" element={<About/>} />
        </Routes>
      </main>

      <footer className="bg-slate-800 text-white border-t border-slate-700">
        <div className="container-max px-4 py-3 text-xs flex flex-col md:flex-row md:items-center md:justify-between gap-2">
          <div>EPL Crowd Impact — Final Year Thesis</div>
          <div className="md:text-right">Analyzing the Impact of Crowd Presence on Home Field Advantage in the Premier League</div>
        </div>
      </footer>
    </div>
  )
}
