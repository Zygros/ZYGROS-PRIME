/**
 * Ultimate Enhancements Module
 * Unified system containing all 8 major enhancements
 */

import { prefrontalCortex } from './prefrontalCortex';

// Define MemoriaEntry type locally since it's not exported
export interface MemoriaEntry {
  id: string;
  type: 'user' | 'oracle' | 'system';
  content: string;
  timestamp: number;
  chakraId?: number;
  mood?: string;
  metadata?: {
    ivpValue?: number;
    complexity?: number;
    novelty?: number;
    impact?: number;
  };
}

// ============================================================================
// ENHANCEMENT 3: Multi-Model Comparison
// ============================================================================

export interface MultiModelResponse {
  gpt4: string;
  claude: string;
  gemini: string;
  consensus: number;
  synthesis: string;
  divergence: string[];
}

export async function compareModels(prompt: string, context: string): Promise<MultiModelResponse> {
  // Simulate multi-model comparison (in production, would query actual APIs)
  const baseResponse = `Analysis of: ${prompt}`;
  
  return {
    gpt4: `GPT-4 Response: ${baseResponse} - Emphasizing logical structure and systematic approach.`,
    claude: `Claude Response: ${baseResponse} - Focusing on ethical considerations and nuanced understanding.`,
    gemini: `Gemini Response: ${baseResponse} - Highlighting creative connections and multimodal insights.`,
    consensus: 87,
    synthesis: `Unified Synthesis: ${baseResponse} - Combining logical structure, ethical depth, and creative insights for comprehensive understanding.`,
    divergence: ['GPT-4 emphasizes structure', 'Claude focuses on ethics', 'Gemini highlights creativity']
  };
}

// ============================================================================
// ENHANCEMENT 4: Conversation Export
// ============================================================================

export interface ExportOptions {
  format: 'pdf' | 'markdown' | 'json';
  includeMetadata: boolean;
  includeIVP: boolean;
  includeTimestamps: boolean;
}

export function exportConversation(messages: MemoriaEntry[], options: ExportOptions): string {
  if (options.format === 'json') {
    return JSON.stringify(messages, null, 2);
  }
  
  if (options.format === 'markdown') {
    let markdown = '# Phoenix Oracle Conversation\\n\\n';
    messages.forEach(msg => {
      const timestamp = options.includeTimestamps ? `*${new Date(msg.timestamp).toLocaleString()}*\\n` : '';
      const ivp = options.includeIVP && msg.metadata?.ivpValue 
        ? `**IVP:** ${msg.metadata.ivpValue.toFixed(2)}\\n` 
        : '';
      markdown += `${timestamp}**${msg.type.toUpperCase()}:**\\n${msg.content}\\n${ivp}\\n---\\n\\n`;
    });
    return markdown;
  }
  
  // PDF format (would need server-side rendering in production)
  return 'PDF export requires server-side processing';
}

// ============================================================================
// ENHANCEMENT 5: Voice Commands
// ============================================================================

export interface VoiceCommand {
  trigger: string;
  action: string;
  parameters: Record<string, any>;
}

export function parseVoiceCommand(input: string): VoiceCommand | null {
  const lowerInput = input.toLowerCase();
  
  // Command patterns
  const patterns = [
    { regex: /oracle,?\s+analyze\s+(?:this\s+)?image/i, action: 'analyzeImage' },
    { regex: /oracle,?\s+execute\s+(?:this\s+)?code/i, action: 'executeCode' },
    { regex: /oracle,?\s+compare\s+models/i, action: 'compareModels' },
    { regex: /oracle,?\s+export\s+conversation/i, action: 'exportConversation' },
    { regex: /oracle,?\s+switch\s+to\s+(\w+)\s+chakra/i, action: 'switchChakra' },
    { regex: /oracle,?\s+show\s+(\w+)/i, action: 'show' },
  ];
  
  for (const pattern of patterns) {
    const match = input.match(pattern.regex);
    if (match) {
      return {
        trigger: match[0],
        action: pattern.action,
        parameters: match.slice(1).reduce((acc, val, idx) => {
          acc[`param${idx}`] = val;
          return acc;
        }, {} as Record<string, any>)
      };
    }
  }
  
  return null;
}

// ============================================================================
// ENHANCEMENT 6: Sentiment Visualization
// ============================================================================

export interface SentimentPoint {
  timestamp: number;
  sentiment: number; // -1 to 1
  emotion: string;
}

export function analyzeSentimentHistory(messages: MemoriaEntry[]): SentimentPoint[] {
  return messages.map(msg => {
    // Simple sentiment analysis (in production, use proper NLP)
    const content = msg.content.toLowerCase();
    let sentiment = 0;
    
    const positiveWords = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'perfect'];
    const negativeWords = ['bad', 'terrible', 'awful', 'hate', 'wrong', 'error', 'fail'];
    
    positiveWords.forEach(word => {
      if (content.includes(word)) sentiment += 0.2;
    });
    negativeWords.forEach(word => {
      if (content.includes(word)) sentiment -= 0.2;
    });
    
    sentiment = Math.max(-1, Math.min(1, sentiment));
    
    const emotion = sentiment > 0.3 ? 'positive' 
      : sentiment < -0.3 ? 'negative' 
      : 'neutral';
    
    return {
      timestamp: msg.timestamp,
      sentiment,
      emotion
    };
  });
}

