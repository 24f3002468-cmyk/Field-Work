import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useDashboardStore } from '../store/useDashboardStore';
import { LayoutDashboard, Calendar, Clock, CheckSquare, Code, Database, BookOpen, Briefcase, ShieldCheck, Wifi, WifiOff } from 'lucide-react';

export const Navbar: React.FC = () => {
  const location = useLocation();
  const { saveStatus, isOffline } = useDashboardStore();

  const links = [
    { path: '/', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/today', label: 'Today', icon: Clock },
    { path: '/planner', label: 'Planner', icon: Calendar },
    { path: '/dsa', label: 'DSA', icon: Code },
    { path: '/project', label: 'Project 1', icon: CheckSquare },
    { path: '/sql', label: 'SQL (Part 1)', icon: Database },
    { path: '/iitm', label: 'IITM & Points', icon: BookOpen },
    { path: '/applications', label: 'Applications', icon: Briefcase },
    { path: '/verification', label: 'Verification', icon: ShieldCheck },
  ];

  return (
    <nav className="bg-slate-900 text-white border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-sky-500 flex items-center justify-center font-bold text-white shadow-lg">
              200
            </div>
            <div>
              <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-sky-400 to-emerald-400 bg-clip-text text-transparent">
                ML Systems OS
              </span>
              <span className="text-xs text-slate-400 block font-mono">Sep 10, 2026 → Apr 30, 2027</span>
            </div>
          </div>

          <div className="hidden md:flex space-x-1">
            {links.map((link) => {
              const Icon = link.icon;
              const active = location.pathname === link.path;
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`flex items-center space-x-1.5 px-3 py-2 rounded-md text-xs font-medium transition-colors ${
                    active
                      ? 'bg-sky-500/20 text-sky-400 border border-sky-500/30'
                      : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{link.label}</span>
                </Link>
              );
            })}
          </div>

          <div className="flex items-center space-x-3 text-xs">
            <span
              className={`px-2.5 py-1 rounded-full font-mono font-medium flex items-center space-x-1 ${
                isOffline ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
              }`}
            >
              {isOffline ? <WifiOff className="w-3.5 h-3.5" /> : <Wifi className="w-3.5 h-3.5" />}
              <span>{saveStatus}</span>
            </span>
          </div>
        </div>
      </div>

      {/* Mobile nav bar */}
      <div className="md:hidden flex overflow-x-auto px-2 py-2 border-t border-slate-800 bg-slate-950 space-x-1">
        {links.map((link) => {
          const Icon = link.icon;
          const active = location.pathname === link.path;
          return (
            <Link
              key={link.path}
              to={link.path}
              className={`flex items-center whitespace-nowrap space-x-1 px-2.5 py-1.5 rounded-md text-xs font-medium ${
                active ? 'bg-sky-500 text-white' : 'text-slate-400 hover:bg-slate-800'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{link.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
};
