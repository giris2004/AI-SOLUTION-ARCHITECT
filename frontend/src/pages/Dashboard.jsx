import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { 
  Plus, Search, FileDown, Trash2, Calendar, HardDrive, 
  Layers, Cloud, ShieldCheck, DollarSign, ListTodo, AlertTriangle, Eye, X 
} from 'lucide-react';

const Dashboard = () => {
  const [history, setHistory] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Modal State for viewing a specific recommendation
  const [selectedProject, setSelectedProject] = useState(null);
  const [selectedRec, setSelectedRec] = useState(null);
  const [activeTab, setActiveTab] = useState('specs');
  const [modalLoading, setModalLoading] = useState(false);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/project/history');
      setHistory(response.data);
    } catch (err) {
      setError("Failed to fetch recommendation history catalog.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async (projectId, projectName) => {
    try {
      const response = await api.get(`/api/project/${projectId}/pdf`, {
        responseType: 'blob'
      });
      const file = new Blob([response.data], { type: 'application/pdf' });
      const fileURL = URL.createObjectURL(file);
      const link = document.createElement('a');
      link.href = fileURL;
      link.setAttribute('download', `architecture_report_${projectName.toLowerCase().replace(/\s+/g, '_')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      alert("Failed to export PDF briefing document.");
      console.error(err);
    }
  };

  const handleDeleteProject = async (projectId) => {
    if (!window.confirm("Are you sure you want to permanently delete this project analysis and recommendation report?")) return;
    try {
      await api.delete(`/api/project/${projectId}`);
      setHistory(history.filter(p => p.project_id !== projectId));
      if (selectedProject?.id === projectId) {
        setSelectedProject(null);
        setSelectedRec(null);
      }
    } catch (err) {
      alert("Failed to delete project record.");
      console.error(err);
    }
  };

  const handleViewRecommendation = async (projectId) => {
    try {
      setModalLoading(true);
      const response = await api.get(`/api/project/${projectId}`);
      setSelectedProject(response.data.project);
      setSelectedRec(response.data.recommendation);
      setActiveTab('specs');
    } catch (err) {
      alert("Failed to load recommendation details.");
      console.error(err);
    } finally {
      setModalLoading(false);
    }
  };

  // Filter history
  const filteredHistory = history.filter(p => 
    p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    p.domain.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto px-6 py-10">
      {/* Top Banner section */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">Architect Control Center</h1>
          <p className="text-slate-400 mt-1">Review, export, and trigger new automated architecture specifications.</p>
        </div>
        <Link to="/project-form" className="glass-btn-primary self-start">
          <Plus size={18} />
          Create Specification
        </Link>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        <div className="glass-card p-6 rounded-xl border border-slate-900">
          <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Total Projects Analyzed</span>
          <p className="text-3xl font-bold text-white mt-2">{history.length}</p>
        </div>
        <div className="glass-card p-6 rounded-xl border border-slate-900">
          <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Unique Domains</span>
          <p className="text-3xl font-bold text-blue-400 mt-2">
            {new Set(history.map(h => h.domain)).size}
          </p>
        </div>
        <div className="glass-card p-6 rounded-xl border border-slate-900">
          <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Default Cloud Framework</span>
          <p className="text-3xl font-bold text-indigo-400 mt-2">AWS / Multi</p>
        </div>
        <div className="glass-card p-6 rounded-xl border border-slate-900">
          <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">System Status</span>
          <p className="text-3xl font-bold text-green-400 mt-2">Active</p>
        </div>
      </div>

      {/* History log segment */}
      <div className="glass-card rounded-xl border border-slate-900 p-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <h3 className="text-lg font-bold text-white">Archived Recommendations</h3>
          <div className="relative w-full sm:max-w-xs">
            <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-500">
              <Search size={18} />
            </span>
            <input
              type="text"
              placeholder="Search by name or domain..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-950/60 border border-slate-800 rounded-lg pl-10 pr-4 py-2 outline-none text-white text-sm focus:border-blue-600 transition-all"
            />
          </div>
        </div>

        {loading ? (
          <div className="py-20 text-center text-slate-500">
            <div className="w-8 h-8 rounded-full border-2 border-blue-500 border-t-transparent animate-spin mx-auto mb-4"></div>
            <p>Loading historical catalog...</p>
          </div>
        ) : error ? (
          <p className="text-red-400 py-10 text-center">{error}</p>
        ) : filteredHistory.length === 0 ? (
          <div className="py-20 text-center text-slate-500 border-2 border-dashed border-slate-900 rounded-xl">
            <Layers size={36} className="mx-auto mb-3 opacity-30 text-blue-500" />
            <p className="text-base font-medium">No architecture reports found.</p>
            <p className="text-sm text-slate-500 mt-1">Submit your project requirements to initiate recommendations.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-850 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  <th className="py-3 px-4">Project Name</th>
                  <th className="py-3 px-4">Domain</th>
                  <th className="py-3 px-4">Target Platform</th>
                  <th className="py-3 px-4">Arch. Pattern</th>
                  <th className="py-3 px-4">Generated Date</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-850">
                {filteredHistory.map((item) => (
                  <tr key={item.project_id} className="hover:bg-slate-900/40 transition-all group">
                    <td className="py-4 px-4 font-semibold text-white">{item.name}</td>
                    <td className="py-4 px-4 text-slate-300">{item.domain}</td>
                    <td className="py-4 px-4 text-slate-400">{item.platform}</td>
                    <td className="py-4 px-4">
                      <span className="bg-blue-900/30 text-blue-400 border border-blue-500/10 px-2 py-0.5 rounded text-xs font-medium">
                        {item.architecture_pattern || 'Analyzing...'}
                      </span>
                    </td>
                    <td className="py-4 px-4 text-slate-400 text-xs">
                      {new Date(item.created_at).toLocaleDateString()}
                    </td>
                    <td className="py-4 px-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleViewRecommendation(item.project_id)}
                          className="p-1.5 rounded bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition"
                          title="Open Blueprint details"
                        >
                          <Eye size={16} />
                        </button>
                        <button
                          onClick={() => handleDownloadPDF(item.project_id, item.name)}
                          className="p-1.5 rounded bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition"
                          title="Download PDF report"
                        >
                          <FileDown size={16} />
                        </button>
                        <button
                          onClick={() => handleDeleteProject(item.project_id)}
                          className="p-1.5 rounded bg-slate-800 text-slate-300 hover:text-red-400 hover:bg-red-500/10 transition"
                          title="Delete Project record"
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Structured Recommendation Modal Viewer */}
      {selectedProject && selectedRec && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-850 rounded-2xl w-full max-w-4xl max-h-[85vh] flex flex-col shadow-2xl relative overflow-hidden animate-scale-up">
            
            {/* Modal Header */}
            <div className="px-6 py-4 border-b border-slate-850 flex items-center justify-between bg-slate-950/40">
              <div>
                <h3 className="text-lg font-bold text-white">{selectedProject.name} Specification</h3>
                <span className="text-xs text-slate-400">{selectedProject.domain}</span>
              </div>
              <button
                onClick={() => { setSelectedProject(null); setSelectedRec(null); }}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
              >
                <X size={20} />
              </button>
            </div>

            {/* Modal Tabs Row */}
            <div className="flex border-b border-slate-850 bg-slate-950/10 text-sm overflow-x-auto">
              <button
                onClick={() => setActiveTab('specs')}
                className={`px-6 py-3 font-semibold border-b-2 transition-all ${
                  activeTab === 'specs' ? 'border-blue-600 text-blue-400 bg-slate-950/20' : 'border-transparent text-slate-400 hover:text-white'
                }`}
              >
                1. System Specs
              </button>
              <button
                onClick={() => setActiveTab('timeline')}
                className={`px-6 py-3 font-semibold border-b-2 transition-all ${
                  activeTab === 'timeline' ? 'border-blue-600 text-blue-400 bg-slate-950/20' : 'border-transparent text-slate-400 hover:text-white'
                }`}
              >
                2. Timeline & Cost
              </button>
              <button
                onClick={() => setActiveTab('sprints')}
                className={`px-6 py-3 font-semibold border-b-2 transition-all ${
                  activeTab === 'sprints' ? 'border-blue-600 text-blue-400 bg-slate-950/20' : 'border-transparent text-slate-400 hover:text-white'
                }`}
              >
                3. Sprints & Risks
              </button>
              <button
                onClick={() => setActiveTab('diagram')}
                className={`px-6 py-3 font-semibold border-b-2 transition-all ${
                  activeTab === 'diagram' ? 'border-blue-600 text-blue-400 bg-slate-950/20' : 'border-transparent text-slate-400 hover:text-white'
                }`}
              >
                4. Architecture Diagram
              </button>
            </div>

            {/* Modal Content Scroll Area */}
            <div className="p-6 overflow-y-auto flex-1 space-y-6 text-left">
              
              {activeTab === 'specs' && (
                <div className="space-y-6">
                  {/* Executive Summary */}
                  <div>
                    <h4 className="text-sm font-bold uppercase text-blue-400 tracking-wider mb-2">Executive Summary</h4>
                    <p className="text-sm text-slate-300 bg-slate-950/30 p-4 rounded-lg border border-slate-850 leading-relaxed">
                      {selectedRec.summary}
                    </p>
                  </div>

                  {/* Core Stack Grid */}
                  <div>
                    <h4 className="text-sm font-bold uppercase text-blue-400 tracking-wider mb-3">Recommended Components</h4>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                      <div className="bg-slate-950/20 p-4 rounded-lg border border-slate-850/60 flex items-start gap-3">
                        <Layers className="text-blue-500 shrink-0 mt-0.5" size={18} />
                        <div>
                          <p className="text-xs text-slate-400 font-semibold">Architecture Pattern</p>
                          <p className="text-sm font-bold text-white mt-1">{selectedRec.architecture_pattern}</p>
                        </div>
                      </div>
                      <div className="bg-slate-950/20 p-4 rounded-lg border border-slate-850/60 flex items-start gap-3">
                        <HardDrive className="text-indigo-400 shrink-0 mt-0.5" size={18} />
                        <div>
                          <p className="text-xs text-slate-400 font-semibold">Backend Engine</p>
                          <p className="text-sm font-bold text-white mt-1">{selectedRec.backend_tech}</p>
                        </div>
                      </div>
                      <div className="bg-slate-950/20 p-4 rounded-lg border border-slate-850/60 flex items-start gap-3">
                        <Layers className="text-sky-400 shrink-0 mt-0.5" size={18} />
                        <div>
                          <p className="text-xs text-slate-400 font-semibold">Frontend Platform</p>
                          <p className="text-sm font-bold text-white mt-1">{selectedRec.frontend_tech}</p>
                        </div>
                      </div>
                      <div className="bg-slate-950/20 p-4 rounded-lg border border-slate-850/60 flex items-start gap-3">
                        <HardDrive className="text-emerald-400 shrink-0 mt-0.5" size={18} />
                        <div>
                          <p className="text-xs text-slate-400 font-semibold">Database Sizing</p>
                          <p className="text-sm font-bold text-white mt-1">{selectedRec.database_tech}</p>
                        </div>
                      </div>
                      <div className="bg-slate-950/20 p-4 rounded-lg border border-slate-850/60 flex items-start gap-3">
                        <Cloud className="text-orange-400 shrink-0 mt-0.5" size={18} />
                        <div>
                          <p className="text-xs text-slate-400 font-semibold">Cloud Platform</p>
                          <p className="text-sm font-bold text-white mt-1">{selectedRec.cloud_platform}</p>
                        </div>
                      </div>
                      <div className="bg-slate-950/20 p-4 rounded-lg border border-slate-850/60 flex items-start gap-3">
                        <ShieldCheck className="text-teal-400 shrink-0 mt-0.5" size={18} />
                        <div>
                          <p className="text-xs text-slate-400 font-semibold">Container Hosting</p>
                          <p className="text-sm font-bold text-white mt-1">{selectedRec.deployment_strategy}</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Comparisons */}
                  <div>
                    <h4 className="text-sm font-bold uppercase text-blue-400 tracking-wider mb-3">Component Alternatives & Trade-Offs</h4>
                    <div className="space-y-4">
                      {selectedRec.comparison_data.map((item, index) => (
                        <div key={index} className="bg-slate-950/20 border border-slate-850 p-4 rounded-lg">
                          <p className="text-sm font-bold text-white mb-2 uppercase tracking-wide">
                            {item.technology_type} Comparison Matrix
                          </p>
                          <p className="text-sm text-slate-400 italic mb-3">Justification: {item.justification}</p>
                          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                            {[item.option_1, item.option_2, item.option_3].map((opt, oIdx) => (
                              <div 
                                key={oIdx} 
                                className={`p-3 rounded-lg border text-xs ${
                                  opt.is_chosen 
                                    ? 'bg-blue-600/10 border-blue-500/30' 
                                    : 'bg-slate-950/40 border-slate-850/60'
                                }`}
                              >
                                <div className="flex items-center justify-between font-bold mb-1 text-white">
                                  <span>{opt.name}</span>
                                  {opt.is_chosen && <span className="text-[10px] bg-blue-600 text-white px-1.5 py-0.2 rounded font-semibold uppercase">Chosen</span>}
                                </div>
                                <div className="grid grid-cols-2 gap-y-1 text-slate-400 mt-2">
                                  <span>Performance:</span> <span className="text-white text-right">{opt.performance}</span>
                                  <span>Scalability:</span> <span className="text-white text-right">{opt.scalability}</span>
                                  <span>Cost Efficiency:</span> <span className="text-white text-right">{opt.cost}</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'timeline' && (
                <div className="space-y-6">
                  {/* Cost Estimator */}
                  <div>
                    <h4 className="text-sm font-bold uppercase text-blue-400 tracking-wider mb-3">Monthly Infrastructure Sizing Cost</h4>
                    <div className="overflow-hidden border border-slate-850 rounded-lg">
                      <table className="w-full text-left text-sm border-collapse">
                        <thead>
                          <tr className="bg-slate-950/40 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-850">
                            <th className="py-3 px-4">Component Resource</th>
                            <th className="py-3 px-4">Sizing Description</th>
                            <th className="py-3 px-4 text-right">Cost/Month</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-850 bg-slate-950/10">
                          {Object.entries(selectedRec.cost_estimation_data).map(([key, val]) => {
                            if (key === 'total_monthly_cost') return null;
                            return (
                              <tr key={key} className="hover:bg-slate-900/20">
                                <td className="py-3 px-4 font-bold text-white capitalize">{key}</td>
                                <td className="py-3 px-4 text-slate-400">{val.description}</td>
                                <td className="py-3 px-4 text-right text-emerald-400 font-bold">${val.monthly_cost.toFixed(2)}</td>
                              </tr>
                            );
                          })}
                          <tr className="bg-slate-950/30 border-t border-slate-800 font-bold text-white">
                            <td className="py-4 px-4">Total Estimated Infrastructure Budget</td>
                            <td className="py-4 px-4"></td>
                            <td className="py-4 px-4 text-right text-lg text-emerald-400">
                              ${selectedRec.cost_estimation_data.total_monthly_cost?.toFixed(2)} / mo
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>

                  {/* Milestones Timeline */}
                  <div>
                    <h4 className="text-sm font-bold uppercase text-blue-400 tracking-wider mb-3">Project Weekly Milestones</h4>
                    <div className="space-y-4">
                      {selectedRec.timeline_data.map((step, idx) => (
                        <div key={idx} className="bg-slate-950/20 border border-slate-850 p-4 rounded-lg flex items-start gap-4">
                          <div className="w-10 h-10 rounded-full bg-blue-600/10 border border-blue-500/20 text-blue-400 shrink-0 flex items-center justify-center font-bold">
                            W{step.week}
                          </div>
                          <div>
                            <h5 className="text-sm font-bold text-white">{step.milestone}</h5>
                            <ul className="mt-2 space-y-1">
                              {step.deliverables.map((d, dIdx) => (
                                <li key={dIdx} className="text-xs text-slate-400 flex items-center gap-1.5">
                                  <span className="w-1 h-1 rounded-full bg-blue-500"></span>
                                  {d}
                                </li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'sprints' && (
                <div className="space-y-6">
                  {/* Sprint Planner */}
                  <div>
                    <h4 className="text-sm font-bold uppercase text-blue-400 tracking-wider mb-3">Agile Sprint Backlogs</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {selectedRec.sprint_plan_data.map((s, idx) => (
                        <div key={idx} className="bg-slate-950/20 border border-slate-850 p-4 rounded-lg">
                          <div className="flex items-center gap-2 mb-2 text-white font-bold">
                            <ListTodo className="text-blue-500" size={16} />
                            <span>{s.sprint}</span>
                          </div>
                          <p className="text-xs text-slate-400 italic mb-3">{s.goal}</p>
                          <ul className="space-y-1.5">
                            {s.backlog.map((t, tIdx) => (
                              <li key={tIdx} className="text-xs text-slate-300 bg-slate-950/30 px-2.5 py-1 rounded border border-slate-850/50">
                                {t}
                              </li>
                            ))}
                          </ul>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Risks Register */}
                  <div>
                    <h4 className="text-sm font-bold uppercase text-blue-400 tracking-wider mb-3">Risk Assessment & Mitigation Matrix</h4>
                    <div className="space-y-4">
                      {selectedRec.risk_analysis_data.map((risk, idx) => (
                        <div key={idx} className="bg-slate-950/20 border border-slate-850 p-4 rounded-lg">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-bold text-white">{risk.risk_type} Risk</span>
                            <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                              risk.impact === 'High' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20'
                            }`}>
                              {risk.impact} Impact
                            </span>
                          </div>
                          <p className="text-xs text-slate-300 leading-relaxed mb-2">{risk.description}</p>
                          <div className="bg-blue-600/5 border border-blue-500/10 p-2.5 rounded text-xs text-blue-400 mt-2">
                            <strong>Mitigation Strategy:</strong> {risk.mitigation}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'diagram' && (
                <div className="space-y-6">
                  <div>
                    <h4 className="text-sm font-bold uppercase text-blue-400 tracking-wider mb-2">Mermaid System Flowchart</h4>
                    <p className="text-xs text-slate-400 mb-3">Copy this syntax and paste it into any Mermaid diagram viewer.</p>
                    <pre className="text-xs text-slate-300 bg-slate-950/40 p-4 rounded-lg border border-slate-850 overflow-x-auto whitespace-pre-wrap font-mono">
                      {selectedRec.diagram_mermaid}
                    </pre>
                  </div>
                </div>
              )}

            </div>

            {/* Modal Footer */}
            <div className="px-6 py-4 border-t border-slate-850 bg-slate-950/40 flex items-center justify-between">
              <span className="text-xs text-slate-500">
                Generated at {new Date(selectedRec.created_at).toLocaleString()}
              </span>
              <button
                onClick={() => handleDownloadPDF(selectedProject.id, selectedProject.name)}
                className="glass-btn-primary"
              >
                <FileDown size={16} />
                Export PDF Briefing
              </button>
            </div>

          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
