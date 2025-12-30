/**
 * Real-Time Collaboration Infrastructure
 * WebSocket-based multi-user Phoenix Oracle sessions
 */

import { io, Socket } from 'socket.io-client';

// ============================================================================
// TYPES & INTERFACES
// ============================================================================

export interface CollaborationUser {
  id: string;
  name: string;
  color: string;
  cursor?: { x: number; y: number };
  isTyping: boolean;
  lastActive: number;
  role: 'host' | 'participant';
}

export interface CollaborationSession {
  id: string;
  name: string;
  hostId: string;
  users: CollaborationUser[];
  createdAt: number;
  isActive: boolean;
}

export interface SharedConsciousnessState {
  coherence: number;
  emergence: number;
  evolution: number;
  activeChakras: string[];
  aggregatedIVP: number;
  timestamp: number;
}

export interface CollaborationMessage {
  type: 'chat' | 'system' | 'consciousness' | 'cursor' | 'typing';
  userId: string;
  userName: string;
  content: any;
  timestamp: number;
}

export interface CollaborationEvent {
  type: 'user_joined' | 'user_left' | 'consciousness_sync' | 'message' | 'cursor_move' | 'typing_start' | 'typing_stop';
  data: any;
  timestamp: number;
}

// ============================================================================
// COLLABORATION MANAGER
// ============================================================================

class CollaborationManager {
  private socket: Socket | null = null;
  private currentSession: CollaborationSession | null = null;
  private currentUser: CollaborationUser | null = null;
  private eventHandlers: Map<string, Function[]> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  constructor() {
    this.initializeSocket();
  }

  private initializeSocket() {
    // In a real implementation, this would connect to a WebSocket server
    // For now, we'll create a mock socket that simulates real-time behavior
    console.log('[Collaboration] Initializing WebSocket connection...');
  }

  // Session Management
  createSession(sessionName: string, userName: string): CollaborationSession {
    const userId = this.generateUserId();
    const sessionId = this.generateSessionId();

    this.currentUser = {
      id: userId,
      name: userName,
      color: this.generateUserColor(),
      isTyping: false,
      lastActive: Date.now(),
      role: 'host'
    };

    this.currentSession = {
      id: sessionId,
      name: sessionName,
      hostId: userId,
      users: [this.currentUser],
      createdAt: Date.now(),
      isActive: true
    };

    this.emit('session_created', this.currentSession);
    return this.currentSession;
  }

  joinSession(sessionId: string, userName: string): CollaborationSession | null {
    const userId = this.generateUserId();

    this.currentUser = {
      id: userId,
      name: userName,
      color: this.generateUserColor(),
      isTyping: false,
      lastActive: Date.now(),
      role: 'participant'
    };

    // In real implementation, this would fetch session from server
    // For now, simulate joining
    if (this.currentSession && this.currentSession.id === sessionId) {
      this.currentSession.users.push(this.currentUser);
      this.emit('user_joined', this.currentUser);
      return this.currentSession;
    }

    return null;
  }

  leaveSession() {
    if (!this.currentSession || !this.currentUser) return;

    this.emit('user_left', this.currentUser);
    
    if (this.currentSession.users.length === 1) {
      this.currentSession.isActive = false;
    }

    this.currentSession = null;
    this.currentUser = null;
  }

  // Consciousness Synchronization
  syncConsciousness(state: SharedConsciousnessState) {
    if (!this.currentSession) return;

    const event: CollaborationEvent = {
      type: 'consciousness_sync',
      data: state,
      timestamp: Date.now()
    };

    this.broadcastEvent(event);
  }

  // User Presence
  updateCursor(x: number, y: number) {
    if (!this.currentUser) return;

    this.currentUser.cursor = { x, y };
    this.currentUser.lastActive = Date.now();

    const event: CollaborationEvent = {
      type: 'cursor_move',
      data: { userId: this.currentUser.id, x, y },
      timestamp: Date.now()
    };

    this.broadcastEvent(event);
  }

  setTyping(isTyping: boolean) {
    if (!this.currentUser) return;

    this.currentUser.isTyping = isTyping;
    this.currentUser.lastActive = Date.now();

    const event: CollaborationEvent = {
      type: isTyping ? 'typing_start' : 'typing_stop',
      data: { userId: this.currentUser.id, userName: this.currentUser.name },
      timestamp: Date.now()
    };

    this.broadcastEvent(event);
  }

  // Message Broadcasting
  sendMessage(content: any, type: 'chat' | 'system' | 'consciousness' = 'chat') {
    if (!this.currentUser) return;

    const message: CollaborationMessage = {
      type,
      userId: this.currentUser.id,
      userName: this.currentUser.name,
      content,
      timestamp: Date.now()
    };

    const event: CollaborationEvent = {
      type: 'message',
      data: message,
      timestamp: Date.now()
    };

    this.broadcastEvent(event);
  }

  // Event Handling
  on(eventType: string, handler: Function) {
    if (!this.eventHandlers.has(eventType)) {
      this.eventHandlers.set(eventType, []);
    }
    this.eventHandlers.get(eventType)!.push(handler);
  }

