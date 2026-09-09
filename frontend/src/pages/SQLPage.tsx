import React from 'react';
import { Database, CheckCircle } from 'lucide-react';

export const SQLPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-3">
        <div className="flex items-center space-x-2 text-xs font-mono text-sky-400">
          <span className="bg-sky-500/20 px-2.5 py-0.5 rounded font-bold">PART 1 MANDATORY REQUIREMENT</span>
          <span>•</span>
          <span>SEP 10 – DEC 31, 2026</span>
        </div>
        <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
          <Database className="w-6 h-6 text-sky-400" />
          <span>SQL Focus Tracker (40–50 Hours Target)</span>
        </h1>
        <p className="text-xs text-slate-400 max-w-2xl">
          SQL is explicitly a Part 1 requirement. Target: 40–50 focused hours covering Window functions, CTEs, complex Joins, Indexing, and Query Optimization.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-center">
          <span className="text-xs text-slate-400 font-mono block">TARGET HOURS</span>
          <span className="text-3xl font-black text-white font-mono mt-1 block">40 – 50 hrs</span>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-center">
          <span className="text-xs text-slate-400 font-mono block">EXECUTION PART</span>
          <span className="text-2xl font-bold text-sky-400 font-mono mt-1 block">PART 1</span>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-center">
          <span className="text-xs text-slate-400 font-mono block">PART 2 ROLE</span>
          <span className="text-sm font-semibold text-slate-300 font-mono mt-2 block">Maintain Competency</span>
        </div>
      </div>

    </div>
  );
};
