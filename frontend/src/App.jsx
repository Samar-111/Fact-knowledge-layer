import React, { useState, useEffect } from 'react';
import { 
  FileText, Upload, CheckCircle2, AlertTriangle, HelpCircle, RefreshCw, 
  GitBranch, Search, Filter, ShieldAlert, Sparkles, BookOpen, ExternalLink,
  Layers, Database, Cpu, ArrowRight, Activity, Award, Trash2
} from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('showcase');
  const [showcaseCases, setShowcaseCases] = useState([]);
  const [facts, setFacts] = useState([]);
  const [relationships, setRelationships] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterCategory, setFilterCategory] = useState('ALL');

  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    setLoading(true);
    try {
      const [resShowcase, resFacts, resRels, resDocs, resGraph] = await Promise.all([
        fetch('/api/showcase').then(r => r.json()),
        fetch('/api/facts').then(r => r.json()),
        fetch('/api/relationships').then(r => r.json()),
        fetch('/api/documents').then(r => r.json()),
        fetch('/api/graph').then(r => r.json())
      ]);

      setShowcaseCases(resShowcase || []);
      setFacts(resFacts || []);
      setRelationships(resRels || []);
      setDocuments(resDocs || []);
      setGraphData(resGraph || { nodes: [], edges: [] });
    } catch (err) {
      console.error('Failed to fetch data from API:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    setUploadStatus('Uploading and analyzing PDF layout...');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error('Upload failed');
      const data = await res.json();

      setUploadStatus(`Success! Processed ${data.page_count} pages, extracted ${data.extracted_facts_count} facts, found ${data.new_relationships_found} relationships.`);
      await fetchInitialData();
    } catch (err) {
      setUploadStatus(`Error: ${err.message}`);
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDocument = async (docId) => {
    try {
      const res = await fetch(`/api/documents/${docId}`, {
        method: 'DELETE',
      });
      if (!res.ok) throw new Error('Failed to delete document');
      await fetchInitialData();
    } catch (err) {
      alert(`Delete Error: ${err.message}`);
    }
  };

  const filteredFacts = facts.filter(f => {
    const matchesSearch = searchQuery === '' || 
      f.metric_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      f.doc_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      f.subject.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesCategory = filterCategory === 'ALL' || f.subject.toUpperCase().includes(filterCategory);
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="bg-gradient-to-tr from-indigo-500 to-emerald-400 p-2.5 rounded-xl shadow-lg shadow-indigo-500/20">
            <Layers className="w-6 h-6 text-slate-950 font-bold" />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-white via-slate-200 to-indigo-300 bg-clip-text text-transparent">
              Fact Knowledge Layer
            </h1>
            <p className="text-xs text-slate-400 font-mono">Grounded AI Fact Extraction & Reconciliation System</p>
          </div>
        </div>

        <nav className="flex items-center space-x-1 bg-slate-950/80 p-1.5 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab('showcase')}
            className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all flex items-center space-x-2 ${
              activeTab === 'showcase'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
            }`}
          >
            <Award className="w-4 h-4" />
            <span>4 Showcase Cases</span>
          </button>

          <button
            onClick={() => setActiveTab('explorer')}
            className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all flex items-center space-x-2 ${
              activeTab === 'explorer'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
            }`}
          >
            <Search className="w-4 h-4" />
            <span>Fact Inspector ({facts.length})</span>
          </button>

          <button
            onClick={() => setActiveTab('graph')}
            className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all flex items-center space-x-2 ${
              activeTab === 'graph'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
            }`}
          >
            <GitBranch className="w-4 h-4" />
            <span>Knowledge Graph</span>
          </button>

          <button
            onClick={() => setActiveTab('upload')}
            className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all flex items-center space-x-2 ${
              activeTab === 'upload'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
            }`}
          >
            <Upload className="w-4 h-4" />
            <span>Upload PDF</span>
          </button>

          <button
            onClick={() => setActiveTab('approach')}
            className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all flex items-center space-x-2 ${
              activeTab === 'approach'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
            }`}
          >
            <BookOpen className="w-4 h-4" />
            <span>Problem Explanation</span>
          </button>
        </nav>

        <div className="flex items-center space-x-3">
          <span className="flex items-center space-x-2 bg-emerald-950/80 border border-emerald-800/80 text-emerald-400 text-xs px-3 py-1.5 rounded-full font-mono">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>API Online</span>
          </span>
          <button 
            onClick={fetchInitialData}
            title="Refresh Data"
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </header>

      <main className="flex-1 p-6 max-w-7xl w-full mx-auto space-y-6">

        {activeTab === 'showcase' && (
          <div className="space-y-6">
            <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-indigo-900/50 rounded-2xl p-6 shadow-xl">
              <div className="flex items-start justify-between">
                <div>
                  <h2 className="text-2xl font-extrabold text-white flex items-center space-x-3">
                    <span>Benchmark Showcase: Four Required Fact Cases</span>
                  </h2>
                  <p className="text-slate-400 text-sm mt-1">
                    Demonstrating automated discovery, evidence grounding, and contextual reasoning across Economic Survey 2024-25, RBI Annual Report 2024-25, and IMF Country Report 2025.
                  </p>
                </div>
              </div>
            </div>

            {loading ? (
              <div className="text-center py-20">
                <RefreshCw className="w-8 h-8 text-indigo-400 animate-spin mx-auto mb-3" />
                <p className="text-slate-400 text-sm">Loading Fact Knowledge Layer reasoning engine...</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-6">
                {showcaseCases.map((c) => (
                  <div 
                    key={c.case_number}
                    className="bg-slate-900/90 border border-slate-800 hover:border-indigo-800/80 rounded-2xl p-6 transition-all shadow-xl space-y-4"
                  >
                    <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                      <div className="flex items-center space-x-3">
                        <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm ${
                          c.relationship_type === 'CORROBORATED' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                          c.relationship_type === 'CONTRADICTED' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                          c.relationship_type === 'RECONCILED' ? 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/30' :
                          'bg-purple-500/20 text-purple-400 border border-purple-500/30'
                        }`}>
                          #{c.case_number}
                        </div>
                        <div>
                          <h3 className="text-lg font-bold text-white">{c.title}</h3>
                          <p className="text-xs text-slate-400">Metric: <span className="text-slate-200 font-semibold">{c.context_diff?.metric || c.fact_a?.metric_name}</span></p>
                        </div>
                      </div>

                      <div className="flex items-center space-x-2">
                        <span className={`text-xs font-bold uppercase tracking-wider px-3 py-1.5 rounded-full border ${
                          c.relationship_type === 'CORROBORATED' ? 'bg-emerald-950/80 text-emerald-300 border-emerald-800' :
                          c.relationship_type === 'CONTRADICTED' ? 'bg-amber-950/80 text-amber-300 border-amber-800' :
                          c.relationship_type === 'RECONCILED' ? 'bg-indigo-950/80 text-indigo-300 border-indigo-800' :
                          'bg-purple-950/80 text-purple-300 border-purple-800'
                        }`}>
                          {c.relationship_type}
                        </span>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {c.fact_a && (
                        <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800/80 space-y-2">
                          <div className="flex items-center justify-between text-xs text-slate-400">
                            <span className="font-semibold text-indigo-300 flex items-center space-x-1">
                              <FileText className="w-3.5 h-3.5" />
                              <span>{c.fact_a.doc_name}</span>
                            </span>
                            <span className="bg-slate-800 px-2 py-0.5 rounded text-slate-300 font-mono">Page {c.fact_a.page_number}</span>
                          </div>

                          <div className="flex items-baseline justify-between pt-1">
                            <span className="text-2xl font-extrabold text-white">{c.fact_a.value_text || `${c.fact_a.value}${c.fact_a.unit}`}</span>
                            <span className="text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded font-mono">{c.fact_a.time_period}</span>
                          </div>

                          <div className="text-xs text-slate-400 space-y-1">
                            <p><span className="text-slate-500">Estimate Stage:</span> <span className="text-slate-300">{c.fact_a.estimate_stage}</span></p>
                          </div>

                          <div className="mt-2 text-xs bg-slate-900/90 p-3 rounded-lg border border-slate-800 text-slate-300 italic font-mono leading-relaxed">
                            "{c.fact_a.exact_quote}"
                          </div>
                        </div>
                      )}

                      {c.fact_b && (
                        <div className="bg-slate-950/60 rounded-xl p-4 border border-slate-800/80 space-y-2">
                          <div className="flex items-center justify-between text-xs text-slate-400">
                            <span className="font-semibold text-indigo-300 flex items-center space-x-1">
                              <FileText className="w-3.5 h-3.5" />
                              <span>{c.fact_b.doc_name}</span>
                            </span>
                            <span className="bg-slate-800 px-2 py-0.5 rounded text-slate-300 font-mono">Page {c.fact_b.page_number}</span>
                          </div>

                          <div className="flex items-baseline justify-between pt-1">
                            <span className="text-2xl font-extrabold text-white">{c.fact_b.value_text || `${c.fact_b.value}${c.fact_b.unit}`}</span>
                            <span className="text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded font-mono">{c.fact_b.time_period}</span>
                          </div>

                          <div className="text-xs text-slate-400 space-y-1">
                            <p><span className="text-slate-500">Estimate Stage:</span> <span className="text-slate-300">{c.fact_b.estimate_stage}</span></p>
                          </div>

                          <div className="mt-2 text-xs bg-slate-900/90 p-3 rounded-lg border border-slate-800 text-slate-300 italic font-mono leading-relaxed">
                            "{c.fact_b.exact_quote}"
                          </div>
                        </div>
                      )}
                    </div>

                    <div className="bg-indigo-950/20 border border-indigo-900/40 p-4 rounded-xl space-y-2">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-indigo-400 flex items-center space-x-2">
                        <Sparkles className="w-4 h-4" />
                        <span>System Reasoning & Context Resolution</span>
                      </h4>
                      <p className="text-xs text-slate-300 leading-relaxed font-sans whitespace-pre-line">
                        {c.reasoning}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'explorer' && (
          <div className="space-y-6">
            <div className="flex flex-col md:flex-row items-center justify-between gap-4 bg-slate-900 p-4 rounded-2xl border border-slate-800">
              <div className="relative flex-1 w-full">
                <Search className="w-4 h-4 absolute left-3 top-3.5 text-slate-500" />
                <input
                  type="text"
                  placeholder="Search facts by metric name, document, or subject..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-4 py-2.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex items-center space-x-2 w-full md:w-auto">
                <Filter className="w-4 h-4 text-slate-400" />
                <select
                  value={filterCategory}
                  onChange={(e) => setFilterCategory(e.target.value)}
                  className="bg-slate-950 border border-slate-800 text-xs rounded-xl px-3 py-2.5 text-slate-200 focus:outline-none focus:border-indigo-500"
                >
                  <option value="ALL">All Categories</option>
                  <option value="INFLATION">Inflation & Prices</option>
                  <option value="NATIONAL">National Accounts / GDP</option>
                  <option value="EXTERNAL">External Sector / Trade</option>
                  <option value="FOREIGN">Foreign Investment</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filteredFacts.map((fact) => (
                <div key={fact.id} className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 hover:border-slate-700 transition-all flex flex-col justify-between space-y-3">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <span className="bg-indigo-950/80 border border-indigo-800/80 text-indigo-300 px-2.5 py-1 rounded-full font-mono">{fact.subject}</span>
                      <span className="text-slate-400 font-mono flex items-center space-x-1">
                        <FileText className="w-3.5 h-3.5 text-slate-500" />
                        <span>p. {fact.page_number}</span>
                      </span>
                    </div>

                    <h4 className="text-base font-bold text-white">{fact.metric_name}</h4>

                    <div className="flex items-baseline space-x-2">
                      <span className="text-2xl font-black text-emerald-400">{fact.value_text || `${fact.value} ${fact.unit}`}</span>
                      <span className="text-xs text-slate-400 font-mono">[{fact.time_period}]</span>
                    </div>

                    <p className="text-xs text-slate-400">
                      <span className="text-slate-500">Stage:</span> <span className="text-slate-300">{fact.estimate_stage}</span>
                    </p>

                    <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800 text-xs text-slate-300 italic font-mono leading-relaxed">
                      "{fact.exact_quote}"
                    </div>
                  </div>

                  <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-500">
                    <span>Doc: <strong className="text-slate-400">{fact.doc_name}</strong></span>
                    <span className="bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-mono">Conf: {(fact.confidence * 100).toFixed(0)}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'graph' && (
          <div className="space-y-6">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
              <h3 className="text-lg font-bold text-white flex items-center space-x-2">
                <GitBranch className="w-5 h-5 text-indigo-400" />
                <span>Fact Knowledge Graph Topology</span>
              </h3>
              <p className="text-xs text-slate-400">
                Visualizing extracted nodes (facts) and directed edges (corroborations, contradictions, and reconciliations).
              </p>

              <div className="space-y-3">
                {relationships.map((rel) => (
                  <div key={rel.id} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <span className={`text-xs font-mono font-bold px-2.5 py-1 rounded border ${
                        rel.relationship_type === 'CORROBORATED' ? 'bg-emerald-950 text-emerald-400 border-emerald-800' :
                        rel.relationship_type === 'CONTRADICTED' ? 'bg-amber-950 text-amber-400 border-amber-800' :
                        rel.relationship_type === 'RECONCILED' ? 'bg-indigo-950 text-indigo-400 border-indigo-800' :
                        'bg-purple-950 text-purple-400 border-purple-800'
                      }`}>
                        {rel.relationship_type}
                      </span>

                      <div className="text-xs">
                        <span className="text-slate-200 font-semibold">{rel.fact_a_doc} ({rel.fact_a_val})</span>
                        <ArrowRight className="w-3.5 h-3.5 inline mx-2 text-slate-500" />
                        <span className="text-slate-200 font-semibold">{rel.fact_b_doc} ({rel.fact_b_val})</span>
                      </div>
                    </div>

                    <span className="text-xs text-slate-400 font-mono hidden md:inline">{rel.fact_a_metric}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'upload' && (
          <div className="max-w-2xl mx-auto space-y-6">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 text-center space-y-4">
              <div className="w-16 h-16 bg-indigo-950 border border-indigo-800/80 rounded-2xl flex items-center justify-center mx-auto text-indigo-400">
                <Upload className="w-8 h-8" />
              </div>

              <div>
                <h3 className="text-xl font-bold text-white">Upload New PDF Document</h3>
                <p className="text-xs text-slate-400 mt-1">
                  Upload any economic, financial, or corporate PDF. The Knowledge Layer will dynamically parse tables, extract grounded facts, and link them to existing knowledge.
                </p>
              </div>

              <label className="inline-flex items-center justify-center space-x-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold px-6 py-3 rounded-xl cursor-pointer transition-all shadow-lg shadow-indigo-600/30">
                <span>Select PDF File</span>
                <input type="file" accept=".pdf" onChange={handleFileUpload} className="hidden" />
              </label>

              {uploading && (
                <div className="flex items-center justify-center space-x-2 text-xs text-indigo-400 pt-3">
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>{uploadStatus}</span>
                </div>
              )}

              {uploadStatus && !uploading && (
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs text-slate-300 font-mono">
                  {uploadStatus}
                </div>
              )}
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-3">
              <h4 className="text-sm font-bold text-white flex items-center space-x-2">
                <Database className="w-4 h-4 text-emerald-400" />
                <span>Active Knowledge Layer Documents ({documents.length})</span>
              </h4>

              <div className="space-y-2">
                {documents.map((doc) => (
                  <div key={doc.id} className="bg-slate-950 p-3.5 rounded-xl border border-slate-800/80 flex items-center justify-between text-xs">
                    <div className="flex items-center space-x-3">
                      <FileText className="w-4 h-4 text-indigo-400" />
                      <span className="font-semibold text-slate-200">{doc.title}</span>
                    </div>

                    <div className="flex items-center space-x-3">
                      <span className="text-slate-400 font-mono">{doc.page_count} Pages</span>
                      <button
                        onClick={() => handleDeleteDocument(doc.id)}
                        title="Delete document and its extracted facts"
                        className="p-1.5 rounded-lg bg-rose-950/60 border border-rose-800/60 hover:bg-rose-900 text-rose-300 transition-colors"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'approach' && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 space-y-6 text-sm text-slate-300 leading-relaxed">
            <div>
              <h2 className="text-2xl font-extrabold text-white mb-2">Problem Statement Explanation & Technical Approach</h2>
            </div>

            <div className="space-y-4">
              <h3 className="text-base font-bold text-indigo-400 border-b border-slate-800 pb-2">What Does This Project Do?</h3>
              <p>
                Important numerical and semantic facts are scattered across reports (e.g. Economic Surveys, Central Bank Annual Reports, IMF Country Assessments).
                These facts are often expressed differently, covered over varying time horizons, supported by other evidence, or appear contradictory.
              </p>
              <p>
                This project builds a <strong>Fact Knowledge Layer</strong> that:
              </p>
              <ul className="list-disc pl-5 space-y-1.5 text-xs text-slate-300">
                <li><strong>Extracts Atomic Facts:</strong> Pulls out metric names, numerical values, units, time periods, estimate stages, and geographic scope.</li>
                <li><strong>Source Evidence Grounding:</strong> Every extracted fact is anchored to its source PDF document, exact page number, and verbatim text quote.</li>
                <li><strong>Automated Fact Relationship Discovery:</strong> Discovers when facts <em>corroborate</em>, <em>contradict</em>, or can be <em>contextually reconciled</em>.</li>
              </ul>
            </div>

            <div className="space-y-4">
              <h3 className="text-base font-bold text-indigo-400 border-b border-slate-800 pb-2">The Four Required Cases Handled</h3>
              <ol className="list-decimal pl-5 space-y-2 text-xs">
                <li><strong>Case 1 (Corroborated Fact):</strong> Retail Headline CPI Inflation averaging 4.6% in FY25 is corroborated across Economic Survey 2024-25, RBI Annual Report 2024-25, and IMF Country Report 2025.</li>
                <li><strong>Case 2 (Genuine Contradiction / Forecast Divergence):</strong> FY26 Real GDP Growth forecasts differ between Economic Survey (6.3-6.8%), RBI Annual Report (6.5%), and IMF Article IV Baseline (6.6%).</li>
                <li><strong>Case 3 (Contextual Reconciliation):</strong> Real GDP Growth for FY25 reported as 6.4% in Economic Survey vs 6.5% in RBI Annual Report. Reconciled by metadata context: Economic Survey used MoSPI First Advance Estimates (Jan 2025), whereas RBI used Second Advance Estimates (Feb 28, 2025).</li>
                <li><strong>Case 4 (Extraction / Reasoning Failure Handled):</strong> Disambiguating Gross FDI Inflows ($81.0B) vs Net FDI Inflows ($0.4B). Handled via an Accounting Identity Verifier & Scope Tagging Engine.</li>
              </ol>
            </div>
          </div>
        )}

      </main>
    </div>
  );
}
