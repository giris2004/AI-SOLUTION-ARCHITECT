import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { 
  ArrowRight, ArrowLeft, Cpu, ShieldAlert, Sparkles, Network,
  Layers, Settings, Users, Calendar, AlertCircle
} from 'lucide-react';

const ProjectForm = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [loadingMessage, setLoadingMessage] = useState('');

  // Form Fields State
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    domain: '',
    target_platform: 'Web App',
    expected_users: 1000,
    expected_traffic: 'Medium',
    budget: 'Medium Range',
    deadline: '3 Months',
    team_size: 4,
    preferred_cloud: 'AWS',
    required_features: '',
    security_level: 'Standard',
    scalability: 'Medium',
    availability: '99.9%',
    third_party_integrations: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleNext = (e) => {
    e.preventDefault();
    if (step === 1 && (!formData.name || !formData.domain || !formData.description)) {
      setError("Please fill out all required fields.");
      return;
    }
    setError('');
    setStep(prev => prev + 1);
  };

  const handlePrev = () => {
    setError('');
    setStep(prev => prev - 1);
  };

  const runLoadingMessages = () => {
    const messages = [
      "Connecting to Google Gemini API...",
      "Analyzing software requirement constraints...",
      "Generating optimal architecture patterns...",
      "Selecting components frontend/backend stack...",
      "Calculating estimated cloud hosting cost matrix...",
      "Compiling agile sprints, milestones and backlogs...",
      "Identifying technical and security risks...",
      "Formatting final response JSON..."
    ];
    let i = 0;
    setLoadingMessage(messages[0]);
    const interval = setInterval(() => {
      i++;
      if (i < messages.length) {
        setLoadingMessage(messages[i]);
      } else {
        clearInterval(interval);
      }
    }, 1800);
    return interval;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.required_features) {
      setError("Please outline your core required features.");
      return;
    }
    
    setError('');
    setLoading(true);
    const msgInterval = runLoadingMessages();

    try {
      await api.post('/api/project/analyze', formData);
      clearInterval(msgInterval);
      navigate('/dashboard');
    } catch (err) {
      clearInterval(msgInterval);
      setError(err.response?.data?.detail || "Failed to analyze requirements. Please verify input data.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-6 py-10 relative">
      {/* Background decoration */}
      <div className="absolute top-1/4 left-1/2 w-80 h-80 rounded-full bg-blue-600/5 blur-[128px] -translate-x-1/2 pointer-events-none"></div>

      {loading ? (
        <div className="py-24 text-center space-y-6 glass-card rounded-2xl p-12 border border-slate-900 shadow-xl relative z-10">
          <div className="w-16 h-16 bg-blue-600/10 border border-blue-500/20 rounded-full flex items-center justify-center mx-auto shadow-lg relative">
            <Cpu className="text-blue-400 animate-pulse" size={32} />
            <div className="absolute inset-0 rounded-full border-2 border-blue-500/20 border-t-blue-500 animate-spin"></div>
          </div>
          <h3 className="text-xl font-bold text-white tracking-wide">Analyzing Project Architecture</h3>
          <p className="text-slate-400 text-sm max-w-sm mx-auto">{loadingMessage}</p>
        </div>
      ) : (
        <div className="glass-card p-8 rounded-2xl border border-slate-900 shadow-2xl relative z-10 text-left">
          {/* Header Title */}
          <div className="mb-8 border-b border-slate-850 pb-6">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="text-blue-500" size={18} />
              <span className="text-xs font-bold text-blue-500 uppercase tracking-widest">AI Engine Ingest</span>
            </div>
            <h2 className="text-2xl font-bold text-white">Project Requirement Intake Form</h2>
            <p className="text-sm text-slate-400 mt-1">Provide project details to receive tailored, validated architectural recommendations.</p>
            
            {/* Step indicators */}
            <div className="flex items-center gap-2 mt-6">
              {[1, 2, 3].map((s) => (
                <div 
                  key={s} 
                  className={`h-1.5 rounded-full flex-1 transition-all duration-300 ${
                    s <= step ? 'bg-blue-600' : 'bg-slate-800'
                  }`}
                ></div>
              ))}
            </div>
          </div>

          {error && (
            <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 flex items-start gap-3 text-sm">
              <AlertCircle className="shrink-0 mt-0.5" size={16} />
              <p>{error}</p>
            </div>
          )}

          <form onSubmit={step === 3 ? handleSubmit : handleNext}>
            {step === 1 && (
              <div className="space-y-6">
                <div>
                  <label className="block text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                    Project Name *
                  </label>
                  <input
                    type="text"
                    name="name"
                    required
                    placeholder="e.g. Enterprise E-Commerce Platform"
                    value={formData.name}
                    onChange={handleChange}
                    className="w-full bg-slate-950/60 border border-slate-850 focus:border-blue-600 rounded-lg px-4 py-2.5 outline-none text-white text-sm transition-all"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                    Industry / Business Domain *
                  </label>
                  <input
                    type="text"
                    name="domain"
                    required
                    placeholder="e.g. FinTech, Healthcare, Logistics, IoT"
                    value={formData.domain}
                    onChange={handleChange}
                    className="w-full bg-slate-950/60 border border-slate-850 focus:border-blue-600 rounded-lg px-4 py-2.5 outline-none text-white text-sm transition-all"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                    Target Deployment Platform *
                  </label>
                  <select
                    name="target_platform"
                    value={formData.target_platform}
                    onChange={handleChange}
                    className="w-full bg-slate-950/60 border border-slate-850 focus:border-blue-600 rounded-lg px-4 py-2.5 outline-none text-white text-sm transition-all appearance-none"
                  >
                    <option value="Web App">Web Application (React, SPA)</option>
                    <option value="Mobile App">Mobile Application (iOS/Android)</option>
                    <option value="Desktop Application">Desktop Application</option>
                    <option value="Cross-Platform Web/Mobile">Cross-Platform (Web, Mobile, API)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                    Project Description Summary *
                  </label>
                  <textarea
                    name="description"
                    required
                    rows={4}
                    placeholder="Outline your application goals, target audience, and primary workflow processes..."
                    value={formData.description}
                    onChange={handleChange}
                    className="w-full bg-slate-950/60 border border-slate-850 focus:border-blue-600 rounded-lg p-4 outline-none text-white text-sm transition-all resize-none"
                  />
                </div>
              </div>
            )}

            {step === 2 && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                      Expected Monthly Active Users
                    </label>
                    <input
                      type="number"
                      name="expected_users"
                      value={formData.expected_users}
                      onChange={handleChange}
                      className="w-full bg-slate-950/60 border border-slate-850 focus:border-blue-600 rounded-lg px-4 py-2.5 outline-none text-white text-sm transition-all"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                      Expected Traffic Volume
                    </label>
                    <select
                      name="expected_traffic"
                      value={formData.expected_traffic}
                      onChange={handleChange}
                      className="w-full bg-slate-950/60 border border-slate-850 focus:border-blue-600 rounded-lg px-4 py-2.5 outline-none text-white text-sm transition-all"
                    >
                      <option value="Low">Low (1-10 req/sec)</option>
                      <option value="Medium">Medium (10-100 req/sec)</option>
                      <option value="High">High (100-1000 req/sec)</option>
                      <option value="Very High">Very High (1000+ req/sec)</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                      Project Budget Constraint
                    </label>
                    <input
                      type="text"
                      name="budget"
                      placeholder="e.g. 50,000 USD, Bootstrapped, VC funded"
                      value={formData.budget}
                      onChange={handleChange}
                      className="w-full bg-slate-950/60 border border-slate-850 focus:border-blue-600 rounded-lg px-4 py-2.5 outline-none text-white text-sm transition-all"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                      Development Target Deadline
                    </label>
                    <input
                      type="text"
                      name="deadline"
                      placeholder="e.g. 3 Months, 6 Months, Flexible"
                      value={formData.deadline}
                      onChange={handleChange}
                      className="w-full bg-slate-950/60 border border-slate-850 focus:border-blue-600 rounded-lg px-4 py-2.5 outline-none text-white text-sm transition-all"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                      Available Development Team Size
                    </label>
                    <input
                      type="number"
                      name="team_size"
                      value={formData.team_size}
                      onChange={handleChange}
                      className="w-full bg-slate-950/60 border border-slate-850 focus:border-blue-600 rounded-lg px-4 py-2.5 outline-none text-white text-sm transition-all"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                      Preferred Cloud Platform
                    </label>
                    <select
                      name="preferred_cloud"
                      value={formData.preferred_cloud}
                      onChange={handleChange}
                      className="w-full bg-slate-950/60 border border-slate-850 focus:border-blue-600 rounded-lg px-4 py-2.5 outline-none text-white text-sm transition-all"
                    >
                      <option value="AWS">Amazon Web Services (AWS)</option>
                      <option value="GCP">Google Cloud Platform (GCP)</option>
                      <option value="Azure">Microsoft Azure</option>
                      <option value="Any">No Preference (AI decides)</option>
                    </select>
                  </div>
                </div>
              </div>
            )}

            {step === 3 && (
              <div className="space-y-6">
                <div>
                  <label className="block text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                    Core Required Features & Integrations *
                  </label>
                  <textarea
                    name="required_features"
                    required
                    rows={3}
                    placeholder="List required modules (e.g. JWT Auth, Payment gateway, Real-time messaging notifications, search index)..."
                    value={formData.required_features}
                    onChange={handleChange}
                    className="w-full bg-slate-950/60 border border-slate-850 focus:border-blue-600 rounded-lg p-4 outline-none text-white text-sm transition-all resize-none"
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                  <div>
                    <label className="block text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                      Target Security Level
                    </label>
                    <select
                      name="security_level"
                      value={formData.security_level}
                      onChange={handleChange}
                      className="w-full bg-slate-950/60 border border-slate-850 focus:border-blue-600 rounded-lg px-3 py-2 outline-none text-white text-sm transition-all"
                    >
                      <option value="Standard">Standard (TLS, HTTPS)</option>
                      <option value="High">High (OAuth2, Encrypted Database)</option>
                      <option value="Enterprise (Audited)">Enterprise (Compliance Audits, HIPAA/PCI)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                      Scalability Target
                    </label>
                    <select
                      name="scalability"
                      value={formData.scalability}
                      onChange={handleChange}
                      className="w-full bg-slate-950/60 border border-slate-850 focus:border-blue-600 rounded-lg px-3 py-2 outline-none text-white text-sm transition-all"
                    >
                      <option value="Low">Low (Simple monolithic scaling)</option>
                      <option value="Medium">Medium (Autoscaling Web Nodes)</option>
                      <option value="High">High (Horizontal Multi-AZ Database)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                      Availability Target SLA
                    </label>
                    <select
                      name="availability"
                      value={formData.availability}
                      onChange={handleChange}
                      className="w-full bg-slate-950/60 border border-slate-850 focus:border-blue-600 rounded-lg px-3 py-2 outline-none text-white text-sm transition-all"
                    >
                      <option value="99.0%">99.0% (Simple failover)</option>
                      <option value="99.9%">99.9% (Multi-AZ Nodes)</option>
                      <option value="99.99%">99.99% (Global replication)</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                    Third-Party APIs or Integrations (Optional)
                  </label>
                  <input
                    type="text"
                    name="third_party_integrations"
                    placeholder="e.g. Twilio SMS, Stripe Payments, SendGrid email"
                    value={formData.third_party_integrations}
                    onChange={handleChange}
                    className="w-full bg-slate-950/60 border border-slate-850 focus:border-blue-600 rounded-lg px-4 py-2.5 outline-none text-white text-sm transition-all"
                  />
                </div>
              </div>
            )}

            {/* Form Nav Buttons */}
            <div className="flex items-center justify-between border-t border-slate-850 pt-6 mt-8">
              {step > 1 ? (
                <button
                  type="button"
                  onClick={handlePrev}
                  className="glass-btn hover:text-white"
                >
                  <ArrowLeft size={16} />
                  Back Step
                </button>
              ) : (
                <div></div>
              )}

              {step < 3 ? (
                <button
                  type="submit"
                  className="glass-btn-primary"
                >
                  Next Step
                  <ArrowRight size={16} />
                </button>
              ) : (
                <button
                  type="submit"
                  className="glass-btn-primary bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-500 hover:to-emerald-500 text-white shadow-lg"
                >
                  Analyze & Generate
                  <Sparkles size={16} />
                </button>
              )}
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default ProjectForm;
