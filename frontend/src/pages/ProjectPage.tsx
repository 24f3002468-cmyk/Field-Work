import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { ProjectStageResponse, ProjectChecklistResponse, ProjectStatus } from '../types';
import { CheckSquare, AlertCircle, Clock, ExternalLink, ShieldCheck } from 'lucide-react';

export const ProjectPage: React.FC = () => {
  const [stages, setStages] = useState<ProjectStageResponse[]>([]);
  const [checklist, setChecklist] = useState<ProjectChecklistResponse[]>([]);
  const [status, setStatus] = useState<ProjectStatus | null>(null);

  const loadProject = async () => {
    const sRes = await api.get('/project');
    const cRes = await api.get('/project/checklist');
    const stRes = await api.get('/project/status');
    setStages(sRes.data);
    setChecklist(cRes.data);
    setStatus(stRes.data);
  };

  useEffect(() => {
    loadProject();
  }, []);

  const toggleChecklist = async (id: number, currentVerified: boolean) => {
    await api.put(`/project/checklist/${id}`, null, { params: { verified: !currentVerified } });
    loadProject();
  };

  const setStageStatus = async (stageNum: number, newStatus: string) => {
    await api.put(`/project/stage/${stageNum}`, null, { params: { status: newStatus } });
    loadProject();
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-sky-950 to-slate-900 border border-sky-500/30 rounded-xl p-6 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center space-x-2 text-xs font-mono text-sky-400">
            <span className="bg-sky-500/20 px-2 py-0.5 rounded font-bold">PROJECT 1 CRITICAL PATH</span>
            <span>•</span>
            <span>CRITICAL DEADLINE: DEC 22, 2026</span>
          </div>
          <h1 className="text-2xl font-black text-white mt-1">Resume Intelligence Platform / Ranking ML System</h1>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Complete end-to-end ML pipeline with TF-IDF baseline, scikit-learn/XGBoost ranking models, NER, SHAP explainability, FastAPI deployment, and Streamlit demo.
          </p>
        </div>

        <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl font-mono text-right shrink-0">
          <span className="text-xs text-slate-400 block uppercase">SHIPPING STATUS</span>
          <span className={`text-xl font-black block mt-0.5 ${status?.ship_status === 'SHIPPED' ? 'text-emerald-400' : 'text-amber-400'}`}>
            {status?.ship_status || 'NOT SHIPPED'}
          </span>
          <span className="text-[11px] text-slate-500 block mt-1">
            Checklist: {status?.checklist_verified || 0} / {status?.total_checklist || 11} Verified
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* 15 Project Stages */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-sm font-bold text-white font-mono flex items-center space-x-2 border-b border-slate-800 pb-3">
            <Clock className="w-4 h-4 text-sky-400" />
            <span>15 PROJECT DEVELOPMENT STAGES</span>
          </h2>

          <div className="space-y-2.5 max-h-[550px] overflow-y-auto pr-1">
            {stages.map((st) => (
              <div
                key={st.id}
                className="p-3 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between gap-3 text-xs"
              >
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-sky-400 font-bold">Stage {st.stage_number}</span>
                    <span className="font-bold text-white">{st.name}</span>
                  </div>
                  <p className="text-[11px] text-slate-400 mt-0.5">{st.description}</p>
                </div>

                <select
                  value={st.status}
                  onChange={(e) => setStageStatus(st.stage_number, e.target.value)}
                  className="bg-slate-900 border border-slate-700 text-xs font-mono text-slate-200 rounded px-2.5 py-1 focus:outline-none focus:border-sky-500"
                >
                  <option value="NOT_STARTED">Not Started</option>
                  <option value="IN_PROGRESS">In Progress</option>
                  <option value="COMPLETED">Completed</option>
                </select>
              </div>
            ))}
          </div>
        </div>

        {/* Project Ship Verification Checklist */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-sm font-bold text-white font-mono flex items-center space-x-2 border-b border-slate-800 pb-3">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>PROJECT SHIP VERIFICATION CHECKLIST</span>
          </h2>

          <p className="text-xs text-slate-400">
            Project cannot automatically become <code className="text-emerald-400">SHIPPED</code> until all verification criteria pass.
          </p>

          <div className="space-y-2.5 max-h-[500px] overflow-y-auto pr-1">
            {checklist.map((item) => (
              <div
                key={item.id}
                onClick={() => toggleChecklist(item.id, item.verified)}
                className={`p-3 rounded-lg border cursor-pointer flex items-center space-x-3 transition ${
                  item.verified
                    ? 'bg-emerald-950/20 border-emerald-500/40 text-emerald-200'
                    : 'bg-slate-950 border-slate-800 text-slate-300 hover:border-slate-700'
                }`}
              >
                <div className={`w-4 h-4 rounded flex items-center justify-center border ${item.verified ? 'bg-emerald-500 border-emerald-400 text-white' : 'border-slate-600'}`}>
                  {item.verified && <CheckSquare className="w-3 h-3" />}
                </div>
                <span className="text-xs font-medium">{item.title}</span>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};
