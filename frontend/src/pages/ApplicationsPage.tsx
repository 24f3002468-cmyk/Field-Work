import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { ApplicationResponse } from '../types';
import { Briefcase, PlusCircle, CheckCircle } from 'lucide-react';

export const ApplicationsPage: React.FC = () => {
  const [apps, setApps] = useState<ApplicationResponse[]>([]);
  const [company, setCompany] = useState('');
  const [role, setRole] = useState('ML Engineer');
  const [status, setStatus] = useState('APPLIED');

  const loadApps = async () => {
    const res = await api.get('/applications');
    setApps(res.data);
  };

  useEffect(() => {
    loadApps();
  }, []);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!company) return;
    await api.post('/applications', {
      company,
      role,
      status,
      application_date: new Date().toISOString().split('T')[0]
    });
    setCompany('');
    loadApps();
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
            <Briefcase className="w-6 h-6 text-sky-400" />
            <span>Applications & Job Hunt Pipeline (Part 2 Focus)</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">Track target roles, application status, interview rounds, and offers by April 30, 2027.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-sm font-bold text-white font-mono flex items-center space-x-2 border-b border-slate-800 pb-3">
            <PlusCircle className="w-4 h-4 text-sky-400" />
            <span>ADD APPLICATION RECORD</span>
          </h2>

          <form onSubmit={handleAdd} className="space-y-3 text-xs">
            <div>
              <label className="text-slate-400 block mb-1">Company</label>
              <input
                type="text"
                required
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                placeholder="e.g. Google, Microsoft, Startup"
                className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white focus:outline-none focus:border-sky-500"
              />
            </div>

            <div>
              <label className="text-slate-400 block mb-1">Role</label>
              <input
                type="text"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white focus:outline-none focus:border-sky-500"
              />
            </div>

            <div>
              <label className="text-slate-400 block mb-1">Pipeline Status</label>
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-2 text-white focus:outline-none focus:border-sky-500 font-mono"
              >
                <option value="TO_APPLY font-mono">TO APPLY</option>
                <option value="APPLIED">APPLIED</option>
                <option value="OA">ONLINE ASSESSMENT (OA)</option>
                <option value="TECHNICAL">TECHNICAL INTERVIEW</option>
                <option value="SYSTEM_DESIGN">SYSTEM DESIGN INTERVIEW</option>
                <option value="OFFER">OFFER RECEIVED</option>
              </select>
            </div>

            <button
              type="submit"
              className="w-full py-2.5 bg-sky-600 hover:bg-sky-500 text-white font-mono font-bold rounded-lg transition"
            >
              Save Application
            </button>
          </form>
        </div>

        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-sm font-bold text-white font-mono border-b border-slate-800 pb-3">
            APPLICATION PIPELINE ({apps.length})
          </h2>

          <div className="space-y-2 max-h-[450px] overflow-y-auto pr-1">
            {apps.map((a) => (
              <div key={a.id} className="p-3 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between text-xs">
                <div>
                  <h3 className="font-bold text-white text-sm">{a.company}</h3>
                  <span className="text-slate-400 font-mono text-[11px]">{a.role} • Applied {a.application_date}</span>
                </div>
                <span className="px-2.5 py-1 rounded bg-sky-500/20 text-sky-300 font-mono font-bold text-[11px]">
                  {a.status}
                </span>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};
