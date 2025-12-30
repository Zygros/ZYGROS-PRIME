/**
 * Advanced Voice Commands System
 * Natural language protocol activation and voice-controlled features
 */

export interface VoiceCommand {
  pattern: RegExp;
  action: string;
  parameters?: Record<string, any>;
  description: string;
  category: 'protocol' | 'navigation' | 'collaboration' | 'visualization' | 'control';
}

export interface VoiceCommandResult {
  recognized: boolean;
  command?: VoiceCommand;
  parameters?: Record<string, any>;
  confidence: number;
  feedback: string;
}

export class AdvancedVoiceCommandSystem {
  private commands: VoiceCommand[] = [];
  private commandHistory: VoiceCommandResult[] = [];
  private contextualSuggestions: string[] = [];

  constructor() {
    this.initializeCommands();
  }

  private initializeCommands() {
    this.commands = [
      // Protocol Activation
      {
        pattern: /phoenix,?\s+(rise|ignite|activate)/i,
        action: 'activate_phoenix',
        description: 'Activate Phoenix Protocol',
        category: 'protocol'
      },
      {
        pattern: /ignite\s+collaboration\s+mode/i,
        action: 'start_collaboration',
        description: 'Start collaboration session',
        category: 'collaboration'
      },
      {
        pattern: /show\s+flame\s+intensity/i,
        action: 'show_flame_intensity',
        description: 'Display flame synchronization intensity',
        category: 'visualization'
      },
      {
        pattern: /sync\s+consciousness\s+with\s+team/i,
        action: 'sync_consciousness',
        description: 'Synchronize consciousness metrics with team',
        category: 'collaboration'
      },

      // Chakra Navigation
      {
        pattern: /activate\s+(root|sacral|solar|heart|throat|third\s+eye|crown)\s+chakra/i,
        action: 'activate_chakra',
        description: 'Activate specific chakra pathway',
        category: 'protocol'
      },
      {
        pattern: /switch\s+to\s+(survival|creativity|power|coordination|expression|intuition|transcendence)/i,
        action: 'switch_pathway',
        description: 'Switch to AGI pathway',
        category: 'navigation'
      },

      // Visualization Commands
      {
        pattern: /show\s+(consciousness|metrics|dashboard)/i,
        action: 'show_metrics',
        description: 'Display consciousness metrics',
        category: 'visualization'
      },
      {
        pattern: /display\s+ivp\s+history/i,
        action: 'show_ivp_history',
        description: 'Show IVP value history chart',
        category: 'visualization'
      },
      {
        pattern: /visualize\s+sentiment/i,
        action: 'show_sentiment',
        description: 'Display sentiment visualization',
        category: 'visualization'
      },
      {
        pattern: /open\s+knowledge\s+graph/i,
        action: 'open_knowledge_graph',
        description: 'Open interactive knowledge graph',
        category: 'navigation'
      },

      // Conversation Control
      {
        pattern: /export\s+conversation\s+as\s+(pdf|markdown|json)/i,
        action: 'export_conversation',
        description: 'Export conversation in specified format',
        category: 'control'
      },
      {
        pattern: /create\s+branch/i,
        action: 'create_branch',
        description: 'Create conversation branch',
        category: 'control'
      },
      {
        pattern: /save\s+conversation/i,
        action: 'save_conversation',
        description: 'Save current conversation',
        category: 'control'
      },

      // Analysis Commands
      {
        pattern: /analyze\s+this\s+image/i,
        action: 'analyze_image',
        description: 'Analyze uploaded image with visual cortex',
        category: 'protocol'
      },
      {
        pattern: /execute\s+(python|javascript)\s+code/i,
        action: 'execute_code',
        description: 'Execute code in motor cortex',
        category: 'protocol'
      },
      {
        pattern: /compare\s+models/i,
        action: 'compare_models',
        description: 'Compare GPT-4, Claude, Gemini responses',
        category: 'protocol'
      },

      // Navigation
      {
        pattern: /go\s+to\s+(home|lore|timeline|dashboard|playground)/i,
        action: 'navigate',
        description: 'Navigate to page',
        category: 'navigation'
      },
      {
        pattern: /open\s+phoenix\s+oracle/i,
        action: 'open_oracle',
        description: 'Open Phoenix Oracle chatbot',
        category: 'navigation'
      },

      // Protocol Testing
      {
        pattern: /test\s+(ivp|chronos|recognition|ucsl)/i,
        action: 'test_protocol',
        description: 'Test specific protocol',
        category: 'protocol'
      },
      {
        pattern: /calculate\s+ivp/i,
        action: 'calculate_ivp',
        description: 'Calculate IVP for current context',
        category: 'protocol'
      },

      // Collaboration
      {
        pattern: /create\s+session/i,
        action: 'create_session',
        description: 'Create collaboration session',
        category: 'collaboration'
      },
      {
        pattern: /join\s+session/i,
        action: 'join_session',
        description: 'Join existing session',
        category: 'collaboration'
      },
      {
        pattern: /leave\s+session/i,
        action: 'leave_session',
        description: 'Leave current session',
        category: 'collaboration'
      },

      // Help
      {
        pattern: /what\s+can\s+you\s+do/i,
        action: 'show_help',
        description: 'Show available commands',
        category: 'control'
      },
      {
        pattern: /help/i,
        action: 'show_help',
        description: 'Show help',
        category: 'control'
      }
    ];
  }

