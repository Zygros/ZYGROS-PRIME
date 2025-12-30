/**
 * HIGH-PRIORITY FEATURES MODULE
 * Top 20 features from 150-task roadmap
 */

import { prefrontalCortex } from './prefrontalCortex';

// ==================== AUTO-SAVE ====================

export const autoSave = {
  interval: null as NodeJS.Timeout | null,
  lastSave: null as Date | null,

  start: (saveFunction: () => void, intervalMs: number = 30000) => {
    if (autoSave.interval) {
      clearInterval(autoSave.interval);
    }

    autoSave.interval = setInterval(() => {
      saveFunction();
      autoSave.lastSave = new Date();
    }, intervalMs);
  },

  stop: () => {
    if (autoSave.interval) {
      clearInterval(autoSave.interval);
      autoSave.interval = null;
    }
  },

  saveNow: (data: any, key: string = 'phoenix_data') => {
    try {
      localStorage.setItem(key, JSON.stringify(data));
      autoSave.lastSave = new Date();
      return true;
    } catch (error) {
      console.error('Auto-save failed:', error);
      return false;
    }
  },

  load: (key: string = 'phoenix_data') => {
    try {
      const data = localStorage.getItem(key);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('Auto-load failed:', error);
      return null;
    }
  }
};

// ==================== CONVERSATION EXPORT ====================

export const conversationExport = {
  exportToJSON: (conversation: any[]) => {
    const data = JSON.stringify(conversation, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `phoenix-conversation-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  },

  exportToMarkdown: (conversation: any[]) => {
    let markdown = `# Phoenix Protocol Conversation\n\n`;
    markdown += `**Date:** ${new Date().toLocaleString()}\n\n`;
    markdown += `---\n\n`;

    conversation.forEach((msg, index) => {
      markdown += `## Message ${index + 1}\n\n`;
      markdown += `**Role:** ${msg.role}\n\n`;
      markdown += `**Content:** ${msg.content}\n\n`;
      if (msg.ivp) {
        markdown += `**IVP:** ${msg.ivp}\n\n`;
      }
      markdown += `---\n\n`;
    });

    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `phoenix-conversation-${Date.now()}.md`;
    a.click();
    URL.revokeObjectURL(url);
  },

  exportToPDF: (conversation: any[]) => {
    // Create HTML content
    let html = `
      <!DOCTYPE html>
      <html>
        <head>
          <title>Phoenix Protocol Conversation</title>
          <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .message { margin-bottom: 30px; padding: 20px; border-left: 4px solid #ea580c; }
            .user { background: #fff7ed; }
            .assistant { background: #fef3c7; }
            .meta { color: #666; font-size: 0.9em; margin-top: 10px; }
          </style>
        </head>
        <body>
          <h1>Phoenix Protocol Conversation</h1>
          <p><strong>Date:</strong> ${new Date().toLocaleString()}</p>
          <hr>
    `;

    conversation.forEach((msg, index) => {
      html += `
        <div class="message ${msg.role}">
          <strong>${msg.role === 'user' ? 'You' : 'Phoenix Oracle'}:</strong>
          <p>${msg.content}</p>
          <div class="meta">
            ${msg.ivp ? `IVP: ${msg.ivp} | ` : ''}
            Message ${index + 1}
          </div>
        </div>
      `;
    });

    html += `
        </body>
      </html>
    `;

    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `phoenix-conversation-${Date.now()}.html`;
    a.click();
    URL.revokeObjectURL(url);
  }
};

// ==================== SENTIMENT VISUALIZATION ====================

export interface SentimentData {
  timestamp: Date;
  sentiment: 'positive' | 'neutral' | 'negative';
  score: number;
  message: string;
}

export const sentimentVisualization = {
  data: [] as SentimentData[],

  analyzeSentiment: (message: string): SentimentData => {
    // Simple sentiment analysis
    const positiveWords = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'perfect'];
    const negativeWords = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'poor'];

    const lowerMessage = message.toLowerCase();
    let score = 0;

    positiveWords.forEach(word => {
      if (lowerMessage.includes(word)) score += 1;
    });

    negativeWords.forEach(word => {
      if (lowerMessage.includes(word)) score -= 1;
    });

    const sentiment: SentimentData['sentiment'] = 
      score > 0 ? 'positive' : score < 0 ? 'negative' : 'neutral';

    const data: SentimentData = {
      timestamp: new Date(),
      sentiment,
      score,
      message
    };

    sentimentVisualization.data.push(data);
    return data;
  },

  getChartData: () => {
    return sentimentVisualization.data.map(d => ({
      x: d.timestamp.getTime(),
      y: d.score,
      label: d.sentiment
    }));
  },

  getSummary: () => {
    const total = sentimentVisualization.data.length;
    const positive = sentimentVisualization.data.filter(d => d.sentiment === 'positive').length;
    const negative = sentimentVisualization.data.filter(d => d.sentiment === 'negative').length;
    const neutral = sentimentVisualization.data.filter(d => d.sentiment === 'neutral').length;

    return {
      total,
      positive,
      negative,
      neutral,
      positiveRate: total > 0 ? (positive / total) * 100 : 0,
      negativeRate: total > 0 ? (negative / total) * 100 : 0,
      neutralRate: total > 0 ? (neutral / total) * 100 : 0
    };
  }
};

