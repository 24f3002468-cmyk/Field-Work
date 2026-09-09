import React, { useState } from 'react';
import { useDashboardStore } from '../store/useDashboardStore';
import { CheckCircle2, XCircle, Clock, Save, Sparkles, Dumbbell, Moon, Sun } from 'lucide-react';
import { api } from '../services/api';

export const TodayPage: React.FC = () => {
  const { today, completeTask, fetchToday } = useDashboardStore();
  const [actuals, setActuals] = useState<Record<string, number>>({});
  const [notes, setNotes] = useState<Record<string, string>>({});
  
  // Daily scorecard state
  const [workout, setWorkout] = useState<boolean>(false);
  const [sleepHours, setSleepHours] = useState<number>(7.5);
  const [focusHours, setFocusHours] = useState<number>(4.5);
  const [blockers, setBlockers] = useState<string>('');
  const [tomorrowPriority, setTomorrowPriority] = useState<string>('');
  const [logSubmitted, setLogSubmitted] = useState<boolean>(false);

  if (!today) return null;

  const handleStatusChange = (taskId: string, status: string, plannedMins: number) => {
    const mins = actuals[taskId] !== undefined ? actuals[taskId] : plannedMins;
    const note = notes[taskId] || '';
    completeTask(taskId, mins, status, note);
  };

  const handleScorecardSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/daily-logs', {
        date: today.today_date,
        day_number: today.day_number,
        score: 8.5,
        workout_completed: workout,
        sleep_hours: sleepHours,
        focus_hours: focusHours,
        blockers,
        tomorrow_priority: tomorrowPriority,
        notes: 'Submitted via Daily Scorecard'
      });
      setLogSubmitted(true);
      fetchToday();
    } catch (err) {
      console.error('Scorecard submission failed');
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs text-slate-400 font-mono">
            <span>{today.today_date}</span>
            <span>•</span>
            <span className="text-sky-400 font-bold">DAY {today.day_number} OF 200</span>
            <span>•</span>
            <span>PART {today.part} ({today.phase})</span>
          </div>
          <h1 className="text-2xl font-bold text-white mt-1">Daily Execution Engine</h1>
          <p className="text-xs text-slate-400 mt-0.5">Strict adherence to morning routine & post-college study blocks.</p>
        </div>

        <div className="flex items-center space-x-4 bg-slate-950 px-4 py-2.5 rounded-lg border border-slate-800 font-mono text-xs">
          <div>
            <span className="text-slate-400 block">PLANNED TIME</span>
            <span className="text-white font-bold">{Math.round(today.total_planned_minutes / 60 * 10) / 10} hrs</span>
          </div>
          <div className="h-6 w-px bg-slate-800" />
          <div>
            <span className="text-slate-400 block">ACTUAL SPENT</span>
            <span className="text-emerald-400 font-bold">{Math.round(today.actual_minutes / 60 * 10) / 10} hrs</span>
          </div>
        </div>
      </div>

      {/* Routine schedule visualization */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <h2 className="text-sm font-bold text-white uppercase tracking-wider font-mono flex items-center space-x-2 border-b border-slate-800 pb-3">
          <Clock className="w-4 h-4 text-sky-400" />
          <span>FIXED DAILY TIMELINE & TASK TRACKER</span>
        </h2>

        <div className="space-y-3">
          {today.tasks.map((task) => (
            <div
              key={task.id}
              className={`p-4 rounded-xl border flex flex-col md:flex-row md:items-center justify-between gap-4 transition ${
                task.status === 'COMPLETED'
                  ? 'bg-slate-900/60 border-emerald-500/30'
                  : 'bg-slate-950 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="space-y-1">
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30">
                    {task.planned_start} - {task.planned_end}
                  </span>
                  <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-medium font-mono">
                    {task.category}
                  </span>
                  {task.is_critical && (
                    <span className="text-[10px] font-bold px-2 py-0.5 bg-rose-500/20 text-rose-300 rounded border border-rose-500/30">
                      CRITICAL
                    </span>
                  )}
                </div>
                <h3 className="text-base font-bold text-white">{task.name}</h3>
                <p className="text-xs text-slate-400">{task.description}</p>
              </div>

              <div className="flex flex-wrap items-center gap-3">
                {/* Actual minutes input */}
                <div className="flex items-center space-x-1.5 font-mono text-xs bg-slate-900 px-3 py-1.5 rounded border border-slate-800">
                  <span className="text-slate-400">Actual Mins:</span>
                  <input
                    type="number"
                    min="0"
                    value={actuals[task.id] !== undefined ? actuals[task.id] : task.actual_minutes}
                    onChange={(e) => setActuals({ ...actuals, [task.id]: parseInt(e.target.value) || 0 })}
                    className="w-14 bg-slate-950 border border-slate-700 text-center text-white rounded px-1 py-0.5 focus:outline-none focus:border-sky-500"
                  />
                  <span className="text-slate-500">/ {task.planned_minutes}</span>
                </div>

                {/* Status Toggle Buttons */}
                <div className="flex items-center space-x-1">
                  <button
                    onClick={() => handleStatusChange(task.id, 'COMPLETED', task.planned_minutes)}
                    className={`px-3 py-1.5 rounded text-xs font-bold font-mono transition ${
                      task.status === 'COMPLETED'
                        ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/40'
                        : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                    }`}
                  >
                    Done
                  </button>
                  <button
                    onClick={() => handleStatusChange(task.id, 'PARTIALLY_COMPLETED', task.planned_minutes)}
                    className={`px-3 py-1.5 rounded text-xs font-bold font-mono transition ${
                      task.status === 'PARTIALLY_COMPLETED'
                        ? 'bg-amber-600 text-white shadow-lg shadow-amber-900/40'
                        : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                    }`}
                  >
                    Partial
                  </button>
                  <button
                    onClick={() => handleStatusChange(task.id, 'MISSED', task.planned_minutes)}
                    className={`px-3 py-1.5 rounded text-xs font-bold font-mono transition ${
                      task.status === 'MISSED'
                        ? 'bg-rose-600 text-white shadow-lg shadow-rose-900/40'
                        : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                    }`}
                  >
                    Missed
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* End of Day Scorecard Form (10:00–10:15 PM) */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider font-mono flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-purple-400" />
            <span>DAILY SCORECARD & NIGHTLY REFLECTION (10:00–10:15 PM)</span>
          </h2>
          {logSubmitted && (
            <span className="text-xs bg-emerald-500/20 text-emerald-300 font-mono px-2.5 py-1 rounded border border-emerald-500/30 flex items-center space-x-1">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Scorecard Logged</span>
            </span>
          )}
        </div>

        <form onSubmit={handleScorecardSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-slate-950 border border-slate-800 rounded-lg">
              <span className="text-xs font-medium text-slate-200 flex items-center space-x-2">
                <Dumbbell className="w-4 h-4 text-sky-400" />
                <span>Morning Workout Completed (6:00–7:00 AM)</span>
              </span>
              <input
                type="checkbox"
                checked={workout}
                onChange={(e) => setWorkout(e.target.checked)}
                className="w-4 h-4 accent-sky-500 rounded cursor-pointer"
              />
            </div>

            <div>
              <label className="text-xs font-mono text-slate-400 block mb-1">Sleep Hours Last Night</label>
              <input
                type="number"
                step="0.5"
                value={sleepHours}
                onChange={(e) => setSleepHours(parseFloat(e.target.value) || 0)}
                className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
              />
            </div>

            <div>
              <label className="text-xs font-mono text-slate-400 block mb-1">Total Focus Study Hours</label>
              <input
                type="number"
                step="0.5"
                value={focusHours}
                onChange={(e) => setFocusHours(parseFloat(e.target.value) || 0)}
                className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
              />
            </div>
          </div>

          <div className="space-y-3">
            <div>
              <label className="text-xs font-mono text-slate-400 block mb-1">Blockers / Friction Points Today</label>
              <textarea
                rows={2}
                value={blockers}
                onChange={(e) => setBlockers(e.target.value)}
                placeholder="e.g. Spent extra 30 min debugging PyTorch tensor shape mismatch"
                className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-xs text-white focus:outline-none focus:border-sky-500"
              />
            </div>

            <div>
              <label className="text-xs font-mono text-slate-400 block mb-1">Tomorrow's #1 Critical Priority</label>
              <input
                type="text"
                value={tomorrowPriority}
                onChange={(e) => setTomorrowPriority(e.target.value)}
                placeholder="e.g. Finish FastAPI endpoint unit tests"
                className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-xs text-white focus:outline-none focus:border-sky-500"
              />
            </div>

            <button
              type="submit"
              className="w-full py-2.5 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-bold font-mono transition flex items-center justify-center space-x-2 shadow-lg shadow-sky-900/40"
            >
              <Save className="w-4 h-4" />
              <span>Save Scorecard & End Day</span>
            </button>
          </div>
        </form>
      </div>

    </div>
  );
};
