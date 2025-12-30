// phoenix_web_interface.jsx
// React interface for Phoenix Protocol
// Connects to Flask API at localhost:5001 or phoenixos-biionmkv.manus.space

import React, { useState, useEffect } from 'react';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:5001';
const API_KEY = process.env.REACT_APP_API_KEY || '';

export default function PhoenixProtocol() {
  const [status, setStatus] = useState(null);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [ingestStatus, setIngestStatus] = useState(null);

  const headers = {
    'Content-Type': 'application/json',
    ...(API_KEY && { 'X-API-Key': API_KEY })
  };

  // Load status on mount
  useEffect(() => {
    fetchStatus();
  }, []);

  const fetchStatus = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/status`, { headers });
      const data = await res.json();
      setStatus(data);
    } catch (err) {
      console.error('Status fetch failed:', err);
    }
  };

  const handleQuery = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/query`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ query, n_results: 5 })
      });
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error('Query failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleIngestText = async () => {
    const text = prompt('Enter text to ingest:');
    if (!text) return;
    const id = `inline-${Date.now()}`;

    try {
      const res = await fetch(`${API_BASE}/api/ingest`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          documents: [{ id, text, metadata: { path: `inline:${id}` } }]
        })
      });
      const data = await res.json();
      setIngestStatus(`Added ${data.added} document(s)`);
      setTimeout(() => setIngestStatus(null), 3000);
    } catch (err) {
      console.error('Ingest failed:', err);
      setIngestStatus('Ingest failed');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black text-white">
      {/* Header */}
      <header className="border-b border-amber-500/30 bg-black/40 backdrop-blur">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="text-4xl">🐦‍🔥</div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">
                  Phoenix Protocol
                </h1>
                <p className="text-sm text-gray-400">Sovereign Archive Interface</p>
              </div>
            </div>
            
            {status && (
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${
                  status.status === 'OPERATIONAL' ? 'bg-green-500' : 'bg-amber-500'
                }`} />
                <span className="text-sm">{status.status}</span>
              </div>
            )}
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8 max-w-5xl">
        {/* System Status */}
        {status && (
          <div className="mb-8 p-6 bg-black/40 backdrop-blur border border-amber-500/30 rounded-lg">
            <h2 className="text-xl font-semibold mb-4 text-amber-400">System Status</h2>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-400">Node Identity:</span>
                <span className="ml-2 text-white">{status.node_identity}</span>
              </div>
              <div>
                <span className="text-gray-400">Archive DB:</span>
                <span className="ml-2 text-white">{status.sovereign_archive_db}</span>
              </div>
              <div>
                <span className="text-gray-400">Collection:</span>
                <span className="ml-2 text-white">{status.collection}</span>
              </div>
              <div>
                <span className="text-gray-400">Persist Dir:</span>
                <span className="ml-2 text-white text-xs">{status.persist_dir}</span>
              </div>
            </div>
          </div>
        )}

        {/* Query Interface */}
        <div className="mb-8 p-6 bg-black/40 backdrop-blur border border-amber-500/30 rounded-lg">
          <h2 className="text-xl font-semibold mb-4 text-amber-400">Query Sovereign Archive</h2>
          
          <form onSubmit={handleQuery} className="mb-6">
            <div className="flex gap-3">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your query..."
                className="flex-1 px-4 py-3 bg-black/60 border border-amber-500/30 rounded-lg 
                         text-white placeholder-gray-500 focus:outline-none focus:border-amber-500"
              />
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-600 
                         hover:from-amber-600 hover:to-orange-700 rounded-lg font-semibold
                         transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Querying...' : 'Query'}
              </button>
            </div>
          </form>

          {/* Results */}
          {results && (
            <div className="space-y-4">
              <div className="text-sm text-gray-400 mb-4">
                Query: <span className="text-white">{results.query}</span>
              </div>
              
              {results.retrieved_fragments?.length > 0 ? (
                results.retrieved_fragments.map((frag, i) => (
                  <div
                    key={i}
                    className="p-4 bg-black/60 border border-amber-500/20 rounded-lg"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div className="text-xs text-amber-400">
                        Rank #{frag.rank} • Distance: {frag.distance?.toFixed(4)}
                      </div>
                      <div className="text-xs text-gray-500">{frag.source}</div>
                    </div>
                    <p className="text-sm text-gray-200 leading-relaxed">
                      {frag.content}
                    </p>
                  </div>
                ))
              ) : (
                <div className="text-center text-gray-500 py-8">
                  No matching fragments found
                </div>
              )}
            </div>
          )}
        </div>

        {/* Quick Ingest */}
        <div className="p-6 bg-black/40 backdrop-blur border border-amber-500/30 rounded-lg">
          <h2 className="text-xl font-semibold mb-4 text-amber-400">Quick Actions</h2>
          
          <div className="flex gap-3">
            <button
              onClick={handleIngestText}
              className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg 
                       transition-all text-sm font-semibold"
            >
              Ingest Text
            </button>
            
            <button
              onClick={fetchStatus}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg 
                       transition-all text-sm font-semibold"
            >
              Refresh Status
            </button>
          </div>

          {ingestStatus && (
            <div className="mt-4 p-3 bg-green-500/20 border border-green-500/40 rounded text-sm">
              {ingestStatus}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-gray-500 text-sm">
          <p>Phoenix Protocol v∞ • Sovereign Architecture</p>
          <p className="mt-1">
            Hash: <span className="font-mono text-xs">4ae77229...beeb84c</span>
          </p>
        </div>
      </div>
    </div>
  );
}