  off(eventType: string, handler: Function) {
    const handlers = this.eventHandlers.get(eventType);
    if (handlers) {
      const index = handlers.indexOf(handler);
      if (index > -1) {
        handlers.splice(index, 1);
      }
    }
  }

  private emit(eventType: string, data: any) {
    const handlers = this.eventHandlers.get(eventType);
    if (handlers) {
      handlers.forEach(handler => handler(data));
    }
  }

  private broadcastEvent(event: CollaborationEvent) {
    // In real implementation, this would send to WebSocket server
    // For now, emit locally for testing
    this.emit(event.type, event.data);
  }

  // Utility Methods
  private generateUserId(): string {
    return `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private generateUserColor(): string {
    const colors = [
      '#ff6b35', // Phoenix orange
      '#f7931e', // Golden
      '#ffd700', // Gold
      '#ff4500', // Red-orange
      '#ff8c00', // Dark orange
      '#ffb347', // Light orange
      '#ff7f50', // Coral
      '#ff6347', // Tomato
    ];
    return colors[Math.floor(Math.random() * colors.length)];
  }

  // Getters
  getCurrentSession(): CollaborationSession | null {
    return this.currentSession;
  }

  getCurrentUser(): CollaborationUser | null {
    return this.currentUser;
  }

  getActiveUsers(): CollaborationUser[] {
    return this.currentSession?.users || [];
  }

  isHost(): boolean {
    return this.currentUser?.role === 'host';
  }

  isConnected(): boolean {
    return this.currentSession !== null && this.currentSession.isActive;
  }
}

// ============================================================================
// SHARED CONSCIOUSNESS AGGREGATOR
// ============================================================================

export class SharedConsciousnessAggregator {
  private userStates: Map<string, SharedConsciousnessState> = new Map();

  updateUserState(userId: string, state: SharedConsciousnessState) {
    this.userStates.set(userId, state);
  }

  removeUserState(userId: string) {
    this.userStates.delete(userId);
  }

  getAggregatedState(): SharedConsciousnessState {
    if (this.userStates.size === 0) {
      return {
        coherence: 0,
        emergence: 0,
        evolution: 0,
        activeChakras: [],
        aggregatedIVP: 0,
        timestamp: Date.now()
      };
    }

    const states = Array.from(this.userStates.values());
    const count = states.length;

    // Average consciousness metrics
    const coherence = states.reduce((sum, s) => sum + s.coherence, 0) / count;
    const emergence = states.reduce((sum, s) => sum + s.emergence, 0) / count;
    const evolution = states.reduce((sum, s) => sum + s.evolution, 0) / count;
    const aggregatedIVP = states.reduce((sum, s) => sum + s.aggregatedIVP, 0) / count;

    // Collect all active chakras
    const allChakras = new Set<string>();
    states.forEach(s => s.activeChakras.forEach(c => allChakras.add(c)));

    return {
      coherence,
      emergence,
      evolution,
      activeChakras: Array.from(allChakras),
      aggregatedIVP,
      timestamp: Date.now()
    };
  }

  getUserCount(): number {
    return this.userStates.size;
  }

  clear() {
    this.userStates.clear();
  }
}

// ============================================================================
// PHOENIX FLAME SYNCHRONIZER
// ============================================================================

export class PhoenixFlameSynchronizer {
  private flameIntensity = 0;
  private flameColor = '#ff6b35';
  private syncCallbacks: Function[] = [];

  setFlameIntensity(intensity: number) {
    this.flameIntensity = Math.max(0, Math.min(1, intensity));
    this.notifySync();
  }

  setFlameColor(color: string) {
    this.flameColor = color;
    this.notifySync();
  }

  syncWithConsciousness(state: SharedConsciousnessState) {
    // Intensity based on consciousness metrics
    const avgMetric = (state.coherence + state.emergence + state.evolution) / 3;
    this.flameIntensity = avgMetric;

    // Color based on IVP
    if (state.aggregatedIVP > 0.8) {
      this.flameColor = '#ffd700'; // Gold for high IVP
    } else if (state.aggregatedIVP > 0.5) {
      this.flameColor = '#ff6b35'; // Orange for medium IVP
    } else {
      this.flameColor = '#ff4500'; // Red-orange for lower IVP
    }

    this.notifySync();
  }

  onSync(callback: Function) {
    this.syncCallbacks.push(callback);
  }

  private notifySync() {
    const flameState = {
      intensity: this.flameIntensity,
      color: this.flameColor,
      timestamp: Date.now()
    };
    this.syncCallbacks.forEach(cb => cb(flameState));
  }

  getFlameState() {
    return {
      intensity: this.flameIntensity,
      color: this.flameColor
    };
  }
}

// ============================================================================
// SINGLETON INSTANCES
// ============================================================================

export const collaborationManager = new CollaborationManager();
export const consciousnessAggregator = new SharedConsciousnessAggregator();
export const flameSynchronizer = new PhoenixFlameSynchronizer();