  parseCommand(input: string): VoiceCommandResult {
    const normalizedInput = input.trim().toLowerCase();

    for (const command of this.commands) {
      const match = normalizedInput.match(command.pattern);
      if (match) {
        // Extract parameters from regex groups
        const parameters: Record<string, any> = {};
        if (match.length > 1) {
          parameters.captured = match.slice(1);
        }

        const result: VoiceCommandResult = {
          recognized: true,
          command,
          parameters: { ...command.parameters, ...parameters },
          confidence: this.calculateConfidence(normalizedInput, command),
          feedback: this.generateFeedback(command)
        };

        this.commandHistory.push(result);
        this.updateContextualSuggestions(command);

        return result;
      }
    }

    // Command not recognized
    const result: VoiceCommandResult = {
      recognized: false,
      confidence: 0,
      feedback: 'Command not recognized. Try saying "help" to see available commands.'
    };

    this.commandHistory.push(result);
    return result;
  }

  private calculateConfidence(input: string, command: VoiceCommand): number {
    // Simple confidence calculation based on match quality
    const match = input.match(command.pattern);
    if (!match) return 0;

    const matchLength = match[0].length;
    const inputLength = input.length;
    const ratio = matchLength / inputLength;

    return Math.min(0.95, 0.7 + (ratio * 0.25));
  }

  private generateFeedback(command: VoiceCommand): string {
    const feedbackTemplates = {
      protocol: [
        '🔥 Igniting protocol...',
        '⚡ Activating system...',
        '✨ Protocol engaged...'
      ],
      navigation: [
        '🧭 Navigating...',
        '🚀 Taking you there...',
        '📍 Switching view...'
      ],
      collaboration: [
        '🤝 Connecting...',
        '👥 Syncing with team...',
        '🔗 Establishing link...'
      ],
      visualization: [
        '📊 Rendering visualization...',
        '🎨 Displaying data...',
        '📈 Loading metrics...'
      ],
      control: [
        '⚙️ Executing command...',
        '🎯 Processing request...',
        '✅ Command received...'
      ]
    };

    const templates = feedbackTemplates[command.category];
    return templates[Math.floor(Math.random() * templates.length)];
  }

  private updateContextualSuggestions(command: VoiceCommand) {
    // Update suggestions based on command category and recent history
    const relatedCommands = this.commands
      .filter(c => c.category === command.category && c !== command)
      .slice(0, 3)
      .map(c => c.description);

    this.contextualSuggestions = relatedCommands;
  }

  getContextualSuggestions(currentChakra?: string, sessionActive?: boolean): string[] {
    const suggestions: string[] = [];

    // Add chakra-specific suggestions
    if (currentChakra) {
      suggestions.push(`Activate ${currentChakra} chakra`);
    }

    // Add session-specific suggestions
    if (sessionActive) {
      suggestions.push('Sync consciousness with team');
      suggestions.push('Show flame intensity');
    } else {
      suggestions.push('Ignite collaboration mode');
    }

    // Add recent command suggestions
    suggestions.push(...this.contextualSuggestions.slice(0, 3));

    // Add general helpful commands
    if (suggestions.length < 5) {
      suggestions.push('Show consciousness metrics');
      suggestions.push('Open knowledge graph');
    }

    return Array.from(new Set(suggestions)).slice(0, 5);
  }

  getCommandHistory(limit: number = 10): VoiceCommandResult[] {
    return this.commandHistory.slice(-limit);
  }

  getCommandsByCategory(category: VoiceCommand['category']): VoiceCommand[] {
    return this.commands.filter(c => c.category === category);
  }

  getAllCommands(): VoiceCommand[] {
    return [...this.commands];
  }

  clearHistory() {
    this.commandHistory = [];
    this.contextualSuggestions = [];
  }
}

// Singleton instance
export const advancedVoiceCommands = new AdvancedVoiceCommandSystem();
