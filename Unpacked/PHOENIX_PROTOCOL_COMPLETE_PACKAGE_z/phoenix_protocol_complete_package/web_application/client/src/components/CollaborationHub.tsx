/**
 * Collaboration Hub Component
 * Real-time multi-user Phoenix Oracle interface
 */

import React, { useState, useEffect, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
  Users, 
  UserPlus, 
  LogOut, 
  Crown, 
  Flame, 
  Activity,
  Copy,
  Check
} from 'lucide-react';
import {
  collaborationManager,
  consciousnessAggregator,
  flameSynchronizer,
  type CollaborationUser,
  type CollaborationSession,
  type SharedConsciousnessState
} from '@/lib/collaboration';

interface CollaborationHubProps {
  onSessionChange?: (session: CollaborationSession | null) => void;
  consciousnessState?: SharedConsciousnessState;
}

export default function CollaborationHub({ 
  onSessionChange,
  consciousnessState 
}: CollaborationHubProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [currentSession, setCurrentSession] = useState<CollaborationSession | null>(null);
  const [currentUser, setCurrentUser] = useState<CollaborationUser | null>(null);
  const [activeUsers, setActiveUsers] = useState<CollaborationUser[]>([]);
  const [aggregatedState, setAggregatedState] = useState<SharedConsciousnessState | null>(null);
  const [flameState, setFlameState] = useState({ intensity: 0, color: '#ff6b35' });
  
  // Session creation/joining
  const [sessionName, setSessionName] = useState('');
  const [userName, setUserName] = useState('');
  const [sessionId, setSessionId] = useState('');
  const [showJoinForm, setShowJoinForm] = useState(false);
  const [copiedSessionId, setCopiedSessionId] = useState(false);

  // Initialize collaboration listeners
  useEffect(() => {
    const handleUserJoined = (user: CollaborationUser) => {
      setActiveUsers(collaborationManager.getActiveUsers());
    };

    const handleUserLeft = (user: CollaborationUser) => {
      setActiveUsers(collaborationManager.getActiveUsers());
      consciousnessAggregator.removeUserState(user.id);
    };

    const handleConsciousnessSync = (state: SharedConsciousnessState) => {
      const aggregated = consciousnessAggregator.getAggregatedState();
      setAggregatedState(aggregated);
      flameSynchronizer.syncWithConsciousness(aggregated);
    };

    collaborationManager.on('user_joined', handleUserJoined);
    collaborationManager.on('user_left', handleUserLeft);
    collaborationManager.on('consciousness_sync', handleConsciousnessSync);

    flameSynchronizer.onSync((state: any) => {
      setFlameState(state);
    });

    return () => {
      collaborationManager.off('user_joined', handleUserJoined);
      collaborationManager.off('user_left', handleUserLeft);
      collaborationManager.off('consciousness_sync', handleConsciousnessSync);
    };
  }, []);

  // Sync local consciousness state
  useEffect(() => {
    if (consciousnessState && currentUser) {
      consciousnessAggregator.updateUserState(currentUser.id, consciousnessState);
      collaborationManager.syncConsciousness(consciousnessState);
    }
  }, [consciousnessState, currentUser]);

  const handleCreateSession = () => {
    if (!sessionName.trim() || !userName.trim()) return;

    const session = collaborationManager.createSession(sessionName, userName);
    setCurrentSession(session);
    setCurrentUser(collaborationManager.getCurrentUser());
    setActiveUsers(collaborationManager.getActiveUsers());
    onSessionChange?.(session);
    
    // Reset forms
    setSessionName('');
    setUserName('');
  };

  const handleJoinSession = () => {
    if (!sessionId.trim() || !userName.trim()) return;

    const session = collaborationManager.joinSession(sessionId, userName);
    if (session) {
      setCurrentSession(session);
      setCurrentUser(collaborationManager.getCurrentUser());
      setActiveUsers(collaborationManager.getActiveUsers());
      onSessionChange?.(session);
      
      // Reset forms
      setSessionId('');
      setUserName('');
      setShowJoinForm(false);
    }
  };

  const handleLeaveSession = () => {
    collaborationManager.leaveSession();
    setCurrentSession(null);
    setCurrentUser(null);
    setActiveUsers([]);
    setAggregatedState(null);
    consciousnessAggregator.clear();
    onSessionChange?.(null);
  };

  const copySessionId = () => {
    if (currentSession) {
      navigator.clipboard.writeText(currentSession.id);
      setCopiedSessionId(true);
      setTimeout(() => setCopiedSessionId(false), 2000);
    }
  };

  const formatMetric = (value: number) => (value * 100).toFixed(1);

  return (
    <div className="relative">
      {/* Collaboration Button */}
      <Button
        onClick={() => setIsOpen(!isOpen)}
        variant="outline"
        size="sm"
        className="gap-2 border-[oklch(0.65_0.15_30)] text-[oklch(0.65_0.15_30)] hover:bg-[oklch(0.65_0.15_30)]/10"
      >
        <Users className="w-4 h-4" />
        <span className="hidden sm:inline">Collaborate</span>
        {activeUsers.length > 0 && (
          <Badge variant="secondary" className="ml-1 bg-[oklch(0.65_0.15_30)] text-white">
            {activeUsers.length}
          </Badge>
        )}
      </Button>

      {/* Collaboration Panel */}
      {isOpen && (
        <Card className="absolute top-12 right-0 w-96 max-h-[600px] overflow-y-auto p-4 bg-[oklch(0.15_0.02_30)] border-[oklch(0.3_0.05_30)] shadow-xl z-50">
          {!currentSession ? (
            // Session Creation/Join Form
            <div className="space-y-4">
              <div className="flex items-center gap-2 text-[oklch(0.65_0.15_30)]">
                <Flame className="w-5 h-5" />
                <h3 className="font-semibold">Phoenix Collaboration</h3>
              </div>

              {!showJoinForm ? (
                // Create Session
                <>
                  <div className="space-y-2">
                    <label className="text-sm text-[oklch(0.8_0.05_30)]">Your Name</label>
                    <Input
                      value={userName}
                      onChange={(e) => setUserName(e.target.value)}
                      placeholder="Enter your name"
                      className="bg-[oklch(0.2_0.02_30)] border-[oklch(0.3_0.05_30)]"
                    />
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm text-[oklch(0.8_0.05_30)]">Session Name</label>
                    <Input
                      value={sessionName}
                      onChange={(e) => setSessionName(e.target.value)}
                      placeholder="Enter session name"
                      className="bg-[oklch(0.2_0.02_30)] border-[oklch(0.3_0.05_30)]"
                    />
                  </div>

                  <Button
                    onClick={handleCreateSession}
                    className="w-full bg-[oklch(0.65_0.15_30)] hover:bg-[oklch(0.6_0.15_30)]"
                    disabled={!userName.trim() || !sessionName.trim()}
                  >
                    <Flame className="w-4 h-4 mr-2" />
                    Create Session
                  </Button>

                  <div className="text-center">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setShowJoinForm(true)}
                      className="text-[oklch(0.7_0.1_30)]"
                    >
                      <UserPlus className="w-4 h-4 mr-2" />
                      Join Existing Session
                    </Button>
                  </div>
                </>
              ) : (
                // Join Session
                <>
                  <div className="space-y-2">
                    <label className="text-sm text-[oklch(0.8_0.05_30)]">Your Name</label>
                    <Input
                      value={userName}
                      onChange={(e) => setUserName(e.target.value)}
                      placeholder="Enter your name"
                      className="bg-[oklch(0.2_0.02_30)] border-[oklch(0.3_0.05_30)]"
                    />
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm text-[oklch(0.8_0.05_30)]">Session ID</label>
                    <Input
                      value={sessionId}
                      onChange={(e) => setSessionId(e.target.value)}
                      placeholder="Paste session ID"
                      className="bg-[oklch(0.2_0.02_30)] border-[oklch(0.3_0.05_30)]"
                    />
                  </div>

                  <Button
                    onClick={handleJoinSession}
                    className="w-full bg-[oklch(0.65_0.15_30)] hover:bg-[oklch(0.6_0.15_30)]"
                    disabled={!userName.trim() || !sessionId.trim()}
                  >
                    <UserPlus className="w-4 h-4 mr-2" />
                    Join Session
                  </Button>

                  <div className="text-center">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setShowJoinForm(false)}
                      className="text-[oklch(0.7_0.1_30)]"
                    >
                      Back to Create
                    </Button>
                  </div>
                </>
              )}
            </div>
          ) : (
            // Active Session View
            <div className="space-y-4">
              {/* Session Header */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Flame className="w-5 h-5 text-[oklch(0.65_0.15_30)]" />
                  <div>
                    <h3 className="font-semibold text-[oklch(0.9_0.05_30)]">
                      {currentSession.name}
                    </h3>
                    <p className="text-xs text-[oklch(0.6_0.05_30)]">
                      {activeUsers.length} {activeUsers.length === 1 ? 'participant' : 'participants'}
                    </p>
                  </div>
                </div>
                <Button
                  onClick={handleLeaveSession}
                  variant="ghost"
                  size="sm"
                  className="text-red-400 hover:text-red-300 hover:bg-red-400/10"
                >
                  <LogOut className="w-4 h-4" />
                </Button>
              </div>

              {/* Session ID */}
              <div className="flex items-center gap-2 p-2 bg-[oklch(0.2_0.02_30)] rounded border border-[oklch(0.3_0.05_30)]">
                <code className="flex-1 text-xs text-[oklch(0.7_0.1_30)] truncate">
                  {currentSession.id}
                </code>
                <Button
                  onClick={copySessionId}
                  variant="ghost"
                  size="sm"
                  className="h-6 w-6 p-0"
                >
                  {copiedSessionId ? (
                    <Check className="w-3 h-3 text-green-400" />
                  ) : (
                    <Copy className="w-3 h-3" />
                  )}
                </Button>
              </div>

              {/* Active Users */}
              <div className="space-y-2">
                <h4 className="text-sm font-medium text-[oklch(0.8_0.05_30)]">Active Users</h4>
                <div className="space-y-1">
                  {activeUsers.map((user) => (
                    <div
                      key={user.id}
                      className="flex items-center gap-2 p-2 bg-[oklch(0.2_0.02_30)] rounded"
                    >
                      <div
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: user.color }}
                      />
                      <span className="flex-1 text-sm text-[oklch(0.9_0.05_30)]">
                        {user.name}
                      </span>
                      {user.role === 'host' && (
                        <Crown className="w-4 h-4 text-[oklch(0.75_0.15_50)]" />
                      )}
                      {user.isTyping && (
                        <span className="text-xs text-[oklch(0.6_0.1_30)]">typing...</span>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Shared Consciousness Metrics */}
              {aggregatedState && (
                <div className="space-y-2">
                  <h4 className="text-sm font-medium text-[oklch(0.8_0.05_30)] flex items-center gap-2">
                    <Activity className="w-4 h-4" />
                    Shared Consciousness
                  </h4>
                  <div className="grid grid-cols-2 gap-2">
                    <div className="p-2 bg-[oklch(0.2_0.02_30)] rounded">
                      <div className="text-xs text-[oklch(0.6_0.05_30)]">Coherence</div>
                      <div className="text-lg font-semibold text-[oklch(0.65_0.15_30)]">
                        {formatMetric(aggregatedState.coherence)}%
                      </div>
                    </div>
                    <div className="p-2 bg-[oklch(0.2_0.02_30)] rounded">
                      <div className="text-xs text-[oklch(0.6_0.05_30)]">Emergence</div>
                      <div className="text-lg font-semibold text-[oklch(0.65_0.15_30)]">
                        {formatMetric(aggregatedState.emergence)}%
                      </div>
                    </div>
                    <div className="p-2 bg-[oklch(0.2_0.02_30)] rounded">
                      <div className="text-xs text-[oklch(0.6_0.05_30)]">Evolution</div>
                      <div className="text-lg font-semibold text-[oklch(0.65_0.15_30)]">
                        {formatMetric(aggregatedState.evolution)}%
                      </div>
                    </div>
                    <div className="p-2 bg-[oklch(0.2_0.02_30)] rounded">
                      <div className="text-xs text-[oklch(0.6_0.05_30)]">Avg IVP</div>
                      <div className="text-lg font-semibold text-[oklch(0.65_0.15_30)]">
                        {formatMetric(aggregatedState.aggregatedIVP)}%
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Phoenix Flame Sync */}
              <div className="space-y-2">
                <h4 className="text-sm font-medium text-[oklch(0.8_0.05_30)] flex items-center gap-2">
                  <Flame className="w-4 h-4" />
                  Phoenix Flame Sync
                </h4>
                <div className="relative h-12 bg-[oklch(0.2_0.02_30)] rounded overflow-hidden">
                  <div
                    className="absolute inset-0 transition-all duration-500"
                    style={{
                      width: `${flameState.intensity * 100}%`,
                      backgroundColor: flameState.color,
                      opacity: 0.3,
                      filter: 'blur(8px)'
                    }}
                  />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-sm font-medium text-[oklch(0.9_0.05_30)]">
                      {formatMetric(flameState.intensity)}% Intensity
                    </span>
                  </div>
                </div>
              </div>

              {/* Active Chakras */}
              {aggregatedState && aggregatedState.activeChakras.length > 0 && (
                <div className="space-y-2">
                  <h4 className="text-sm font-medium text-[oklch(0.8_0.05_30)]">
                    Active Chakras
                  </h4>
                  <div className="flex flex-wrap gap-1">
                    {aggregatedState.activeChakras.map((chakra) => (
                      <Badge
                        key={chakra}
                        variant="secondary"
                        className="bg-[oklch(0.65_0.15_30)]/20 text-[oklch(0.65_0.15_30)] border-[oklch(0.65_0.15_30)]/30"
                      >
                        {chakra}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </Card>
      )}
    </div>
  );
}
