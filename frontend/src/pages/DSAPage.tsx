import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { DSASummary } from '../types';
import { Code, Award, PlusCircle } from 'lucide-react';

export const DSAPage: React.FC = () => {
  const [summary, setSummary] = useState<DSASummary | null>(null);
  const [problems, setProblems] = useState<any[]>([]);
  const [title, setTitle] = useState('');
  const [difficulty, setDifficulty] = useState('Medium');
  const [topic, setTopic] = useState('Arrays & Hashing');
  const [solveTime, setSolveTime] = useState(25);

  const loadData = async () => {
    const sRes = await api.get('/dsa/summary');
    const pRes = await api.get('/dsa');
    setSummary(sRes.data);
    setProblems(pRes.data);
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title) return;
    await api.post('/dsa/problems', {
      title,
      difficulty,
      topic,
      platform: 'LeetCode',
      status: 'solved',
      solve_time_minutes: solveTime,
      solved_date: new Date().toISOString().split('T')[0]
    });
    setTitle('');
    loadData();
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
            <Code className="w-6 h-6 text-sky-400" />
            <span>DSA & LeetCode Progress Engine</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">Primary Target: 50–60 solid Medium-level problems mastered with review notes.</p>
        </div>

        <div className="bg-slate-950 px-4 py-2.5 rounded-lg border border-slate-800 font-mono text-xs flex items-center space-x-4">
          <div>
            <span className="text-slate-400 block">MEDIUM SOLVED</span>
            <span className="text-emerald-400 font-black text-lg">{summary?.medium_solved || 0} / 50</span>
          </div>
          <div className="h-6 w-px bg-slate-800" />
          <div>
            <span className="text-slate-400 block">STRETCH TARGET</span>
            <span className="text-sky-400 font-bold text-base">60 Mediums</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Record Problem Form */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-sm font-bold text-white font-mono flex items-center space-x-2 border-b border-slate-800 pb-3">
            <PlusCircle className="w-4 h-4 text-emerald-400" />
            <span>LOG SOLVED DSA PROBLEM</span>
          </h2>

          <form onSubmit={handleAdd} className="space-y-3 text-xs">
            <div>
              <label className="text-slate-400 block mb-1">Problem Title</label>
              <input
                type="text"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. 3Sum / Product of Array Except Self"
                className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white focus:outline-none focus:border-sky-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-slate-400 block mb-1">Difficulty</label>
                <select
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-2 text-white focus:outline-none focus:border-sky-500"
                >
                  <option value="Easy">Easy</option>
                  <option value="Medium">Medium</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>

              <div>
                <label className="text-slate-400 block mb-1">Solve Time (Mins)</label>
                <input
                  type="number"
                  value={solveTime}
                  onChange={(e) => setSolveTime(parseInt(e.target.value) || 0)}
                  className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white focus:outline-none focus:border-sky-500"
                />
              </div>
            </div>

            <div>
              <label className="text-slate-400 block mb-1">Topic</label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g. Two Pointers, Binary Search, Trees"
                className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white focus:outline-none focus:border-sky-500"
              />
            </div>

            <button
              type="submit"
              className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-mono font-bold rounded-lg transition"
            >
              Record Problem
            </button>
          </form>
        </div>

        {/* Problems Log Table */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-sm font-bold text-white font-mono border-b border-slate-800 pb-3">
            RECORDED SOLVED PROBLEMS ({problems.length})
          </h2>

          <div className="space-y-2 max-h-[450px] overflow-y-auto pr-1">
            {problems.map((p) => (
              <div key={p.id} className="p-3 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between text-xs">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-0.5 rounded font-mono font-bold ${
                      p.difficulty === 'Medium' ? 'bg-amber-500/20 text-amber-300' : (p.difficulty === 'Hard' ? 'bg-rose-500/20 text-rose-300' : 'bg-emerald-500/20 text-emerald-300')
                    }`}>
                      {p.difficulty}
                    </span>
                    <span className="font-bold text-white">{p.title}</span>
                  </div>
                  <span className="text-slate-400 font-mono text-[11px] mt-0.5 block">{p.topic} • Solved on {p.solved_date}</span>
                </div>
                <span className="font-mono text-slate-400">{p.solve_time_minutes} mins</span>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};
