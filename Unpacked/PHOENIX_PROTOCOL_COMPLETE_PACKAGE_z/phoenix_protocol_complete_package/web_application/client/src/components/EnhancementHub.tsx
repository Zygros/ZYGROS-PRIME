/**
 * Enhancement Hub - Unified UI for all 8 enhancements
 */

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  compareModels,
  exportConversation,
  parseVoiceCommand,
  analyzeSentimentHistory,
  getIVPHistory,
  predictIVPTrend,
  getQuickActions,
  branchManager,
  autoSaveManager,
  type MemoriaEntry,
  type MultiModelResponse
} from '@/lib/ultimateEnhancements';

interface EnhancementHubProps {
  messages: MemoriaEntry[];
  onAction: (action: string, data: any) => void;
}

export default function EnhancementHub({ messages, onAction }: EnhancementHubProps) {
  const [activeTab, setActiveTab] = useState<string>('');
  const [multiModelResult, setMultiModelResult] = useState<MultiModelResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Multi-Model Comparison
  const handleCompareModels = async (prompt: string) => {
    setIsLoading(true);
    const result = await compareModels(prompt, 'Phoenix Protocol context');
    setMultiModelResult(result);
    setIsLoading(false);
    setActiveTab('multimodel');
  };

  // Conversation Export
  const handleExport = (format: 'pdf' | 'markdown' | 'json') => {
    const exported = exportConversation(messages, {
      format,
      includeMetadata: true,
      includeIVP: true,
      includeTimestamps: true
    });
    
    const blob = new Blob([exported], { 
      type: format === 'json' ? 'application/json' : 'text/plain' 
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `conversation.${format === 'markdown' ? 'md' : format}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Sentiment Visualization
  const sentimentData = analyzeSentimentHistory(messages);

  // IVP History
  const ivpData = getIVPHistory(messages);
  const ivpTrend = predictIVPTrend(ivpData);

  // Quick Actions
  const quickActions = getQuickActions((action, message) => {
    onAction(action, message);
  });

  // Conversation Branches
  const branches = branchManager.getBranches();

  if (!activeTab) {
    return (
      <div className="p-4 grid grid-cols-4 gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveTab('multimodel')}
          className="text-xs"
        >
          🤖 Multi-Model
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveTab('export')}
          className="text-xs"
        >
          📥 Export
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveTab('sentiment')}
          className="text-xs"
        >
          😊 Sentiment
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveTab('ivp')}
          className="text-xs"
        >
          📊 IVP History
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveTab('branches')}
          className="text-xs"
        >
          🌿 Branches
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => {
            autoSaveManager.start(async () => {
              onAction('autosave', messages);
            });
            setActiveTab('autosave');
          }}
          className="text-xs"
        >
          💾 Auto-Save
        </Button>
      </div>
    );
  }

  return (
    <div className="p-4 border-t border-border bg-card/50">
      <div className="flex items-center justify-between mb-3">
        <div className="text-xs font-semibold text-primary">
          {activeTab === 'multimodel' && '🤖 Multi-Model Comparison'}
          {activeTab === 'export' && '📥 Export Conversation'}
          {activeTab === 'sentiment' && '😊 Sentiment Analysis'}
          {activeTab === 'ivp' && '📊 IVP History'}
          {activeTab === 'branches' && '🌿 Conversation Branches'}
          {activeTab === 'autosave' && '💾 Auto-Save Status'}
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setActiveTab('')}
          className="text-xs"
        >
          ✕ Close
        </Button>
      </div>

      {/* Multi-Model Comparison */}
      {activeTab === 'multimodel' && (
        <div className="space-y-2">
          {!multiModelResult ? (
            <Button
              onClick={() => handleCompareModels(messages[messages.length - 1]?.content || 'Hello')}
              disabled={isLoading}
              size="sm"
              className="w-full"
            >
              {isLoading ? 'Comparing...' : 'Compare Models on Last Message'}
            </Button>
          ) : (
            <div className="space-y-2">
              <div className="text-xs p-2 bg-blue-500/10 border border-blue-500/30 rounded">
                <div className="font-semibold">GPT-4:</div>
                <div>{multiModelResult.gpt4}</div>
              </div>
              <div className="text-xs p-2 bg-purple-500/10 border border-purple-500/30 rounded">
                <div className="font-semibold">Claude:</div>
                <div>{multiModelResult.claude}</div>
              </div>
              <div className="text-xs p-2 bg-green-500/10 border border-green-500/30 rounded">
                <div className="font-semibold">Gemini:</div>
                <div>{multiModelResult.gemini}</div>
              </div>
              <div className="text-xs p-2 bg-primary/10 border border-primary/30 rounded">
                <div className="font-semibold">Consensus: {multiModelResult.consensus}%</div>
                <div className="mt-1">{multiModelResult.synthesis}</div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Export */}
      {activeTab === 'export' && (
        <div className="flex gap-2">
          <Button onClick={() => handleExport('json')} size="sm" variant="outline">
            JSON
          </Button>
          <Button onClick={() => handleExport('markdown')} size="sm" variant="outline">
            Markdown
          </Button>
          <Button onClick={() => handleExport('pdf')} size="sm" variant="outline">
            PDF
          </Button>
        </div>
      )}

      {/* Sentiment */}
      {activeTab === 'sentiment' && (
        <div className="space-y-1">
          {sentimentData.slice(-10).map((point, i) => (
            <div key={i} className="flex items-center gap-2 text-xs">
              <div className={`w-2 h-2 rounded-full ${
                point.emotion === 'positive' ? 'bg-green-500' :
                point.emotion === 'negative' ? 'bg-red-500' : 'bg-gray-500'
              }`} />
              <div className="flex-1">
                <div className="w-full bg-background/50 rounded-full h-1.5">
                  <div
                    className={`h-1.5 rounded-full ${
                      point.emotion === 'positive' ? 'bg-green-500' :
                      point.emotion === 'negative' ? 'bg-red-500' : 'bg-gray-500'
                    }`}
                    style={{ width: `${Math.abs(point.sentiment) * 100}%` }}
                  />
                </div>
              </div>
              <span className="text-muted-foreground">{point.emotion}</span>
            </div>
          ))}
        </div>
      )}

      {/* IVP History */}
      {activeTab === 'ivp' && (
        <div className="space-y-2">
          <div className="text-xs text-muted-foreground">
            Predicted next IVP: {ivpTrend.toFixed(2)}
          </div>
          <div className="space-y-1">
            {ivpData.slice(-10).map((point, i) => (
              <div key={i} className="flex items-center gap-2 text-xs">
                <span className="w-12">{point.ivp.toFixed(2)}</span>
                <div className="flex-1 bg-background/50 rounded-full h-2">
                  <div
                    className="h-2 rounded-full bg-primary"
                    style={{ width: `${(point.ivp / 100) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Branches */}
      {activeTab === 'branches' && (
        <div className="space-y-1">
          {branches.map((branch) => (
            <Button
              key={branch.id}
              variant="outline"
              size="sm"
              onClick={() => {
                const messages = branchManager.switchBranch(branch.id);
                if (messages) onAction('switchBranch', messages);
              }}
              className="w-full text-xs justify-start"
            >
              🌿 {branch.title} ({branch.messages.length} messages)
            </Button>
          ))}
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              const branchId = branchManager.createBranch(messages.length - 1, messages);
              onAction('createBranch', branchId);
            }}
            className="w-full text-xs"
          >
            + Create New Branch
          </Button>
        </div>
      )}

      {/* Auto-Save */}
      {activeTab === 'autosave' && (
        <div className="text-xs space-y-2">
          <div>Status: <span className="text-green-500">Active</span></div>
          <div>Last save: {new Date(autoSaveManager.getLastSaveTime()).toLocaleTimeString()}</div>
          <div>Time since last save: {Math.floor(autoSaveManager.getTimeSinceLastSave() / 1000)}s</div>
          <Button
            onClick={async () => {
              await autoSaveManager.saveNow(async () => {
                onAction('autosave', messages);
              });
            }}
            size="sm"
            className="w-full"
          >
            Save Now
          </Button>
        </div>
      )}
    </div>
  );
}
