import React from 'react';
import { useDashboardStore } from '../store/useDashboardStore';
import { Clock, Play, CheckCircle, AlertCircle } from 'lucide-react';

export const WhatShouldIDoNow: React.FC = () => {
  const { today, completeTask } = useDashboardStore();

  if (!today) return null;

  const activeTask = today.active_task_now;
  const current_time = today.current_time;

  return (
    <div className="bg-gradient-to-r from-slate-900 via-sky-950 to-slate-900 border border-sky-500/30 rounded-xl p-5 shadow-xl">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 rounded-full bg-emerald-400 animate-ping" />
          <h2 className="text-xs font-mono font-bold uppercase tracking-wider text-sky-400">
            WHAT SHOULD I DO NOW?
          </h2>
        </div>
        <div className="flex items-center space-x-1.5 text-slate-400 text-xs font-mono bg-slate-800/80 px-2.5 py-1 rounded-md">
          <Clock className="w-3.5 h-3.5 text-sky-400" />
          <span>Current Time: {current_time}</span>
        </div>
      </div>

      {activeTask ? (
        <div className="bg-slate-900/90 border border-sky-500/40 rounded-lg p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-semibold px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 font-mono">
                {activeTask.planned_start} – {activeTask.planned_end}
              </span>
              <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-medium">
                {activeTask.category}
              </span>
              {activeTask.is_critical && (
                <span className="text-xs px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-semibold border border-rose-500/30">
                  CRITICAL
                </span>
              )}
            </div>
            <h3 className="text-lg font-bold text-white mt-1">{activeTask.name}</h3>
            <p className="text-xs text-slate-400 mt-0.5">{activeTask.description}</p>
          </div>

          <div className="flex items-center space-x-2 shrink-0">
            <button
              onClick={() => completeTask(activeTask.id, activeTask.planned_minutes, 'COMPLETED')}
              className="flex items-center space-x-1.5 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold transition shadow-lg shadow-emerald-900/40"
            >
              <CheckCircle className="w-4 h-4" />
              <span>Mark Complete</span>
            </button>
          </div>
        </div>
      ) : (
        <div className="bg-slate-900/60 border border-slate-800 rounded-lg p-4 text-center md:text-left flex flex-col md:flex-row items-center justify-between">
          <div>
            <span className="text-xs text-slate-400 font-mono">SCHEDULE STATUS</span>
            <p className="text-sm font-semibold text-slate-200 mt-0.5">
              No active study task scheduled right now. Next: Daily Scorecard at 10:00 PM.
            </p>
          </div>
          <div className="mt-3 md:mt-0 text-xs text-slate-400 font-mono bg-slate-800 px-3 py-1.5 rounded">
            College window (09:00–16:00) strictly preserved.
          </div>
        </div>
      )}
    </div>
  );
};
