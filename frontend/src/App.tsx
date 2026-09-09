import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Dashboard } from './pages/Dashboard';
import { TodayPage } from './pages/TodayPage';
import { PlannerPage } from './pages/PlannerPage';
import { DSAPage } from './pages/DSAPage';
import { ProjectPage } from './pages/ProjectPage';
import { SQLPage } from './pages/SQLPage';
import { IITMPage } from './pages/IITMPage';
import { ApplicationsPage } from './pages/ApplicationsPage';
import { VerificationPage } from './pages/VerificationPage';

export function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-950 font-sans antialiased text-slate-100 selection:bg-sky-500 selection:text-white">
        <Navbar />
        <main className="pb-12">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/today" element={<TodayPage />} />
            <Route path="/planner" element={<PlannerPage />} />
            <Route path="/dsa" element={<DSAPage />} />
            <Route path="/project" element={<ProjectPage />} />
            <Route path="/sql" element={<SQLPage />} />
            <Route path="/iitm" element={<IITMPage />} />
            <Route path="/applications" element={<ApplicationsPage />} />
            <Route path="/verification" element={<VerificationPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
