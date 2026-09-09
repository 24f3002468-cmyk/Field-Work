import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Milestone } from '../types';
import { Calendar, Flag, CheckCircle, Clock } from 'lucide-react';

export const PlannerPage: React.FC = () => {
  const [milestones, setMilestones] = useState<Milestone[]>([]);
  const [selectedDay, setSelectedDay] = useState<number | null>(1);
  const [dayDetail, setDayDetail] = useState<any>(null);

  useEffect(() => {
    api.get('/planner/milestones').then((res) => setMilestones(res.data));
  }, []);

  useEffect(() => {
    if (selectedDay) {
      api.get(`/planner/day/${selectedDay}`).then((res) => setDayDetail(res.data));
    }
  }, [selectedDay]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h1 className="text-2xl font-bold text-white">200-Day Execution Calendar & Heatmap</h1>
        <p className="text-xs text-slate-400 mt-1">Immutable master calendar mapped strictly from Sep 10, 2026 to Apr 30, 2027.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* 200-Day Heatmap Grid */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h2 className="text-sm font-bold text-white font-mono flex items-center space-x-2">
              <Calendar className="w-4 h-4 text-sky-400" />
              <span>200 EXECUTION DAYS GRID</span>
            </h2>
            <div className="flex items-center space-x-3 text-xs font-mono text-slate-400">
              <span className="flex items-center space-x-1"><span className="w-3 h-3 bg-sky-900 border border-sky-500 rounded-sm" /><span>Part 1</span></span>
              <span className="flex items-center space-x-1"><span className="w-3 h-3 bg-indigo-900 border border-indigo-500 rounded-sm" /><span>Part 2</span></span>
            </div>
          </div>

          <div className="grid grid-cols-10 sm:grid-cols-20 gap-1.5 max-h-96 overflow-y-auto p-1">
            {Array.from({ length: 200 }, (_, i) => i + 1).map((dayNum) => {
              const isPart1 = dayNum <= 113;
              const isSelected = selectedDay === dayNum;
              return (
                <button
                  key={dayNum}
                  onClick={() => setSelectedDay(dayNum)}
                  className={`h-7 rounded text-[10px] font-mono font-bold transition flex items-center justify-center border ${
                    isSelected
                      ? 'bg-sky-500 text-white ring-2 ring-sky-300 border-white'
                      : isPart1
                      ? 'bg-sky-950/60 text-sky-300 border-sky-800 hover:border-sky-500'
                      : 'bg-indigo-950/60 text-indigo-300 border-indigo-800 hover:border-indigo-500'
                  }`}
                >
                  {dayNum}
                </button>
              );
            })}
          </div>

          {/* Selected Day Inspector */}
          {dayDetail && (
            <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 mt-4 space-y-3">
              <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                <div>
                  <span className="text-xs font-mono text-sky-400 font-bold">DAY {dayDetail.day_number} OF 200</span>
                  <h3 className="text-base font-bold text-white">{dayDetail.date} ({dayDetail.weekday})</h3>
                </div>
                <span className="text-xs px-2.5 py-1 rounded font-mono font-semibold bg-slate-800 text-slate-300">
                  PART {dayDetail.part} • {dayDetail.phase}
                </span>
              </div>

              <div className="space-y-2">
                {dayDetail.tasks?.map((t: any) => (
                  <div key={t.id} className="p-2.5 bg-slate-900 border border-slate-800 rounded-lg flex items-center justify-between text-xs">
                    <div>
                      <span className="font-mono text-sky-400 font-semibold">{t.planned_start} - {t.planned_end}</span>
                      <span className="ml-2 font-bold text-white">{t.name}</span>
                      <p className="text-[11px] text-slate-400 mt-0.5">{t.description}</p>
                    </div>
                    <span className="font-mono text-slate-400">{t.planned_minutes} min</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Milestones Engine */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-sm font-bold text-white font-mono flex items-center space-x-2 border-b border-slate-800 pb-3">
            <Flag className="w-4 h-4 text-emerald-400" />
            <span>CRITICAL MILESTONES TRACKER</span>
          </h2>

          <div className="space-y-3 max-h-[500px] overflow-y-auto pr-1">
            {milestones.map((m) => (
              <div
                key={m.id}
                className={`p-3 rounded-lg border space-y-1.5 transition ${
                  m.critical
                    ? 'bg-slate-950 border-rose-500/40'
                    : 'bg-slate-950 border-slate-800'
                }`}
              >
                <div className="flex items-center justify-between text-xs">
                  <span className="font-mono text-sky-400 font-bold">Target Day {m.target_day} ({m.target_date})</span>
                  {m.critical && (
                    <span className="text-[10px] font-bold px-1.5 py-0.5 bg-rose-500/20 text-rose-300 rounded border border-rose-500/30">
                      CRITICAL
                    </span>
                  )}
                </div>
                <h3 className="text-xs font-bold text-white">{m.name}</h3>
                <p className="text-[11px] text-slate-400">{m.description}</p>
                <div className="text-[11px] font-mono text-slate-500 flex justify-between pt-1">
                  <span>Phase: {m.phase}</span>
                  <span className="uppercase font-bold text-slate-300">{m.status}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};
