import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Lock, Mail, User, ShieldCheck, AlertCircle } from 'lucide-react';

const Login = () => {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [role, setRole] = useState('architect');
  
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isRegister) {
        await register(email, fullName, password, role);
        // Automatically login user after registration
        await login(email, password);
      } else {
        await login(email, password);
      }
      navigate('/dashboard');
    } catch (err) {
      setError(typeof err === 'string' ? err : 'An unexpected auth error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 relative overflow-hidden bg-slate-950">
      {/* Background Cyber Glowing Decors */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full bg-blue-600/10 blur-[128px] cyber-glow"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full bg-indigo-600/10 blur-[128px] cyber-glow"></div>

      <div className="w-full max-w-md glass-card p-8 rounded-2xl border border-slate-800 shadow-2xl relative z-10">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-blue-600/10 border border-blue-500/20 flex items-center justify-center mx-auto mb-4 text-3xl shadow-lg shadow-blue-500/5">
            🏛️
          </div>
          <h2 className="text-2xl font-bold tracking-tight text-white">
            {isRegister ? 'Create Architect Account' : 'Architect Console'}
          </h2>
          <p className="text-sm text-slate-400 mt-2">
            {isRegister ? 'Sign up to build and Persist AI system architectures' : 'Sign in to access recommendation engines'}
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 flex items-start gap-3 text-sm">
            <AlertCircle className="shrink-0 mt-0.5" size={16} />
            <p>{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {isRegister && (
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
                Full Name
              </label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-500">
                  <User size={18} />
                </span>
                <input
                  type="text"
                  required
                  placeholder="Enter full name"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full bg-slate-900/60 border border-slate-850 focus:border-blue-500 rounded-lg pl-10 pr-4 py-2.5 outline-none text-white text-sm transition-all"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
              Email Address
            </label>
            <div className="relative">
              <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-500">
                <Mail size={18} />
              </span>
              <input
                type="email"
                required
                placeholder="architect@enterprise.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-slate-900/60 border border-slate-850 focus:border-blue-500 rounded-lg pl-10 pr-4 py-2.5 outline-none text-white text-sm transition-all"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
              Console Password
            </label>
            <div className="relative">
              <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-500">
                <Lock size={18} />
              </span>
              <input
                type="password"
                required
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-slate-900/60 border border-slate-850 focus:border-blue-500 rounded-lg pl-10 pr-4 py-2.5 outline-none text-white text-sm transition-all"
              />
            </div>
          </div>

          {isRegister && (
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
                System Access Role
              </label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-500">
                  <ShieldCheck size={18} />
                </span>
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  className="w-full bg-slate-900/60 border border-slate-850 focus:border-blue-500 rounded-lg pl-10 pr-4 py-2.5 outline-none text-white text-sm transition-all appearance-none"
                >
                  <option value="architect">Solution Architect</option>
                  <option value="lead">Chief Architect / Lead</option>
                  <option value="admin">Administrator</option>
                </select>
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full glass-btn-primary py-3 font-semibold mt-4 shadow-lg flex items-center justify-center gap-2"
          >
            {loading ? 'Processing Session...' : isRegister ? 'Register Account' : 'Authenticate Session'}
          </button>
        </form>

        <div className="mt-8 text-center text-sm text-slate-400 border-t border-slate-900 pt-6">
          <p>
            {isRegister ? 'Already registered?' : 'Need a local credentials account?'}
            <button
              onClick={() => {
                setIsRegister(!isRegister);
                setError('');
              }}
              className="text-blue-400 hover:text-blue-300 font-semibold ml-1.5 focus:outline-none"
            >
              {isRegister ? 'Sign In Instead' : 'Create Account'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
