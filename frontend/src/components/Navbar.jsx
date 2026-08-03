import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LayoutDashboard, FileSpreadsheet, LogOut, ShieldAlert } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  if (!user) return null;

  return (
    <nav className="glass-panel sticky top-0 z-50 px-6 py-4 flex items-center justify-between border-b border-slate-800">
      <div className="flex items-center gap-8">
        <Link to="/" className="flex items-center gap-3 text-xl font-bold tracking-tight text-white hover:opacity-90">
          <span className="text-2xl">🏛️</span>
          <span className="bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
            AI Solution Architect
          </span>
        </Link>

        <div className="hidden md:flex items-center gap-2">
          <Link
            to="/dashboard"
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all duration-150 ${
              isActive('/dashboard') || isActive('/')
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/30'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
            }`}
          >
            <LayoutDashboard size={18} />
            Dashboard
          </Link>

          <Link
            to="/project-form"
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all duration-150 ${
              isActive('/project-form')
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/30'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
            }`}
          >
            <FileSpreadsheet size={18} />
            New Requirement
          </Link>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-3 bg-slate-900/60 border border-slate-800 rounded-full pl-3 pr-4 py-1.5">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white text-sm font-bold shadow-md uppercase">
            {user.full_name.charAt(0)}
          </div>
          <div className="flex flex-col text-left">
            <span className="text-sm font-semibold text-white leading-none">{user.full_name}</span>
            <span className="text-xs text-blue-400 leading-none mt-1 capitalize">{user.role}</span>
          </div>
        </div>

        <button
          onClick={logout}
          className="p-2 rounded-lg border border-slate-800 hover:border-red-500/30 text-slate-400 hover:text-red-400 hover:bg-red-500/10 transition-all duration-150"
          title="Sign Out"
        >
          <LogOut size={20} />
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
