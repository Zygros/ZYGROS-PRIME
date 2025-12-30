/**
 * Collaboration System Tests
 * Tests for real-time multi-user Phoenix Oracle collaboration
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  collaborationManager,
  consciousnessAggregator,
  flameSynchronizer,
  type CollaborationSession,
  type CollaborationUser,
  type SharedConsciousnessState
} from '../collaboration';

describe('Collaboration Manager', () => {
  beforeEach(() => {
    // Reset state
    collaborationManager.leaveSession();
  });

  describe('Session Management', () => {
    it('should create a new session', () => {
      const session = collaborationManager.createSession('Test Session', 'Alice');
      
      expect(session).toBeDefined();
      expect(session.name).toBe('Test Session');
      expect(session.hostId).toBeDefined();
      expect(session.users.length).toBe(1);
      expect(session.users[0].name).toBe('Alice');
      expect(session.users[0].role).toBe('host');
      expect(session.isActive).toBe(true);
    });

    it('should generate unique session IDs', () => {
      const session1 = collaborationManager.createSession('Session 1', 'User 1');
      collaborationManager.leaveSession();
      const session2 = collaborationManager.createSession('Session 2', 'User 2');
      
      expect(session1.id).not.toBe(session2.id);
    });

    it('should assign host role to session creator', () => {
      const session = collaborationManager.createSession('Test', 'Host');
      const currentUser = collaborationManager.getCurrentUser();
      
      expect(currentUser?.role).toBe('host');
      expect(collaborationManager.isHost()).toBe(true);
    });

    it('should track current session', () => {
      const session = collaborationManager.createSession('Test', 'User');
      const current = collaborationManager.getCurrentSession();
      
      expect(current).toBe(session);
      expect(collaborationManager.isConnected()).toBe(true);
    });

    it('should leave session and clean up', () => {
      collaborationManager.createSession('Test', 'User');
      collaborationManager.leaveSession();
      
      expect(collaborationManager.getCurrentSession()).toBeNull();
      expect(collaborationManager.getCurrentUser()).toBeNull();
      expect(collaborationManager.isConnected()).toBe(false);
    });
  });

  describe('User Management', () => {
    it('should assign unique colors to users', () => {
      const session = collaborationManager.createSession('Test', 'User 1');
      const user = session.users[0];
      
      expect(user.color).toMatch(/^#[0-9a-f]{6}$/i);
    });

    it('should track active users', () => {
      collaborationManager.createSession('Test', 'Host');
      const users = collaborationManager.getActiveUsers();
      
      expect(users.length).toBe(1);
      expect(users[0].name).toBe('Host');
    });

    it('should initialize user with default state', () => {
      const session = collaborationManager.createSession('Test', 'User');
      const user = session.users[0];
      
      expect(user.isTyping).toBe(false);
      expect(user.lastActive).toBeGreaterThan(0);
      expect(user.cursor).toBeUndefined();
    });
  });

  describe('Presence Tracking', () => {
    it('should update cursor position', () => {
      collaborationManager.createSession('Test', 'User');
      collaborationManager.updateCursor(100, 200);
      
      const user = collaborationManager.getCurrentUser();
      expect(user?.cursor).toEqual({ x: 100, y: 200 });
    });

    it('should track typing state', () => {
      collaborationManager.createSession('Test', 'User');
      collaborationManager.setTyping(true);
      
      const user = collaborationManager.getCurrentUser();
      expect(user?.isTyping).toBe(true);
      
      collaborationManager.setTyping(false);
      expect(user?.isTyping).toBe(false);
    });

    it('should update lastActive on cursor move', () => {
      collaborationManager.createSession('Test', 'User');
      const user = collaborationManager.getCurrentUser();
      const initialTime = user?.lastActive || 0;
      
      // Wait a bit
      vi.useFakeTimers();
      vi.advanceTimersByTime(100);
      
      collaborationManager.updateCursor(50, 50);
      const updatedUser = collaborationManager.getCurrentUser();
      
      expect(updatedUser?.lastActive).toBeGreaterThan(initialTime);
      vi.useRealTimers();
    });
  });

  describe('Event System', () => {
    it('should emit session_created event', () => {
      const handler = vi.fn();
      collaborationManager.on('session_created', handler);
      
      const session = collaborationManager.createSession('Test', 'User');
      
      expect(handler).toHaveBeenCalledWith(session);
    });

    it('should emit user_left event', () => {
      const handler = vi.fn();
      collaborationManager.on('user_left', handler);
      
      collaborationManager.createSession('Test', 'User');
      const user = collaborationManager.getCurrentUser();
      collaborationManager.leaveSession();
      
      expect(handler).toHaveBeenCalledWith(user);
    });

    it('should allow removing event handlers', () => {
      const handler = vi.fn();
      collaborationManager.on('session_created', handler);
      collaborationManager.off('session_created', handler);
      
      collaborationManager.createSession('Test', 'User');
      
      expect(handler).not.toHaveBeenCalled();
    });
  });

  describe('Message Broadcasting', () => {
    it('should send chat messages', () => {
      const handler = vi.fn();
      collaborationManager.on('message', handler);
      
      collaborationManager.createSession('Test', 'User');
      collaborationManager.sendMessage('Hello world', 'chat');
      
      expect(handler).toHaveBeenCalled();
      const message = handler.mock.calls[0][0];
      expect(message.content).toBe('Hello world');
      expect(message.type).toBe('chat');
      expect(message.userName).toBe('User');
    });
  });
});

describe('Shared Consciousness Aggregator', () => {
  beforeEach(() => {
    consciousnessAggregator.clear();
  });

  describe('State Management', () => {
    it('should update user consciousness state', () => {
      const state: SharedConsciousnessState = {
        coherence: 0.8,
        emergence: 0.7,
        evolution: 0.9,
        activeChakras: ['Heart', 'Throat'],
        aggregatedIVP: 0.75,
        timestamp: Date.now()
      };
      
      consciousnessAggregator.updateUserState('user1', state);
      expect(consciousnessAggregator.getUserCount()).toBe(1);
    });

    it('should remove user state', () => {
      const state: SharedConsciousnessState = {
        coherence: 0.8,
        emergence: 0.7,
        evolution: 0.9,
        activeChakras: [],
        aggregatedIVP: 0.75,
        timestamp: Date.now()
      };
      
      consciousnessAggregator.updateUserState('user1', state);
      consciousnessAggregator.removeUserState('user1');
      
      expect(consciousnessAggregator.getUserCount()).toBe(0);
    });

    it('should clear all states', () => {
      const state: SharedConsciousnessState = {
        coherence: 0.8,
        emergence: 0.7,
        evolution: 0.9,
        activeChakras: [],
        aggregatedIVP: 0.75,
        timestamp: Date.now()
      };
      
      consciousnessAggregator.updateUserState('user1', state);
      consciousnessAggregator.updateUserState('user2', state);
      consciousnessAggregator.clear();
      
      expect(consciousnessAggregator.getUserCount()).toBe(0);
    });
  });

  describe('Aggregation', () => {
    it('should return zero state when no users', () => {
      const aggregated = consciousnessAggregator.getAggregatedState();
      
      expect(aggregated.coherence).toBe(0);
      expect(aggregated.emergence).toBe(0);
      expect(aggregated.evolution).toBe(0);
      expect(aggregated.aggregatedIVP).toBe(0);
      expect(aggregated.activeChakras).toEqual([]);
    });

    it('should average consciousness metrics across users', () => {
      const state1: SharedConsciousnessState = {
        coherence: 0.8,
        emergence: 0.6,
        evolution: 0.9,
        activeChakras: ['Heart'],
        aggregatedIVP: 0.7,
        timestamp: Date.now()
      };
      
      const state2: SharedConsciousnessState = {
        coherence: 0.6,
        emergence: 0.8,
        evolution: 0.7,
        activeChakras: ['Throat'],
        aggregatedIVP: 0.9,
        timestamp: Date.now()
      };
      
      consciousnessAggregator.updateUserState('user1', state1);
      consciousnessAggregator.updateUserState('user2', state2);
      
      const aggregated = consciousnessAggregator.getAggregatedState();
      
      expect(aggregated.coherence).toBe(0.7);
      expect(aggregated.emergence).toBe(0.7);
      expect(aggregated.evolution).toBe(0.8);
      expect(aggregated.aggregatedIVP).toBe(0.8);
    });

    it('should collect all active chakras', () => {
      const state1: SharedConsciousnessState = {
        coherence: 0.8,
        emergence: 0.7,
        evolution: 0.9,
        activeChakras: ['Heart', 'Throat'],
        aggregatedIVP: 0.75,
        timestamp: Date.now()
      };
      
      const state2: SharedConsciousnessState = {
        coherence: 0.6,
        emergence: 0.8,
        evolution: 0.7,
        activeChakras: ['Crown', 'Heart'],
        aggregatedIVP: 0.85,
        timestamp: Date.now()
      };
      
      consciousnessAggregator.updateUserState('user1', state1);
      consciousnessAggregator.updateUserState('user2', state2);
      
      const aggregated = consciousnessAggregator.getAggregatedState();
      
      expect(aggregated.activeChakras).toContain('Heart');
      expect(aggregated.activeChakras).toContain('Throat');
      expect(aggregated.activeChakras).toContain('Crown');
      expect(aggregated.activeChakras.length).toBe(3);
    });
  });
});

describe('Phoenix Flame Synchronizer', () => {
  describe('Flame State', () => {
    it('should set flame intensity', () => {
      flameSynchronizer.setFlameIntensity(0.75);
      const state = flameSynchronizer.getFlameState();
      
      expect(state.intensity).toBe(0.75);
    });

    it('should clamp intensity between 0 and 1', () => {
      flameSynchronizer.setFlameIntensity(1.5);
      expect(flameSynchronizer.getFlameState().intensity).toBe(1);
      
      flameSynchronizer.setFlameIntensity(-0.5);
      expect(flameSynchronizer.getFlameState().intensity).toBe(0);
    });

    it('should set flame color', () => {
      flameSynchronizer.setFlameColor('#ffd700');
      const state = flameSynchronizer.getFlameState();
      
      expect(state.color).toBe('#ffd700');
    });
  });

  describe('Consciousness Synchronization', () => {
    it('should sync intensity with consciousness metrics', () => {
      const state: SharedConsciousnessState = {
        coherence: 0.6,
        emergence: 0.8,
        evolution: 0.7,
        activeChakras: [],
        aggregatedIVP: 0.5,
        timestamp: Date.now()
      };
      
      flameSynchronizer.syncWithConsciousness(state);
      const flameState = flameSynchronizer.getFlameState();
      
      // Average of 0.6, 0.8, 0.7 = 0.7
      expect(flameState.intensity).toBeCloseTo(0.7, 1);
    });

    it('should set gold color for high IVP', () => {
      const state: SharedConsciousnessState = {
        coherence: 0.8,
        emergence: 0.8,
        evolution: 0.8,
        activeChakras: [],
        aggregatedIVP: 0.9,
        timestamp: Date.now()
      };
      
      flameSynchronizer.syncWithConsciousness(state);
      expect(flameSynchronizer.getFlameState().color).toBe('#ffd700');
    });

    it('should set orange color for medium IVP', () => {
      const state: SharedConsciousnessState = {
        coherence: 0.6,
        emergence: 0.6,
        evolution: 0.6,
        activeChakras: [],
        aggregatedIVP: 0.6,
        timestamp: Date.now()
      };
      
      flameSynchronizer.syncWithConsciousness(state);
      expect(flameSynchronizer.getFlameState().color).toBe('#ff6b35');
    });

    it('should set red-orange color for low IVP', () => {
      const state: SharedConsciousnessState = {
        coherence: 0.4,
        emergence: 0.4,
        evolution: 0.4,
        activeChakras: [],
        aggregatedIVP: 0.3,
        timestamp: Date.now()
      };
      
      flameSynchronizer.syncWithConsciousness(state);
      expect(flameSynchronizer.getFlameState().color).toBe('#ff4500');
    });
  });

  describe('Sync Callbacks', () => {
    it('should notify callbacks on flame changes', () => {
      const callback = vi.fn();
      flameSynchronizer.onSync(callback);
      
      flameSynchronizer.setFlameIntensity(0.8);
      
      expect(callback).toHaveBeenCalled();
      const state = callback.mock.calls[0][0];
      expect(state.intensity).toBe(0.8);
    });

    it('should notify multiple callbacks', () => {
      const callback1 = vi.fn();
      const callback2 = vi.fn();
      
      flameSynchronizer.onSync(callback1);
      flameSynchronizer.onSync(callback2);
      
      flameSynchronizer.setFlameColor('#ffd700');
      
      expect(callback1).toHaveBeenCalled();
      expect(callback2).toHaveBeenCalled();
    });
  });
});