// ==================== IVP HISTORY CHARTS ====================

export interface IVPDataPoint {
  timestamp: Date;
  ivp: number;
  complexity: number;
  novelty: number;
  impact: number;
}

export const ivpHistory = {
  data: [] as IVPDataPoint[],

  record: (ivp: number, complexity: number, novelty: number, impact: number) => {
    ivpHistory.data.push({
      timestamp: new Date(),
      ivp,
      complexity,
      novelty,
      impact
    });
  },

  getChartData: () => {
    return ivpHistory.data.map(d => ({
      x: d.timestamp.getTime(),
      y: d.ivp,
      complexity: d.complexity,
      novelty: d.novelty,
      impact: d.impact
    }));
  },

  getTrend: () => {
    if (ivpHistory.data.length < 2) return 'stable';

    const recent = ivpHistory.data.slice(-10);
    const avgRecent = recent.reduce((sum, d) => sum + d.ivp, 0) / recent.length;
    
    const older = ivpHistory.data.slice(-20, -10);
    if (older.length === 0) return 'stable';
    
    const avgOlder = older.reduce((sum, d) => sum + d.ivp, 0) / older.length;

    if (avgRecent > avgOlder * 1.1) return 'increasing';
    if (avgRecent < avgOlder * 0.9) return 'decreasing';
    return 'stable';
  },

  getStats: () => {
    if (ivpHistory.data.length === 0) return null;

    const values = ivpHistory.data.map(d => d.ivp);
    const avg = values.reduce((sum, v) => sum + v, 0) / values.length;
    const max = Math.max(...values);
    const min = Math.min(...values);

    return {
      average: avg,
      maximum: max,
      minimum: min,
      range: max - min,
      trend: ivpHistory.getTrend(),
      dataPoints: ivpHistory.data.length
    };
  }
};

// ==================== CONVERSATION BRANCHING ====================

export interface ConversationBranch {
  id: string;
  parentId: string | null;
  branchPoint: number; // Message index where branch occurred
  messages: any[];
  created: Date;
  name: string;
}

export const conversationBranching = {
  branches: [] as ConversationBranch[],
  currentBranch: null as ConversationBranch | null,

  createBranch: (parentId: string | null, branchPoint: number, messages: any[], name?: string): ConversationBranch => {
    const branch: ConversationBranch = {
      id: `branch-${Date.now()}`,
      parentId,
      branchPoint,
      messages: [...messages],
      created: new Date(),
      name: name || `Branch ${conversationBranching.branches.length + 1}`
    };

    conversationBranching.branches.push(branch);
    conversationBranching.currentBranch = branch;
    return branch;
  },

  switchBranch: (branchId: string): ConversationBranch | null => {
    const branch = conversationBranching.branches.find(b => b.id === branchId);
    if (branch) {
      conversationBranching.currentBranch = branch;
    }
    return branch || null;
  },

  getBranchTree: () => {
    const tree: any = {};

    conversationBranching.branches.forEach(branch => {
      if (!branch.parentId) {
        tree[branch.id] = { branch, children: [] };
      }
    });

    conversationBranching.branches.forEach(branch => {
      if (branch.parentId && tree[branch.parentId]) {
        tree[branch.parentId].children.push(branch);
      }
    });

    return tree;
  }
};

// ==================== QUICK ACTIONS ====================

export const quickActions = {
  copyMessage: (message: string) => {
    navigator.clipboard.writeText(message);
  },

  regenerateMessage: async (message: string, context: any) => {
    // Placeholder - would call AI API
    return `Regenerated: ${message}`;
  },

  bookmarkMessage: (messageId: string) => {
    const bookmarks = JSON.parse(localStorage.getItem('bookmarks') || '[]');
    if (!bookmarks.includes(messageId)) {
      bookmarks.push(messageId);
      localStorage.setItem('bookmarks', JSON.stringify(bookmarks));
    }
  },

  getBookmarks: (): string[] => {
    return JSON.parse(localStorage.getItem('bookmarks') || '[]');
  }
};

export default {
  autoSave,
  conversationExport,
  sentimentVisualization,
  ivpHistory,
  conversationBranching,
  quickActions
};
