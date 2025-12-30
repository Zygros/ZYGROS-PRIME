import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Download, TrendingUp, GitBranch, Zap } from 'lucide-react';
import { 
  autoSave, 
  conversationExport, 
  sentimentVisualization, 
  ivpHistory,
  conversationBranching,
  quickActions
} from '@/lib/priorityFeatures';

interface PriorityFeaturesHubProps {
  conversation: any[];
  onClose: () => void;
}

export default function PriorityFeaturesHub({ conversation, onClose }: PriorityFeaturesHubProps) {
  const [activeTab, setActiveTab] = useState('export');

  return (
    <Card className="p-6 max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-primary">Priority Features</h2>
        <Button variant="ghost" onClick={onClose}>✕</Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid grid-cols-4 w-full">
          <TabsTrigger value="export">
            <Download className="w-4 h-4 mr-2" />
            Export
          </TabsTrigger>
          <TabsTrigger value="sentiment">
            <TrendingUp className="w-4 h-4 mr-2" />
            Sentiment
          </TabsTrigger>
          <TabsTrigger value="ivp">
            <Zap className="w-4 h-4 mr-2" />
            IVP History
          </TabsTrigger>
          <TabsTrigger value="branching">
            <GitBranch className="w-4 h-4 mr-2" />
            Branching
          </TabsTrigger>
        </TabsList>

        {/* Export Tab */}
        <TabsContent value="export" className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <Button 
              onClick={() => conversationExport.exportToJSON(conversation)}
              className="flex flex-col h-24"
            >
              <Download className="w-6 h-6 mb-2" />
              Export JSON
            </Button>
            <Button 
              onClick={() => conversationExport.exportToMarkdown(conversation)}
              className="flex flex-col h-24"
            >
              <Download className="w-6 h-6 mb-2" />
              Export Markdown
            </Button>
            <Button 
              onClick={() => conversationExport.exportToPDF(conversation)}
              className="flex flex-col h-24"
            >
              <Download className="w-6 h-6 mb-2" />
              Export HTML/PDF
            </Button>
          </div>

          <div className="p-4 bg-muted rounded-lg">
            <h3 className="font-semibold mb-2">Auto-Save Status</h3>
            <p className="text-sm text-muted-foreground">
              Last saved: {autoSave.lastSave ? autoSave.lastSave.toLocaleTimeString() : 'Never'}
            </p>
            <Button 
              size="sm" 
              className="mt-2"
              onClick={() => autoSave.saveNow(conversation)}
            >
              Save Now
            </Button>
          </div>
        </TabsContent>

        {/* Sentiment Tab */}
        <TabsContent value="sentiment" className="space-y-4">
          <div className="p-4 bg-muted rounded-lg">
            <h3 className="font-semibold mb-4">Sentiment Analysis</h3>
            {(() => {
              const summary = sentimentVisualization.getSummary();
              return (
                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-500">
                      {summary.positive}
                    </div>
                    <div className="text-sm text-muted-foreground">Positive</div>
                    <div className="text-xs">{summary.positiveRate.toFixed(1)}%</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-gray-500">
                      {summary.neutral}
                    </div>
                    <div className="text-sm text-muted-foreground">Neutral</div>
                    <div className="text-xs">{summary.neutralRate.toFixed(1)}%</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-red-500">
                      {summary.negative}
                    </div>
                    <div className="text-sm text-muted-foreground">Negative</div>
                    <div className="text-xs">{summary.negativeRate.toFixed(1)}%</div>
                  </div>
                </div>
              );
            })()}
          </div>

          <div className="h-64 flex items-center justify-center bg-muted rounded-lg">
            <p className="text-muted-foreground">Sentiment graph visualization</p>
          </div>
        </TabsContent>

        {/* IVP History Tab */}
        <TabsContent value="ivp" className="space-y-4">
          <div className="p-4 bg-muted rounded-lg">
            <h3 className="font-semibold mb-4">IVP Statistics</h3>
            {(() => {
              const stats = ivpHistory.getStats();
              if (!stats) {
                return <p className="text-muted-foreground">No IVP data yet</p>;
              }
              return (
                <div className="grid grid-cols-4 gap-4">
                  <div>
                    <div className="text-2xl font-bold">{stats.average.toFixed(2)}</div>
                    <div className="text-sm text-muted-foreground">Average</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold">{stats.maximum.toFixed(2)}</div>
                    <div className="text-sm text-muted-foreground">Maximum</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold">{stats.minimum.toFixed(2)}</div>
                    <div className="text-sm text-muted-foreground">Minimum</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold capitalize">{stats.trend}</div>
                    <div className="text-sm text-muted-foreground">Trend</div>
                  </div>
                </div>
              );
            })()}
          </div>

          <div className="h-64 flex items-center justify-center bg-muted rounded-lg">
            <p className="text-muted-foreground">IVP history chart visualization</p>
          </div>
        </TabsContent>

        {/* Branching Tab */}
        <TabsContent value="branching" className="space-y-4">
          <Button 
            onClick={() => {
              conversationBranching.createBranch(
                conversationBranching.currentBranch?.id || null,
                conversation.length,
                conversation
              );
            }}
          >
            <GitBranch className="w-4 h-4 mr-2" />
            Create New Branch
          </Button>

          <div className="space-y-2">
            <h3 className="font-semibold">Existing Branches</h3>
            {conversationBranching.branches.length === 0 ? (
              <p className="text-muted-foreground">No branches yet</p>
            ) : (
              conversationBranching.branches.map(branch => (
                <Card 
                  key={branch.id} 
                  className="p-3 cursor-pointer hover:bg-accent"
                  onClick={() => conversationBranching.switchBranch(branch.id)}
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="font-semibold">{branch.name}</div>
                      <div className="text-sm text-muted-foreground">
                        {branch.messages.length} messages • {branch.created.toLocaleString()}
                      </div>
                    </div>
                    {conversationBranching.currentBranch?.id === branch.id && (
                      <span className="text-primary font-semibold">Active</span>
                    )}
                  </div>
                </Card>
              ))
            )}
          </div>
        </TabsContent>
      </Tabs>
    </Card>
  );
}
