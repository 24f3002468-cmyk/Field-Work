import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { VerificationReport } from '../types';
import { ShieldCheck, RefreshCw, Download, Database, CheckCircle2 } from 'lucide-react';

export const VerificationPage: React.FC = () => {
  const [report, setReport] = useState<VerificationReport | null>(null);
  const [backupMsg, setBackupMsg] = useState<string | null>(null);
  const [recalcMsg, setRecalcMsg] = useState<string | null>(null);

  const loadIntegrity = async () => {
    const res = await api.get('/verification/data-integrity');
    setReport(res.data);
  };

  useEffect(() => {
    loadIntegrity();
  }, []);

  const handleRecalculate = async () => {
    const res = await api.post('/verification/recalculate');
    setRecalcMsg(res.data.message);
    loadIntegrity();
  };

  const handleBackup = async () => {
    const res = await api.get('/verification/backup-status');
    setBackupMsg(`Backup file created: ${res.data.filename}`);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center space-x-2">
            <ShieldCheck className="w-6 h-6 text-emerald-400" />
            <span>System Health & Data Integrity Verification</span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">Automated validation of 200 planner days, milestone dates, metrics consistency, and backup restoration.</p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={handleRecalculate}
            className="px-3.5 py-2 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-mono font-bold transition flex items-center space-x-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Recalculate Metrics</span>
          </button>
          <button
            onClick={handleBackup}
            className="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-mono font-bold transition flex items-center space-x-1.5"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Trigger Backup</span>
          </button>
        </div>
      </div>

      {recalcMsg && (
        <div className="bg-sky-950/60 border border-sky-500/40 text-sky-200 text-xs p-3 rounded-lg font-mono">
          ✓ {recalcMsg}
        </div>
      )}

      {backupMsg && (
        <div className="bg-emerald-950/60 border border-emerald-500/40 text-emerald-200 text-xs p-3 rounded-lg font-mono">
          ✓ {backupMsg}
        </div>
      )}

      {/* Verification Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl text-center">
          <span className="text-xs text-slate-400 font-mono block">INTEGRITY STATUS</span>
          <span className={`text-2xl font-black font-mono mt-1 block ${report?.status === 'PASS' ? 'text-emerald-400' : 'text-rose-400'}`}>
            {report?.status || 'CHECKING'}
          </span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl text-center">
          <span className="text-xs text-slate-400 font-mono block">PLANNER DAYS VERIFIED</span>
          <span className="text-2xl font-black text-white font-mono mt-1 block">{report?.days_count || 0} / 200</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl text-center">
          <span className="text-xs text-slate-400 font-mono block">TOTAL PLANNER TASKS</span>
          <span className="text-2xl font-black text-white font-mono mt-1 block">{report?.tasks_count || 0}</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl text-center">
          <span className="text-xs text-slate-400 font-mono block">MILESTONES VERIFIED</span>
          <span className="text-2xl font-black text-white font-mono mt-1 block">{report?.milestones_count || 0}</span>
        </div>
      </div>

      {/* Detailed Issues Report */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <h2 className="text-sm font-bold text-white font-mono border-b border-slate-800 pb-3">
          AUTOMATED AUDIT LOG & REPORT
        </h2>

        {report?.issues && report.issues.length > 0 ? (
          <div className="space-y-2">
            {report.issues.map((iss, i) => (
              <div key={i} className="p-3 bg-rose-950/40 border border-rose-500/40 text-rose-200 text-xs font-mono rounded-lg">
                ⚠ {iss}
              </div>
            ))}
          </div>
        ) : (
          <div className="p-4 bg-emerald-950/30 border border-emerald-500/30 rounded-lg text-emerald-300 text-xs font-mono flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>All 200 planner execution days, schedule block rules, milestones, and foreign keys verified clean. No data integrity anomalies found.</span>
          </div>
        )}
      </div>

    </div>
  );
};
