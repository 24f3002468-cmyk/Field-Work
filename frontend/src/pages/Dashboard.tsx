import React, { useEffect } from 'react';
import { useDashboardStore } from '../store/useDashboardStore';
import { WhatShouldIDoNow } from '../components/WhatShouldIDoNow';
import { AlertTriangle, CheckCircle2, Clock, Calendar, ArrowRight, ShieldCheck, Target, Award } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Dashboard: React.FC = () => {
  const { today, backlog, projectStatus, dsaSummary, pointsSummary, fetchToday, fetchBacklog, fetchProjectStatus, fetchDSASummary, fetchPointsSummary } = useDashboardStore();

  useEffect(() => {
    fetchToday();
    fetchBacklog();
    fetchProjectStatus();
    fetchDSASummary();
    fetchPointsSummary();
  }, []);

  if (!today) {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
        <div className="animate-spin w-8 h-8 border-4 border-sky-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  const criticalTasks = today.tasks.filter(t => t.is_critical);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      
      {/* WHAT SHOULD I DO NOW */}
      <WhatShouldIDoNow />

      {/* 1. WHERE AM I */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>EXECUTION DAY</span>
            <span className="bg-sky-500/20 text-sky-400 px-2 py-0.5 rounded font-bold">PART {today.part}</span>
          </div>
          <div className="mt-2">
            <span className="text-3xl font-black text-white font-mono">DAY {today.day_number}</span>
            <span className="text-slate-400 text-sm font-mono"> / 200</span>
          </div>
          <p className="text-xs text-slate-400 mt-1 font-medium">{today.phase}</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>PROJECT 1 SHIPPING</span>
            <Target className="w-4 h-4 text-sky-400" />
          </div>
          <div className="mt-2">
            <span className="text-2xl font-bold text-white">{projectStatus?.ship_status || 'NOT SHIPPED'}</span>
          </div>
          <p className="text-xs text-slate-400 mt-1 font-mono">Deadline: Dec 22, 2026</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>DSA MEDIUM TARGET</span>
            <Award className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="mt-2 font-mono">
            <span className="text-3xl font-black text-emerald-400">{dsaSummary?.medium_solved || 0}</span>
            <span className="text-slate-400 text-sm"> / 50 min</span>
          </div>
          <p className="text-xs text-slate-400 mt-1 font-mono">Stretch target: 60 Mediums</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>PLACEMENT POINTS</span>
            <BookOpen className="w-4 h-4 text-purple-400 text-xs" />
          </div>
          <div className="mt-2 font-mono">
            <span className="text-3xl font-black text-purple-400">{pointsSummary?.earned_points || 0}</span>
            <span className="text-slate-400 text-sm"> / {pointsSummary?.required_points || 50}</span>
          </div>
          <p className="text-xs text-slate-400 mt-1 font-mono">IITM Eligible Activities</p>
        </div>
      </div>

      {/* 2. AM I ON TRACK & CRITICAL PRIORITIES */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Today's Tasks */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h2 className="text-base font-bold text-white flex items-center space-x-2">
                <Clock className="w-4 h-4 text-sky-400" />
                <span>TODAY'S SCHEDULED TASKS</span>
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">{today.today_date} ({today.tasks.length} planned tasks)</p>
            </div>
            <Link to="/today" className="text-xs text-sky-400 hover:text-sky-300 font-medium flex items-center space-x-1">
              <span>View Execution Log</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-2.5">
            {today.tasks.map((task) => (
              <div
                key={task.id}
                className={`p-3.5 rounded-lg border flex items-center justify-between transition ${
                  task.status === 'COMPLETED'
                    ? 'bg-slate-900/50 border-emerald-500/30 text-slate-400'
                    : 'bg-slate-950 border-slate-800 text-slate-200 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <div
                    className={`w-2.5 h-2.5 rounded-full ${
                      task.status === 'COMPLETED'
                        ? 'bg-emerald-400'
                        : task.is_critical
                        ? 'bg-rose-500 animate-pulse'
                        : 'bg-sky-400'
                    }`}
                  />
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="text-xs font-mono font-semibold px-2 py-0.5 bg-slate-800 rounded text-slate-300">
                        {task.planned_start} - {task.planned_end}
                      </span>
                      <span className="text-xs font-medium text-slate-400">{task.category}</span>
                      {task.is_critical && (
                        <span className="text-[10px] font-bold px-1.5 py-0.5 bg-rose-500/20 text-rose-300 rounded border border-rose-500/30">
                          CRITICAL
                        </span>
                      )}
                    </div>
                    <p className={`text-sm font-semibold mt-1 ${task.status === 'COMPLETED' ? 'line-through text-slate-500' : 'text-white'}`}>
                      {task.name}
                    </p>
                  </div>
                </div>

                <div className="text-right font-mono text-xs">
                  <span className={task.status === 'COMPLETED' ? 'text-emerald-400 font-bold' : 'text-slate-400'}>
                    {task.status}
                  </span>
                  <span className="block text-[11px] text-slate-500">{task.planned_minutes} min</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Backlog & Priorities */}
        <div className="space-y-6">
          
          {/* Backlog Status */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2.5">
              <h2 className="text-sm font-bold text-white flex items-center space-x-2">
                <AlertTriangle className={`w-4 h-4 ${(backlog?.overdue_count || 0) > 0 ? 'text-amber-400' : 'text-emerald-400'}`} />
                <span>ACCUMULATED BACKLOG</span>
              </h2>
              <span className={`text-xs font-mono px-2 py-0.5 rounded font-bold ${(backlog?.overdue_count || 0) > 0 ? 'bg-amber-500/20 text-amber-300' : 'bg-emerald-500/20 text-emerald-300'}`}>
                {backlog?.overdue_count || 0} overdue
              </span>
            </div>

            <p className="text-xs text-slate-400 leading-relaxed">
              {backlog?.catch_up_recommendation || 'No overdue backlog. Keep up the high execution standards!'}
            </p>

            {(backlog?.critical_overdue_tasks?.length || 0) > 0 && (
              <div className="bg-rose-950/40 border border-rose-500/30 rounded-lg p-3">
                <span className="text-xs font-bold text-rose-300 block mb-1">CRITICAL OVERDUE:</span>
                {backlog?.critical_overdue_tasks.slice(0, 3).map((ct) => (
                  <div key={ct.id} className="text-xs text-rose-200 py-0.5 flex justify-between font-mono">
                    <span>• {ct.name}</span>
                    <span>Day {ct.day_number}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Critical Priority Focus */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <h2 className="text-sm font-bold text-white flex items-center space-x-2 border-b border-slate-800 pb-2.5">
              <Target className="w-4 h-4 text-sky-400" />
              <span>TOP 3 CRITICAL PRIORITIES TODAY</span>
            </h2>

            <div className="space-y-2">
              {criticalTasks.slice(0, 3).map((ct, idx) => (
                <div key={ct.id} className="p-2.5 bg-slate-950 border border-slate-800 rounded-lg flex items-center space-x-3">
                  <span className="w-5 h-5 rounded-full bg-sky-500/20 text-sky-400 flex items-center justify-center text-xs font-bold font-mono">
                    {idx + 1}
                  </span>
                  <div className="text-xs">
                    <p className="font-semibold text-white">{ct.name}</p>
                    <span className="text-slate-400 font-mono">{ct.category} • {ct.planned_minutes} min</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>

    </div>
  );
};
