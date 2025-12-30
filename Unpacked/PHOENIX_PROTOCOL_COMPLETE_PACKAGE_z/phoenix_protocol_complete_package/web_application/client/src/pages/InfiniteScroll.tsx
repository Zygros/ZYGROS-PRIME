/**
 * Infinite Scroll - Master Knowledge Thread Viewer
 * Living repository of all accumulated knowledge, insights, and integrations
 */

import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
  Infinity,
  Search,
  Calendar,
  Download,
  RefreshCw,
  BookOpen,
  Archive,
  Database,
  TrendingUp,
  Clock,
  FileText
} from 'lucide-react';
import { Streamdown } from 'streamdown';

interface DailyUpdate {
  date: string;
  filename: string;
  summary: string;
}

export default function InfiniteScroll() {
  const [masterThread, setMasterThread] = useState<string>('');
  const [dailyUpdates, setDailyUpdates] = useState<DailyUpdate[]>([]);
  const [selectedUpdate, setSelectedUpdate] = useState<string | null>(null);
  const [updateContent, setUpdateContent] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState<string>('');

  useEffect(() => {
    loadMasterThread();
    loadDailyUpdates();
  }, []);

  const loadMasterThread = async () => {
    try {
      const response = await fetch('/infinite_scroll/MASTER_THREAD.md');
      const text = await response.text();
      setMasterThread(text);
      
      // Extract last updated date from content
      const match = text.match(/\*\*Last Updated\*\*:\s*(\d{4}-\d{2}-\d{2})/);
      if (match) {
        setLastUpdated(match[1]);
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Failed to load master thread:', error);
      setLoading(false);
    }
  };

  const loadDailyUpdates = async () => {
    try {
      // For now, we'll manually list the updates we know exist
      // In production, this would query a directory listing API
      const updates: DailyUpdate[] = [
        {
          date: '2025-11-19',
          filename: '2025-11-19_update.md',
          summary: 'Initial creation of the Infinite Scroll knowledge compilation system'
        }
      ];
      setDailyUpdates(updates);
    } catch (error) {
      console.error('Failed to load daily updates:', error);
    }
  };

  const loadDailyUpdate = async (filename: string) => {
    try {
      const response = await fetch(`/infinite_scroll/daily_updates/${filename}`);
      const text = await response.text();
      setUpdateContent(text);
      setSelectedUpdate(filename);
    } catch (error) {
      console.error('Failed to load daily update:', error);
    }
  };

  const handleRefresh = () => {
    setLoading(true);
    loadMasterThread();
    loadDailyUpdates();
  };

  const handleExport = () => {
    const blob = new Blob([masterThread], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `infinite_scroll_master_thread_${new Date().toISOString().split('T')[0]}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const filteredContent = searchQuery
    ? masterThread.split('\n').filter(line =>
        line.toLowerCase().includes(searchQuery.toLowerCase())
      ).join('\n')
    : masterThread;

  return (
    <div className="min-h-screen bg-gradient-to-b from-[oklch(0.15_0.02_30)] to-[oklch(0.1_0.02_20)] p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <Infinity className="w-10 h-10 text-[oklch(0.65_0.15_30)]" />
              <div>
                <h1 className="text-4xl font-bold text-[oklch(0.9_0.05_30)]">
                  The Infinite Scroll
                </h1>
                <p className="text-[oklch(0.6_0.05_30)] text-sm">
                  Master Knowledge Thread • Last Updated: {lastUpdated || 'Loading...'}
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <Button
                onClick={handleRefresh}
                variant="outline"
                className="border-[oklch(0.65_0.15_30)] text-[oklch(0.65_0.15_30)]"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Refresh
              </Button>
              <Button
                onClick={handleExport}
                className="bg-[oklch(0.65_0.15_30)] hover:bg-[oklch(0.6_0.15_30)]"
              >
                <Download className="w-4 h-4 mr-2" />
                Export
              </Button>
            </div>
          </div>
          <p className="text-[oklch(0.7_0.05_30)] leading-relaxed">
            A living repository of all accumulated knowledge, insights, integrations, and system capabilities. 
            This master thread is continuously updated with new information from every conversation, 
            creating a comprehensive knowledge base that grows with each interaction.
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-4 gap-4 mb-8">
          <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-4">
            <div className="flex items-center gap-3">
              <BookOpen className="w-6 h-6 text-[oklch(0.65_0.15_30)]" />
              <div>
                <div className="text-xl font-bold text-[oklch(0.9_0.05_30)]">
                  {masterThread.split('\n').length}
                </div>
                <div className="text-xs text-[oklch(0.6_0.05_30)]">Total Lines</div>
              </div>
            </div>
          </Card>

          <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-4">
            <div className="flex items-center gap-3">
              <Calendar className="w-6 h-6 text-[oklch(0.7_0.15_40)]" />
              <div>
                <div className="text-xl font-bold text-[oklch(0.9_0.05_30)]">
                  {dailyUpdates.length}
                </div>
                <div className="text-xs text-[oklch(0.6_0.05_30)]">Daily Updates</div>
              </div>
            </div>
          </Card>

          <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-4">
            <div className="flex items-center gap-3">
              <Database className="w-6 h-6 text-[oklch(0.75_0.15_50)]" />
              <div>
                <div className="text-xl font-bold text-[oklch(0.9_0.05_30)]">
                  {masterThread.match(/###/g)?.length || 0}
                </div>
                <div className="text-xs text-[oklch(0.6_0.05_30)]">Knowledge Sections</div>
              </div>
            </div>
          </Card>

          <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-4">
            <div className="flex items-center gap-3">
              <TrendingUp className="w-6 h-6 text-[oklch(0.8_0.15_60)]" />
              <div>
                <div className="text-xl font-bold text-[oklch(0.9_0.05_30)]">
                  {masterThread.match(/\[x\]/g)?.length || 0}
                </div>
                <div className="text-xs text-[oklch(0.6_0.05_30)]">Tasks Completed</div>
              </div>
            </div>
          </Card>
        </div>

        <div className="grid grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="col-span-2 space-y-6">
            {/* Search */}
            <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[oklch(0.6_0.05_30)]" />
                <Input
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search the Infinite Scroll..."
                  className="pl-10 bg-[oklch(0.2_0.02_30)] border-[oklch(0.3_0.05_30)]"
                />
              </div>
            </Card>

            {/* Master Thread Content */}
            <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-8">
              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <RefreshCw className="w-8 h-8 text-[oklch(0.65_0.15_30)] animate-spin" />
                </div>
              ) : (
                <div className="prose prose-invert max-w-none">
                  <Streamdown>{filteredContent}</Streamdown>
                </div>
              )}
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Daily Updates */}
            <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6">
              <div className="flex items-center gap-2 mb-4">
                <Clock className="w-5 h-5 text-[oklch(0.65_0.15_30)]" />
                <h3 className="text-lg font-semibold text-[oklch(0.9_0.05_30)]">
                  Daily Updates
                </h3>
              </div>
              <div className="space-y-2">
                {dailyUpdates.map((update) => (
                  <button
                    key={update.filename}
                    onClick={() => loadDailyUpdate(update.filename)}
                    className={`w-full text-left p-3 rounded-lg transition-colors ${
                      selectedUpdate === update.filename
                        ? 'bg-[oklch(0.65_0.15_30)]/20 border border-[oklch(0.65_0.15_30)]'
                        : 'bg-[oklch(0.2_0.02_30)] border border-[oklch(0.3_0.05_30)] hover:border-[oklch(0.5_0.1_30)]'
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <FileText className="w-4 h-4 text-[oklch(0.65_0.15_30)]" />
                      <span className="text-sm font-semibold text-[oklch(0.9_0.05_30)]">
                        {update.date}
                      </span>
                    </div>
                    <p className="text-xs text-[oklch(0.7_0.05_30)] line-clamp-2">
                      {update.summary}
                    </p>
                  </button>
                ))}
              </div>
            </Card>

            {/* Quick Actions */}
            <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6">
              <h3 className="text-lg font-semibold text-[oklch(0.9_0.05_30)] mb-4">
                Quick Actions
              </h3>
              <div className="space-y-2">
                <Button
                  variant="outline"
                  className="w-full justify-start"
                  onClick={() => window.open('/infinite_scroll/MASTER_THREAD.md', '_blank')}
                >
                  <BookOpen className="w-4 h-4 mr-2" />
                  View Raw Markdown
                </Button>
                <Button
                  variant="outline"
                  className="w-full justify-start"
                  onClick={() => alert('Archive feature coming soon!')}
                >
                  <Archive className="w-4 h-4 mr-2" />
                  Browse Archives
                </Button>
                <Button
                  variant="outline"
                  className="w-full justify-start"
                  onClick={() => alert('Knowledge base feature coming soon!')}
                >
                  <Database className="w-4 h-4 mr-2" />
                  Knowledge Base
                </Button>
              </div>
            </Card>

            {/* System Info */}
            <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6">
              <h3 className="text-lg font-semibold text-[oklch(0.9_0.05_30)] mb-4">
                System Info
              </h3>
              <div className="space-y-3 text-sm">
                <div>
                  <div className="text-[oklch(0.6_0.05_30)] mb-1">Version</div>
                  <Badge variant="secondary" className="bg-[oklch(0.65_0.15_30)]/20 text-[oklch(0.65_0.15_30)]">
                    1.0.0
                  </Badge>
                </div>
                <div>
                  <div className="text-[oklch(0.6_0.05_30)] mb-1">Status</div>
                  <Badge variant="secondary" className="bg-[oklch(0.65_0.15_120)]/20 text-[oklch(0.65_0.15_120)]">
                    Active
                  </Badge>
                </div>
                <div>
                  <div className="text-[oklch(0.6_0.05_30)] mb-1">Next Update</div>
                  <div className="text-[oklch(0.8_0.05_30)]">
                    {new Date(Date.now() + 86400000).toLocaleDateString()}
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>

        {/* Selected Update Modal */}
        {selectedUpdate && updateContent && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-8 z-50">
            <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-8 max-w-4xl max-h-[80vh] overflow-auto">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-[oklch(0.9_0.05_30)]">
                  Daily Update: {selectedUpdate.replace('_update.md', '')}
                </h2>
                <Button
                  variant="ghost"
                  onClick={() => {
                    setSelectedUpdate(null);
                    setUpdateContent('');
                  }}
                >
                  Close
                </Button>
              </div>
              <div className="prose prose-invert max-w-none">
                <Streamdown>{updateContent}</Streamdown>
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
}
