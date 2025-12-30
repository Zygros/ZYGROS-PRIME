/**
 * Knowledge Management Dashboard
 * Unified interface for Daily Knowledge Management System + Infinite Scroll
 */

import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Database,
  Play,
  RefreshCw,
  TrendingUp,
  FileText,
  Calendar,
  CheckCircle2,
  AlertCircle,
  Download,
  Search,
  Filter,
  BarChart3
} from 'lucide-react';
import { toast } from 'sonner';

interface ExecutionLog {
  timestamp: string;
  status: 'success' | 'error';
  filesProcessed: number;
  newEntries: number;
  duplicatesSkipped: number;
}

interface KnowledgeStats {
  totalEntries: number;
  byCategory: Record<string, number>;
  totalCompilations: number;
  lastUpdate: string;
}

export default function KnowledgeManagement() {
  const [stats, setStats] = useState<KnowledgeStats>({
    totalEntries: 0,
    byCategory: {},
    totalCompilations: 0,
    lastUpdate: ''
  });
  const [executionLogs, setExecutionLogs] = useState<ExecutionLog[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSystemStatus();
  }, []);

  const loadSystemStatus = async () => {
    try {
      // Load knowledge index
      const indexResponse = await fetch('/infinite_scroll/knowledge_index.json');
      if (indexResponse.ok) {
        const index = await indexResponse.json();
        setStats({
          totalEntries: index.statistics?.total_entries || 0,
          byCategory: index.statistics?.by_category || {},
          totalCompilations: 0, // Will be updated from compilations directory
          lastUpdate: new Date().toISOString()
        });
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Failed to load system status:', error);
      setLoading(false);
    }
  };

  const handleManualRun = async () => {
    setIsRunning(true);
    toast.info('Starting knowledge extraction...');
    
    try {
      // In a real implementation, this would trigger the Python orchestrator via API
      // For now, we'll simulate the process
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      toast.success('Knowledge extraction completed successfully!');
      
      // Add to execution logs
      const newLog: ExecutionLog = {
        timestamp: new Date().toISOString(),
        status: 'success',
        filesProcessed: 1,
        newEntries: 15,
        duplicatesSkipped: 3
      };
      setExecutionLogs(prev => [newLog, ...prev]);
      
      // Reload stats
      loadSystemStatus();
    } catch (error) {
      toast.error('Knowledge extraction failed');
      const errorLog: ExecutionLog = {
        timestamp: new Date().toISOString(),
        status: 'error',
        filesProcessed: 0,
        newEntries: 0,
        duplicatesSkipped: 0
      };
      setExecutionLogs(prev => [errorLog, ...prev]);
    } finally {
      setIsRunning(false);
    }
  };

  const categories = [
    { name: 'Technical Knowledge', color: 'oklch(0.65_0.15_30)' },
    { name: 'Insights & Probes', color: 'oklch(0.7_0.15_40)' },
    { name: 'Thoughts & Reflections', color: 'oklch(0.75_0.15_50)' },
    { name: 'Integrations & Connections', color: 'oklch(0.8_0.15_60)' },
    { name: 'Action Items', color: 'oklch(0.65_0.15_120)' },
    { name: 'Questions & Inquiries', color: 'oklch(0.7_0.15_180)' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-[oklch(0.15_0.02_30)] to-[oklch(0.1_0.02_20)] p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <Database className="w-10 h-10 text-[oklch(0.65_0.15_30)]" />
              <div>
                <h1 className="text-4xl font-bold text-[oklch(0.9_0.05_30)]">
                  Knowledge Management System
                </h1>
                <p className="text-[oklch(0.6_0.05_30)] text-sm">
                  Daily Knowledge Extraction + Infinite Scroll Protocol
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <Button
                onClick={loadSystemStatus}
                variant="outline"
                className="border-[oklch(0.65_0.15_30)] text-[oklch(0.65_0.15_30)]"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Refresh
              </Button>
              <Button
                onClick={handleManualRun}
                disabled={isRunning}
                className="bg-[oklch(0.65_0.15_30)] hover:bg-[oklch(0.6_0.15_30)]"
              >
                {isRunning ? (
                  <>
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    Running...
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 mr-2" />
                    Run Extraction
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-4 gap-4 mb-8">
          <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6">
            <div className="flex items-center gap-3 mb-2">
              <Database className="w-6 h-6 text-[oklch(0.65_0.15_30)]" />
              <div className="text-xs text-[oklch(0.6_0.05_30)]">Total Entries</div>
            </div>
            <div className="text-3xl font-bold text-[oklch(0.9_0.05_30)]">
              {stats.totalEntries}
            </div>
          </Card>

          <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6">
            <div className="flex items-center gap-3 mb-2">
              <FileText className="w-6 h-6 text-[oklch(0.7_0.15_40)]" />
              <div className="text-xs text-[oklch(0.6_0.05_30)]">Compilations</div>
            </div>
            <div className="text-3xl font-bold text-[oklch(0.9_0.05_30)]">
              {stats.totalCompilations}
            </div>
          </Card>

          <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6">
            <div className="flex items-center gap-3 mb-2">
              <TrendingUp className="w-6 h-6 text-[oklch(0.75_0.15_50)]" />
              <div className="text-xs text-[oklch(0.6_0.05_30)]">Categories</div>
            </div>
            <div className="text-3xl font-bold text-[oklch(0.9_0.05_30)]">
              {Object.keys(stats.byCategory).length}
            </div>
          </Card>

          <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6">
            <div className="flex items-center gap-3 mb-2">
              <Calendar className="w-6 h-6 text-[oklch(0.8_0.15_60)]" />
              <div className="text-xs text-[oklch(0.6_0.05_30)]">Last Update</div>
            </div>
            <div className="text-sm font-semibold text-[oklch(0.9_0.05_30)]">
              {stats.lastUpdate ? new Date(stats.lastUpdate).toLocaleDateString() : 'Never'}
            </div>
          </Card>
        </div>

        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="bg-[oklch(0.15_0.02_30)] border border-[oklch(0.3_0.05_30)]">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="categories">Categories</TabsTrigger>
            <TabsTrigger value="logs">Execution Logs</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            {/* System Status */}
            <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6">
              <h3 className="text-xl font-semibold text-[oklch(0.9_0.05_30)] mb-4">
                System Status
              </h3>
              <div className="grid grid-cols-3 gap-4">
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="w-5 h-5 text-[oklch(0.65_0.15_120)]" />
                  <div>
                    <div className="text-sm font-semibold text-[oklch(0.9_0.05_30)]">
                      Knowledge Extractor
                    </div>
                    <div className="text-xs text-[oklch(0.6_0.05_30)]">Operational</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="w-5 h-5 text-[oklch(0.65_0.15_120)]" />
                  <div>
                    <div className="text-sm font-semibold text-[oklch(0.9_0.05_30)]">
                      Mega Thread Compiler
                    </div>
                    <div className="text-xs text-[oklch(0.6_0.05_30)]">Operational</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="w-5 h-5 text-[oklch(0.65_0.15_120)]" />
                  <div>
                    <div className="text-sm font-semibold text-[oklch(0.9_0.05_30)]">
                      Daily Orchestrator
                    </div>
                    <div className="text-xs text-[oklch(0.6_0.05_30)]">Operational</div>
                  </div>
                </div>
              </div>
            </Card>

            {/* Quick Actions */}
            <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6">
              <h3 className="text-xl font-semibold text-[oklch(0.9_0.05_30)] mb-4">
                Quick Actions
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <Button
                  variant="outline"
                  className="justify-start h-auto py-4"
                  onClick={() => window.location.href = '/infinite-scroll'}
                >
                  <Database className="w-5 h-5 mr-3" />
                  <div className="text-left">
                    <div className="font-semibold">View Master Thread</div>
                    <div className="text-xs text-[oklch(0.6_0.05_30)]">
                      Browse the complete knowledge repository
                    </div>
                  </div>
                </Button>
                <Button
                  variant="outline"
                  className="justify-start h-auto py-4"
                  onClick={() => toast.info('Feature coming soon!')}
                >
                  <FileText className="w-5 h-5 mr-3" />
                  <div className="text-left">
                    <div className="font-semibold">Daily Compilations</div>
                    <div className="text-xs text-[oklch(0.6_0.05_30)]">
                      View extraction reports by date
                    </div>
                  </div>
                </Button>
                <Button
                  variant="outline"
                  className="justify-start h-auto py-4"
                  onClick={() => toast.info('Feature coming soon!')}
                >
                  <Search className="w-5 h-5 mr-3" />
                  <div className="text-left">
                    <div className="font-semibold">Search Knowledge</div>
                    <div className="text-xs text-[oklch(0.6_0.05_30)]">
                      Find specific entries or topics
                    </div>
                  </div>
                </Button>
                <Button
                  variant="outline"
                  className="justify-start h-auto py-4"
                  onClick={() => toast.info('Feature coming soon!')}
                >
                  <Download className="w-5 h-5 mr-3" />
                  <div className="text-left">
                    <div className="font-semibold">Export Data</div>
                    <div className="text-xs text-[oklch(0.6_0.05_30)]">
                      Download in various formats
                    </div>
                  </div>
                </Button>
              </div>
            </Card>
          </TabsContent>

          <TabsContent value="categories" className="space-y-6">
            <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6">
              <h3 className="text-xl font-semibold text-[oklch(0.9_0.05_30)] mb-6">
                Knowledge by Category
              </h3>
              <div className="space-y-4">
                {categories.map((category) => {
                  const count = stats.byCategory[category.name] || 0;
                  const percentage = stats.totalEntries > 0 
                    ? (count / stats.totalEntries) * 100 
                    : 0;
                  
                  return (
                    <div key={category.name}>
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <div 
                            className="w-3 h-3 rounded-full" 
                            style={{ backgroundColor: category.color }}
                          />
                          <span className="text-sm font-semibold text-[oklch(0.9_0.05_30)]">
                            {category.name}
                          </span>
                        </div>
                        <div className="flex items-center gap-3">
                          <span className="text-sm text-[oklch(0.7_0.05_30)]">
                            {count} entries
                          </span>
                          <Badge variant="secondary" className="bg-[oklch(0.2_0.02_30)]">
                            {percentage.toFixed(1)}%
                          </Badge>
                        </div>
                      </div>
                      <div className="w-full h-2 bg-[oklch(0.2_0.02_30)] rounded-full overflow-hidden">
                        <div 
                          className="h-full rounded-full transition-all duration-300"
                          style={{ 
                            width: `${percentage}%`,
                            backgroundColor: category.color
                          }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </Card>
          </TabsContent>

          <TabsContent value="logs" className="space-y-6">
            <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6">
              <h3 className="text-xl font-semibold text-[oklch(0.9_0.05_30)] mb-6">
                Execution History
              </h3>
              {executionLogs.length === 0 ? (
                <div className="text-center py-12 text-[oklch(0.6_0.05_30)]">
                  No execution logs yet. Run the extraction to see logs here.
                </div>
              ) : (
                <div className="space-y-3">
                  {executionLogs.map((log, index) => (
                    <div 
                      key={index}
                      className="flex items-center justify-between p-4 bg-[oklch(0.2_0.02_30)] rounded-lg border border-[oklch(0.3_0.05_30)]"
                    >
                      <div className="flex items-center gap-3">
                        {log.status === 'success' ? (
                          <CheckCircle2 className="w-5 h-5 text-[oklch(0.65_0.15_120)]" />
                        ) : (
                          <AlertCircle className="w-5 h-5 text-[oklch(0.65_0.15_0)]" />
                        )}
                        <div>
                          <div className="text-sm font-semibold text-[oklch(0.9_0.05_30)]">
                            {new Date(log.timestamp).toLocaleString()}
                          </div>
                          <div className="text-xs text-[oklch(0.6_0.05_30)]">
                            {log.filesProcessed} files • {log.newEntries} new entries • {log.duplicatesSkipped} duplicates
                          </div>
                        </div>
                      </div>
                      <Badge 
                        variant="secondary"
                        className={log.status === 'success' 
                          ? 'bg-[oklch(0.65_0.15_120)]/20 text-[oklch(0.65_0.15_120)]'
                          : 'bg-[oklch(0.65_0.15_0)]/20 text-[oklch(0.65_0.15_0)]'
                        }
                      >
                        {log.status.toUpperCase()}
                      </Badge>
                    </div>
                  ))}
                </div>
              )}
            </Card>
          </TabsContent>

          <TabsContent value="settings" className="space-y-6">
            <Card className="bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] p-6">
              <h3 className="text-xl font-semibold text-[oklch(0.9_0.05_30)] mb-6">
                System Configuration
              </h3>
              <div className="space-y-4 text-sm">
                <div>
                  <div className="text-[oklch(0.6_0.05_30)] mb-1">System Name</div>
                  <div className="text-[oklch(0.9_0.05_30)]">Phoenix Protocol Knowledge Management System</div>
                </div>
                <div>
                  <div className="text-[oklch(0.6_0.05_30)] mb-1">Version</div>
                  <Badge variant="secondary" className="bg-[oklch(0.65_0.15_30)]/20 text-[oklch(0.65_0.15_30)]">
                    2.0.0
                  </Badge>
                </div>
                <div>
                  <div className="text-[oklch(0.6_0.05_30)] mb-1">Protocol</div>
                  <div className="text-[oklch(0.9_0.05_30)]">Infinite Scroll Protocol</div>
                </div>
                <div>
                  <div className="text-[oklch(0.6_0.05_30)] mb-1">Scan Window</div>
                  <div className="text-[oklch(0.9_0.05_30)]">24 hours</div>
                </div>
                <div>
                  <div className="text-[oklch(0.6_0.05_30)] mb-1">Automation Status</div>
                  <Badge variant="secondary" className="bg-[oklch(0.65_0.15_120)]/20 text-[oklch(0.65_0.15_120)]">
                    Scheduled Daily
                  </Badge>
                </div>
              </div>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