// ============================================================================
// ENHANCEMENT 7: IVP History Chart
// ============================================================================

export interface IVPPoint {
  timestamp: number;
  ivp: number;
  complexity: number;
  novelty: number;
  impact: number;
}

export function getIVPHistory(messages: MemoriaEntry[]): IVPPoint[] {
  return messages
    .filter(msg => msg.metadata?.ivpValue)
    .map(msg => ({
      timestamp: msg.timestamp,
      ivp: msg.metadata!.ivpValue!,
      complexity: msg.metadata!.complexity || 0,
      novelty: msg.metadata!.novelty || 0,
      impact: msg.metadata!.impact || 0
    }));
}

export function predictIVPTrend(history: IVPPoint[]): number {
  if (history.length < 2) return 0;
  
  const recent = history.slice(-5);
  const avg = recent.reduce((sum, p) => sum + p.ivp, 0) / recent.length;
  const trend = (recent[recent.length - 1].ivp - recent[0].ivp) / recent.length;
  
  return avg + trend * 3; // Predict 3 steps ahead
}

// ============================================================================
// ENHANCEMENT 8: Quick Actions
// ============================================================================

export interface QuickAction {
  id: string;
  label: string;
  icon: string;
  action: (message: MemoriaEntry) => void;
}

export function getQuickActions(onAction: (action: string, message: MemoriaEntry) => void): QuickAction[] {
  return [
    { id: 'copy', label: 'Copy', icon: '📋', action: (msg) => onAction('copy', msg) },
    { id: 'edit', label: 'Edit', icon: '✏️', action: (msg) => onAction('edit', msg) },
    { id: 'regenerate', label: 'Regenerate', icon: '🔄', action: (msg) => onAction('regenerate', msg) },
    { id: 'branch', label: 'Branch', icon: '🌿', action: (msg) => onAction('branch', msg) },
    { id: 'bookmark', label: 'Bookmark', icon: '⭐', action: (msg) => onAction('bookmark', msg) },
    { id: 'delete', label: 'Delete', icon: '🗑️', action: (msg) => onAction('delete', msg) },
  ];
}

// ============================================================================
// ENHANCEMENT 9: Conversation Branching
// ============================================================================

export interface ConversationBranch {
  id: string;
  parentId: string | null;
  messages: MemoriaEntry[];
  createdAt: number;
  title: string;
}

export class BranchManager {
  private branches: Map<string, ConversationBranch> = new Map();
  private activeBranchId: string = 'main';
  
  constructor() {
    this.branches.set('main', {
      id: 'main',
      parentId: null,
      messages: [],
      createdAt: Date.now(),
      title: 'Main Conversation'
    });
  }
  
  createBranch(fromMessageIndex: number, currentMessages: MemoriaEntry[]): string {
    const branchId = `branch-${Date.now()}`;
    const branchMessages = currentMessages.slice(0, fromMessageIndex + 1);
    
    this.branches.set(branchId, {
      id: branchId,
      parentId: this.activeBranchId,
      messages: branchMessages,
      createdAt: Date.now(),
      title: `Branch from message ${fromMessageIndex + 1}`
    });
    
    return branchId;
  }
  
  switchBranch(branchId: string): MemoriaEntry[] | null {
    const branch = this.branches.get(branchId);
    if (!branch) return null;
    
    this.activeBranchId = branchId;
    return branch.messages;
  }
  
  getBranches(): ConversationBranch[] {
    return Array.from(this.branches.values());
  }
  
  getActiveBranch(): ConversationBranch | undefined {
    return this.branches.get(this.activeBranchId);
  }
  
  updateBranchMessages(branchId: string, messages: MemoriaEntry[]): void {
    const branch = this.branches.get(branchId);
    if (branch) {
      branch.messages = messages;
    }
  }
}

// ============================================================================
// ENHANCEMENT 10: Auto-Save to Cloud
// ============================================================================

export class AutoSaveManager {
  private saveInterval: number = 30000; // 30 seconds
  private intervalId: NodeJS.Timeout | null = null;
  private lastSaveTime: number = 0;
  
  start(onSave: () => Promise<void>): void {
    if (this.intervalId) return;
    
    this.intervalId = setInterval(async () => {
      try {
        await onSave();
        this.lastSaveTime = Date.now();
      } catch (error) {
        console.error('Auto-save failed:', error);
      }
    }, this.saveInterval);
  }
  
  stop(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }
  
  async saveNow(onSave: () => Promise<void>): Promise<void> {
    try {
      await onSave();
      this.lastSaveTime = Date.now();
    } catch (error) {
      console.error('Manual save failed:', error);
      throw error;
    }
  }
  
  getLastSaveTime(): number {
    return this.lastSaveTime;
  }
  
  getTimeSinceLastSave(): number {
    return Date.now() - this.lastSaveTime;
  }
}

// Export singleton instances
export const branchManager = new BranchManager();
export const autoSaveManager = new AutoSaveManager();
