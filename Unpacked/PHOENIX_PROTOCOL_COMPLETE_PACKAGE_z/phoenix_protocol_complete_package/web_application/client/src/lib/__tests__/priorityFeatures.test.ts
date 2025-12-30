import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  autoSave,
  conversationExport,
  sentimentVisualization,
  ivpHistory,
  conversationBranching,
  quickActions
} from '../priorityFeatures';

describe('Priority Features', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
  });

  describe('Auto-Save', () => {
    it('should save data to localStorage', () => {
      const testData = { messages: ['test1', 'test2'] };
      const result = autoSave.saveNow(testData);
      
      expect(result).toBe(true);
      expect(autoSave.lastSave).toBeInstanceOf(Date);
    });

    it('should load data from localStorage', () => {
      const testData = { messages: ['test1', 'test2'] };
      autoSave.saveNow(testData);
      
      const loaded = autoSave.load();
      expect(loaded).toEqual(testData);
    });

    it('should handle save errors gracefully', () => {
      // Mock localStorage to throw error
      const mockSetItem = vi.spyOn(Storage.prototype, 'setItem');
      mockSetItem.mockImplementation(() => {
        throw new Error('Storage full');
      });

      const result = autoSave.saveNow({ data: 'test' });
      expect(result).toBe(false);

      mockSetItem.mockRestore();
    });
  });

  describe('Conversation Export', () => {
    it('should export conversation to JSON', () => {
      const conversation = [
        { role: 'user', content: 'Hello', ivp: 0.5 },
        { role: 'assistant', content: 'Hi there', ivp: 0.6 }
      ];

      // Mock URL methods
      global.URL.createObjectURL = vi.fn(() => 'blob:mock');
      global.URL.revokeObjectURL = vi.fn();
      
      const mockClick = vi.fn();
      const mockCreateElement = vi.spyOn(document, 'createElement');
      mockCreateElement.mockReturnValue({
        click: mockClick,
        href: '',
        download: ''
      } as any);

      conversationExport.exportToJSON(conversation);

      expect(mockClick).toHaveBeenCalled();
      mockCreateElement.mockRestore();
    });

    it('should export conversation to Markdown', () => {
      const conversation = [
        { role: 'user', content: 'Hello' }
      ];

      // Mock URL methods
      global.URL.createObjectURL = vi.fn(() => 'blob:mock');
      global.URL.revokeObjectURL = vi.fn();
      
      const mockClick = vi.fn();
      const mockCreateElement = vi.spyOn(document, 'createElement');
      mockCreateElement.mockReturnValue({
        click: mockClick,
        href: '',
        download: ''
      } as any);

      conversationExport.exportToMarkdown(conversation);

      expect(mockClick).toHaveBeenCalled();
      mockCreateElement.mockRestore();
    });
  });

  describe('Sentiment Visualization', () => {
    it('should analyze positive sentiment', () => {
      const result = sentimentVisualization.analyzeSentiment('This is great and wonderful!');
      
      expect(result.sentiment).toBe('positive');
      expect(result.score).toBeGreaterThan(0);
    });

    it('should analyze negative sentiment', () => {
      const result = sentimentVisualization.analyzeSentiment('This is terrible and awful!');
      
      expect(result.sentiment).toBe('negative');
      expect(result.score).toBeLessThan(0);
    });

    it('should analyze neutral sentiment', () => {
      const result = sentimentVisualization.analyzeSentiment('This is a statement.');
      
      expect(result.sentiment).toBe('neutral');
      expect(result.score).toBe(0);
    });

    it('should generate chart data', () => {
      sentimentVisualization.data = []; // Reset
      sentimentVisualization.analyzeSentiment('Great!');
      sentimentVisualization.analyzeSentiment('Bad!');
      
      const chartData = sentimentVisualization.getChartData();
      expect(chartData.length).toBeGreaterThanOrEqual(2);
      expect(chartData[0]).toHaveProperty('x');
      expect(chartData[0]).toHaveProperty('y');
      expect(chartData[0]).toHaveProperty('label');
    });

    it('should generate summary statistics', () => {
      sentimentVisualization.data = []; // Reset
      sentimentVisualization.analyzeSentiment('Great!');
      sentimentVisualization.analyzeSentiment('Terrible!');
      sentimentVisualization.analyzeSentiment('Okay.');
      
      const summary = sentimentVisualization.getSummary();
      expect(summary.total).toBe(3);
      expect(summary.positive).toBe(1);
      expect(summary.negative).toBe(1);
      expect(summary.neutral).toBe(1);
      expect(summary.positiveRate).toBeCloseTo(33.33, 1);
    });
  });

  describe('IVP History', () => {
    it('should record IVP data points', () => {
      ivpHistory.data = []; // Reset
      ivpHistory.record(0.75, 8, 7, 9);
      
      expect(ivpHistory.data.length).toBe(1);
      expect(ivpHistory.data[0].ivp).toBe(0.75);
      expect(ivpHistory.data[0].complexity).toBe(8);
    });

    it('should generate chart data', () => {
      ivpHistory.data = []; // Reset
      ivpHistory.record(0.5, 5, 5, 5);
      ivpHistory.record(0.7, 7, 7, 7);
      
      const chartData = ivpHistory.getChartData();
      expect(chartData.length).toBe(2);
      expect(chartData[0].y).toBe(0.5);
      expect(chartData[1].y).toBe(0.7);
    });

    it('should detect increasing trend', () => {
      ivpHistory.data = []; // Reset
      // Add older lower values
      for (let i = 0; i < 10; i++) {
        ivpHistory.record(0.5, 5, 5, 5);
      }
      // Add recent higher values
      for (let i = 0; i < 10; i++) {
        ivpHistory.record(0.8, 8, 8, 8);
      }
      
      expect(ivpHistory.getTrend()).toBe('increasing');
    });

    it('should calculate statistics', () => {
      ivpHistory.data = []; // Reset
      ivpHistory.record(0.5, 5, 5, 5);
      ivpHistory.record(0.7, 7, 7, 7);
      ivpHistory.record(0.9, 9, 9, 9);
      
      const stats = ivpHistory.getStats();
      expect(stats).not.toBeNull();
      expect(stats!.average).toBeCloseTo(0.7, 1);
      expect(stats!.maximum).toBe(0.9);
      expect(stats!.minimum).toBe(0.5);
      expect(stats!.range).toBeCloseTo(0.4, 1);
    });
  });

  describe('Conversation Branching', () => {
    it('should create a new branch', () => {
      conversationBranching.branches = []; // Reset
      const messages = [{ content: 'test' }];
      
      const branch = conversationBranching.createBranch(null, 0, messages, 'Test Branch');
      
      expect(branch.id).toBeDefined();
      expect(branch.name).toBe('Test Branch');
      expect(branch.messages).toEqual(messages);
      expect(conversationBranching.currentBranch).toBe(branch);
    });

    it('should switch between branches', () => {
      conversationBranching.branches = []; // Reset
      const branch1 = conversationBranching.createBranch(null, 0, [], 'Branch 1');
      const branch2 = conversationBranching.createBranch(null, 0, [], 'Branch 2');
      
      expect(conversationBranching.branches.length).toBe(2);
      expect(conversationBranching.branches.some(b => b.name === 'Branch 1')).toBe(true);
      expect(conversationBranching.branches.some(b => b.name === 'Branch 2')).toBe(true);
    });

    it('should generate branch tree', () => {
      conversationBranching.branches = []; // Reset
      const parent = conversationBranching.createBranch(null, 0, [], 'Parent');
      conversationBranching.createBranch(parent.id, 5, [], 'Child');
      
      const tree = conversationBranching.getBranchTree();
      expect(Object.keys(tree).length).toBeGreaterThan(0);
    });
  });

  describe('Quick Actions', () => {
    it('should copy message to clipboard', async () => {
      const mockWriteText = vi.fn();
      Object.assign(navigator, {
        clipboard: {
          writeText: mockWriteText
        }
      });

      quickActions.copyMessage('Test message');
      expect(mockWriteText).toHaveBeenCalledWith('Test message');
    });

    it('should bookmark messages', () => {
      quickActions.bookmarkMessage('msg-123');
      const bookmarks = quickActions.getBookmarks();
      
      expect(bookmarks).toContain('msg-123');
    });

    it('should not duplicate bookmarks', () => {
      quickActions.bookmarkMessage('msg-456');
      quickActions.bookmarkMessage('msg-456');
      
      const bookmarks = quickActions.getBookmarks();
      expect(bookmarks.filter(id => id === 'msg-456').length).toBe(1);
    });
  });
});
