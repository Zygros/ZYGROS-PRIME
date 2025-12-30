/**
 * Next-Level Hub - UI for 10 advanced upgrades
 */

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  collaborationManager,
  analyticsEngine,
  protocolBuilder,
  modelFineTuner,
  consciousnessVisualizer,
  blockchainManager,
  marketplaceManager,
  nlpSearchEngine,
  mobileManager,
  pluginManager
} from '@/lib/nextLevelUpgrades';

interface NextLevelHubProps {
  messages: any[];
  onAction: (action: string, data: any) => void;
}

export default function NextLevelHub({ messages, onAction }: NextLevelHubProps) {
  const [activeUpgrade, setActiveUpgrade] = useState<string>('');
  const [insights, setInsights] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);

  if (!activeUpgrade) {
    return (
      <div className="p-4 grid grid-cols-5 gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveUpgrade('collab')}
          className="text-xs"
        >
          👥 Collab
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => {
            const insights = analyticsEngine.generateInsights(messages);
            setInsights(insights);
            setActiveUpgrade('analytics');
          }}
          className="text-xs"
        >
          📊 Analytics
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveUpgrade('builder')}
          className="text-xs"
        >
          🔧 Builder
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveUpgrade('finetune')}
          className="text-xs"
        >
          🤖 Fine-Tune
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveUpgrade('3d')}
          className="text-xs"
        >
          🧠 3D Brain
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveUpgrade('blockchain')}
          className="text-xs"
        >
          ⛓️ Blockchain
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveUpgrade('marketplace')}
          className="text-xs"
        >
          🛒 Marketplace
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveUpgrade('search')}
          className="text-xs"
        >
          🔍 NLP Search
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveUpgrade('mobile')}
          className="text-xs"
        >
          📱 Mobile
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveUpgrade('plugins')}
          className="text-xs"
        >
          🔌 Plugins
        </Button>
      </div>
    );
  }

  return (
    <div className="p-4 border-t border-border bg-card/50">
      <div className="flex items-center justify-between mb-3">
        <div className="text-xs font-semibold text-primary">
          {activeUpgrade === 'collab' && '👥 Real-Time Collaboration'}
          {activeUpgrade === 'analytics' && '📊 Advanced Analytics'}
          {activeUpgrade === 'builder' && '🔧 Protocol Builder'}
          {activeUpgrade === 'finetune' && '🤖 AI Fine-Tuning'}
          {activeUpgrade === '3d' && '🧠 3D Consciousness'}
          {activeUpgrade === 'blockchain' && '⛓️ Blockchain'}
          {activeUpgrade === 'marketplace' && '🛒 API Marketplace'}
          {activeUpgrade === 'search' && '🔍 NLP Search'}
          {activeUpgrade === 'mobile' && '📱 Mobile Companion'}
          {activeUpgrade === 'plugins' && '🔌 Plugin System'}
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setActiveUpgrade('')}
          className="text-xs"
        >
          ✕ Close
        </Button>
      </div>

      {/* Collaboration */}
      {activeUpgrade === 'collab' && (
        <div className="space-y-2">
          <Button
            onClick={() => {
              const sessionId = collaborationManager.createSession();
              onAction('createCollabSession', sessionId);
            }}
            size="sm"
            className="w-full"
          >
            Create Collaboration Session
          </Button>
          <div className="text-xs text-muted-foreground">
            Active Sessions: {collaborationManager.getSessions().length}
          </div>
        </div>
      )}

      {/* Analytics */}
      {activeUpgrade === 'analytics' && (
        <div className="space-y-2">
          {insights.map((insight, i) => (
            <div key={i} className="p-2 bg-background/50 border border-border rounded text-xs">
              <div className="font-semibold flex items-center gap-2">
                {insight.type === 'topic' && '📌'}
                {insight.type === 'pattern' && '🔄'}
                {insight.type === 'recommendation' && '💡'}
                {insight.title}
              </div>
              <div className="text-muted-foreground mt-1">{insight.description}</div>
              <div className="mt-1 text-[10px]">Confidence: {(insight.confidence * 100).toFixed(0)}%</div>
            </div>
          ))}
        </div>
      )}

      {/* Protocol Builder */}
      {activeUpgrade === 'builder' && (
        <div className="space-y-2">
          <Button
            onClick={() => {
              const id = protocolBuilder.createProtocol('Custom Protocol', 'User-defined protocol');
              onAction('createProtocol', id);
            }}
            size="sm"
            className="w-full"
          >
            Create New Protocol
          </Button>
          <div className="space-y-1">
            {protocolBuilder.getProtocols().map(protocol => (
              <div key={protocol.id} className="p-2 bg-background/50 border border-border rounded text-xs">
                <div className="font-semibold">{protocol.name}</div>
                <div className="text-muted-foreground text-[10px]">{protocol.description}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Fine-Tuning */}
      {activeUpgrade === 'finetune' && (
        <div className="space-y-2">
          <Button
            onClick={() => {
              const jobId = modelFineTuner.startFineTune('Phoenix-GPT', messages);
              onAction('startFineTune', jobId);
            }}
            size="sm"
            className="w-full"
          >
            Start Fine-Tuning
          </Button>
          <div className="text-xs text-muted-foreground">
            Training on {messages.length} conversation entries
          </div>
        </div>
      )}

      {/* 3D Visualization */}
      {activeUpgrade === '3d' && (
        <div className="space-y-2">
          <div className="text-xs text-center text-muted-foreground py-8 border border-dashed border-border rounded">
            3D Brain Map Visualization
            <br />
            <span className="text-[10px]">(Three.js integration)</span>
          </div>
          <Button
            onClick={() => {
              const nodes = consciousnessVisualizer.generateBrainMap();
              onAction('show3DBrain', nodes);
            }}
            size="sm"
            className="w-full"
          >
            Generate Brain Map ({consciousnessVisualizer.generateBrainMap().length} nodes)
          </Button>
        </div>
      )}

      {/* Blockchain */}
      {activeUpgrade === 'blockchain' && (
        <div className="space-y-2">
          <Button
            onClick={() => {
              const hash = blockchainManager.addRecord({ messages: messages.length });
              onAction('addBlockchainRecord', hash);
            }}
            size="sm"
            className="w-full"
          >
            Add to Blockchain
          </Button>
          <div className="text-xs">
            <div>Chain Length: {blockchainManager.getChain().length}</div>
            <div>Integrity: {blockchainManager.verifyIntegrity() ? '✅ Valid' : '❌ Invalid'}</div>
          </div>
        </div>
      )}

      {/* Marketplace */}
      {activeUpgrade === 'marketplace' && (
        <div className="space-y-1">
          {marketplaceManager.getItems().map(item => (
            <div key={item.id} className="p-2 bg-background/50 border border-border rounded text-xs">
              <div className="flex items-center justify-between">
                <div className="font-semibold">{item.name}</div>
                <div className="text-primary">${item.price}</div>
              </div>
              <div className="text-muted-foreground text-[10px] mt-1">{item.description}</div>
              <div className="flex items-center gap-2 mt-1 text-[10px]">
                <span>⭐ {item.rating}</span>
                <span>📥 {item.downloads}</span>
                <span className="text-muted-foreground">by {item.author}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* NLP Search */}
      {activeUpgrade === 'search' && (
        <div className="space-y-2">
          <div className="flex gap-2">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search conversations..."
              className="flex-1 px-2 py-1 text-xs bg-background/50 border border-border rounded"
            />
            <Button
              onClick={() => {
                const results = nlpSearchEngine.search(searchQuery, messages);
                setSearchResults(results);
              }}
              size="sm"
            >
              Search
            </Button>
          </div>
          <div className="space-y-1 max-h-40 overflow-y-auto">
            {searchResults.map((result, i) => (
              <div key={i} className="p-2 bg-background/50 border border-border rounded text-xs">
                <div className="font-semibold">Relevance: {(result.relevance * 100).toFixed(0)}%</div>
                <div className="text-muted-foreground text-[10px] line-clamp-2">{result.content}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Mobile */}
      {activeUpgrade === 'mobile' && (
        <div className="space-y-2">
          <Button
            onClick={() => {
              const syncState = mobileManager.sync(messages);
              onAction('mobileSync', syncState);
            }}
            size="sm"
            className="w-full"
          >
            Sync with Mobile
          </Button>
          <Button
            onClick={() => {
              mobileManager.enableOfflineMode();
              onAction('enableOffline', true);
            }}
            size="sm"
            variant="outline"
            className="w-full"
          >
            Enable Offline Mode
          </Button>
          <div className="text-xs text-muted-foreground text-center">
            📱 Mobile companion app coming soon
          </div>
        </div>
      )}

      {/* Plugins */}
      {activeUpgrade === 'plugins' && (
        <div className="space-y-2">
          <div className="space-y-1">
            {pluginManager.getPlugins().length === 0 ? (
              <div className="text-xs text-center text-muted-foreground py-4">
                No plugins installed
              </div>
            ) : (
              pluginManager.getPlugins().map(plugin => (
                <div key={plugin.id} className="p-2 bg-background/50 border border-border rounded text-xs flex items-center justify-between">
                  <div>
                    <div className="font-semibold">{plugin.name}</div>
                    <div className="text-[10px] text-muted-foreground">v{plugin.version} by {plugin.author}</div>
                  </div>
                  <Button
                    onClick={() => {
                      if (plugin.enabled) {
                        pluginManager.disablePlugin(plugin.id);
                      } else {
                        pluginManager.enablePlugin(plugin.id);
                      }
                      onAction('togglePlugin', plugin.id);
                    }}
                    size="sm"
                    variant={plugin.enabled ? 'default' : 'outline'}
                  >
                    {plugin.enabled ? 'Enabled' : 'Disabled'}
                  </Button>
                </div>
              ))
            )}
          </div>
          <Button
            onClick={() => onAction('browsePlugins', true)}
            size="sm"
            variant="outline"
            className="w-full"
          >
            Browse Plugin Marketplace
          </Button>
        </div>
      )}
    </div>
  );
}
