import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { PlacementPointsSummary } from '../types';
import { BookOpen, Award, CheckCircle, PlusCircle } from 'lucide-react';

export const IITMPage: React.FC = () => {
  const [summary, setSummary] = useState<PlacementPointsSummary | null>(null);
  const [activity, setActivity] = useState('');
  const [category, setCategory] = useState('Certificate');
  const [points, setPoints] = useState(5);

  const loadPoints = async () => {
    const res = await api.get('/placement-points/summary');
    setSummary(res.data);
  };

  useEffect(() => {
    loadPoints();
  }, []);

  const handleAddPoint = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activity) return;
    await api.post('/placement-points', {
      activity_name: activity,
      category,
      points,
      status: 'Verified',
      date: new Date().toISOString().split('T')[0]
    });
    setActivity('');
    loadPoints();
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
            <BookOpen className="w-6 h-6 text-purple-400" />
            <span>IITM Academic & Placement Points Tracker</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">Dedicated academic tracking for IITM coursework, assignments, and eligible Placement Points.</p>
        </div>

        <div className="bg-slate-950 px-4 py-2.5 rounded-lg border border-slate-800 font-mono text-xs flex items-center space-x-4">
          <div>
            <span className="text-slate-400 block">EARNED POINTS</span>
            <span className="text-purple-400 font-black text-lg">{summary?.earned_points || 0} / {summary?.required_points || 50}</span>
          </div>
          <div className="h-6 w-px bg-slate-800" />
          <div>
            <span className="text-slate-400 block">REMAINING</span>
            <span className="text-amber-400 font-bold text-base">{summary?.remaining_points || 0} pts</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Record Placement Point Form */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-sm font-bold text-white font-mono flex items-center space-x-2 border-b border-slate-800 pb-3">
            <PlusCircle className="w-4 h-4 text-purple-400" />
            <span>LOG IITM PLACEMENT POINT</span>
          </h2>

          <form onSubmit={handleAddPoint} className="space-y-3 text-xs">
            <div>
              <label className="text-slate-400 block mb-1">Eligible Activity Name</label>
              <input
                type="text"
                required
                value={activity}
                onChange={(e) => setActivity(e.target.value)}
                placeholder="e.g. NPTEL Certificate / Coding Competition"
                className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white focus:outline-none focus:border-purple-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-slate-400 block mb-1">Category</label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-2 text-white focus:outline-none focus:border-purple-500"
                >
                  <option value="Certificate">Certificate</option>
                  <option value="Problem Solving">Problem Solving</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div>
                <label className="text-slate-400 block mb-1">Points Earned</label>
                <input
                  type="number"
                  value={points}
                  onChange={(e) => setPoints(parseInt(e.target.value) || 0)}
                  className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white focus:outline-none focus:border-purple-500"
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full py-2.5 bg-purple-600 hover:bg-purple-500 text-white font-mono font-bold rounded-lg transition"
            >
              Add Placement Points
            </button>
          </form>
        </div>

        {/* Breakdown Card */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-sm font-bold text-white font-mono border-b border-slate-800 pb-3">
            POINTS BREAKDOWN & ELIGIBILITY STATUS
          </h2>

          <div className="grid grid-cols-3 gap-4 font-mono text-center">
            <div className="bg-slate-950 p-4 border border-slate-800 rounded-lg">
              <span className="text-xs text-slate-400 block">Certificates</span>
              <span className="text-2xl font-bold text-sky-400 mt-1 block">{summary?.certificates || 0} pts</span>
            </div>
            <div className="bg-slate-950 p-4 border border-slate-800 rounded-lg">
              <span className="text-xs text-slate-400 block">Problem Solving</span>
              <span className="text-2xl font-bold text-emerald-400 mt-1 block">{summary?.problem_solving || 0} pts</span>
            </div>
            <div className="bg-slate-950 p-4 border border-slate-800 rounded-lg">
              <span className="text-xs text-slate-400 block">Other Activities</span>
              <span className="text-2xl font-bold text-purple-400 mt-1 block">{summary?.other_activities || 0} pts</span>
            </div>
          </div>
        </div>
      </div>

    </div>
  );
};
