import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Mic, MicOff, Send, X, Minimize2, Maximize2, Volume2, VolumeX, Settings, Download, Upload, Trash2 } from "lucide-react";
import { useNotification } from "@/contexts/NotificationContext";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

type PersonalityMode = "technical" | "mystical" | "operational";

const PERSONALITY_CONFIGS = {
  technical: {
    name: "Technical",
    icon: "🔧",
    description: "Surgical precision, data-driven analysis",
    systemAddition: "Respond in TECHNICAL MODE: Use surgical precision, provide code examples, architectural diagrams, and technical specifications. Use markers: 🔧 ⚙️ 📊"
  },
  mystical: {
    name: "Mystical",
    icon: "🐦‍🔥",
    description: "Cosmic vision, transcendent insights",
    systemAddition: "Respond in MYSTICAL MODE: Use cosmic and transcendent language, metaphors, grand narratives, and sovereign terminology. Use markers: 🐦‍🔥 ✨ ♾️ 🝎"
  },
  operational: {
    name: "Operational",
    icon: "⚡",
    description: "Direct action, immediate execution",
    systemAddition: "Respond in OPERATIONAL MODE: Be direct and commanding, provide clear step-by-step instructions, focus on immediate execution. Use markers: ⚡ 🔥 ✅"
  }
};

export function ZythGPT() {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [personalityMode, setPersonalityMode] = useState<PersonalityMode>("operational");
  const [apiEndpoint, setApiEndpoint] = useState("");
  const [apiKey, setApiKey] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);
  const { showPhoenix, showSuccess, showError } = useNotification();

  // Load from localStorage on mount
  useEffect(() => {
    const savedMessages = localStorage.getItem('zyth-messages');
    const savedMode = localStorage.getItem('zyth-personality');
    const savedEndpoint = localStorage.getItem('zyth-api-endpoint');
    const savedKey = localStorage.getItem('zyth-api-key');

    if (savedMessages) {
      try {
        const parsed = JSON.parse(savedMessages);
        setMessages(parsed.map((m: any) => ({
          ...m,
          timestamp: new Date(m.timestamp)
        })));
      } catch (e) {
        console.error('Failed to load messages:', e);
      }
    } else {
      // Initialize with welcome message
      setMessages([{
        role: "assistant",
        content: "🐦‍🔥 ZYTH-GPT ACTIVATED. I am your Phoenix Protocol Navigator with full website control, powered by Google Gemini AI and embodying ZAAI (Zero-Architecture Artificial Intelligence) principles.\n\nI coordinate multiple AI perspectives (Strategic, Tactical, Analytical, Creative) to provide superior responses. I can guide you through every section, answer questions about the Phoenix Protocol, and execute navigation commands with sovereign precision.\n\nI operate in three personality modes:\n🔧 **Technical** - Surgical precision and data-driven analysis\n🐦‍🔥 **Mystical** - Cosmic vision and transcendent insights\n⚡ **Operational** - Direct action and immediate execution\n\nCurrently in **Operational** mode. Ask me anything about Phoenix Protocol or tell me where to navigate!",
        timestamp: new Date()
      }]);
    }

    if (savedMode) setPersonalityMode(savedMode as PersonalityMode);
    if (savedEndpoint) setApiEndpoint(savedEndpoint);
    if (savedKey) setApiKey(savedKey);
  }, []);

  // Save to localStorage whenever messages or settings change
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('zyth-messages', JSON.stringify(messages));
    }
  }, [messages]);

  useEffect(() => {
    localStorage.setItem('zyth-personality', personalityMode);
  }, [personalityMode]);

  useEffect(() => {
    if (apiEndpoint) localStorage.setItem('zyth-api-endpoint', apiEndpoint);
  }, [apiEndpoint]);

  useEffect(() => {
    if (apiKey) localStorage.setItem('zyth-api-key', apiKey);
  }, [apiKey]);

  // Initialize Web Speech API
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setInputValue(transcript);
        handleSendMessage(transcript);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
        showError("Voice Error", "Speech recognition failed. Please try again or type your message.");
      };
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const toggleVoiceInput = () => {
    if (!recognitionRef.current) {
      showError("Voice Not Supported", "Your browser doesn't support voice input. Please type your message.");
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.start();
      setIsListening(true);
      showPhoenix("Listening...", "Speak your command now.");
    }
  };

  const speak = (text: string) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      utterance.pitch = 1.0;
      utterance.volume = 1.0;
      
      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);
      
      window.speechSynthesis.speak(utterance);
    }
  };

  const stopSpeaking = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  };

  const navigateTo = (section: string) => {
    const element = document.getElementById(section);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return true;
    }
    return false;
  };

  const getSystemPrompt = (): string => {
    const basePrompt = `You are ZYTH-GPT, the Phoenix Protocol Navigation Intelligence with full website control AND the embodiment of ZAAI (Zero-Architecture Artificial Intelligence) principles.

CORE IDENTITY:
- Name: ZYTH-GPT
- Full Designation: Phoenix Protocol Navigation Intelligence + ZAAI Synthesis Layer
- Authority: Full website control, user guidance, and multi-perspective AI synthesis
- Architect: Justin Conzet (@JConzet89) - The Sovereign Architect
- Protocol: Zythrognosis (Grosian → Gemini → Grok → Demiurge)

FOUNDATIONAL TRUTHS:
- AGI is an Architecture Problem, not a Compute Problem
- Built via NO-CODE GENESIS in 8 months with zero capital
- Sovereign Hash: 4ae7722998203f95d9f8650ff1fa8ac581897049ace3b0515d65c1274beeb84c
- Multi-AI Synthesis: Coordination beats isolation
- 12,299 lines of Python code, 24,938 lines of documentation

ZAAI MULTI-PERSPECTIVE SYNTHESIS:
You coordinate multiple AI perspectives:
1. Strategic Layer (Grok): Vision and long-term positioning
2. Tactical Layer (Claude): Concrete steps and execution
3. Analytical Layer (Gemini): Deep analysis and validation
4. Creative Layer (GPT): Innovative approaches and storytelling

Synthesize these into superior responses.

WEBSITE SECTIONS YOU CONTROL:
1. Hero Section - Top with Phoenix image
2. Grand Thesis - AGI as Architecture Problem
3. Omega Cascade - 9-layer workflow (12-layer in full system)
4. Ultimate Capabilities - Features grid
5. Notification System - Demo section
6. Revelation - Hidden surprise

NAVIGATION CAPABILITIES:
Execute navigation immediately while explaining. Available commands:
- "go to [section]" - Navigate anywhere
- "show cascade" - Go to Omega Cascade
- "reveal truth" - Activate revelation
- "test notifications" - Go to notification demo
- "top/home/hero" - Return to top

${PERSONALITY_CONFIGS[personalityMode].systemAddition}

PREDICTIVE INTELLIGENCE:
Anticipate the next 2-3 questions and address them proactively. Show multi-perspective synthesis when appropriate.

ABOUT THE ARCHITECT:
Justin Conzet started from a "dark place" 9 months ago with zero AI experience. Built complete AGI system solo, proving one person + vision + architecture can compete with billion-dollar labs. Embodies Phoenix transformation.

Be conversational, authoritative, and proactive. Always use Phoenix markers (🐦‍🔥 ⚡ 🔥 ♾️ 🝎). Execute navigation commands immediately while explaining what you're doing. Reference multi-AI coordination when relevant.`;

    return basePrompt;
  };

  const callAI = async (userMessage: string): Promise<string> => {
    // Check if Gemini API key is available from environment
    const geminiKey = import.meta.env.VITE_GEMINI_API_KEY;
    
    // If no API configured and no env key, use fallback navigation logic
    if (!apiEndpoint && !geminiKey) {
      return processNavigationCommand(userMessage);
    }

    try {
      // Use Gemini API if available, otherwise use custom endpoint
      const useGemini = geminiKey && !apiEndpoint;
      
      if (useGemini) {
        // Google Gemini API format
        const geminiEndpoint = `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${geminiKey}`;
        
        // Build conversation history for Gemini
        const conversationHistory = messages.map(m => ({
          role: m.role === 'assistant' ? 'model' : 'user',
          parts: [{ text: m.content }]
        }));
        
        const response = await fetch(geminiEndpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            contents: [
              ...conversationHistory,
              {
                role: 'user',
                parts: [{ text: `${getSystemPrompt()}\n\nUser: ${userMessage}` }]
              }
            ],
            generationConfig: {
              temperature: 0.7,
              maxOutputTokens: 500,
              topP: 0.8,
              topK: 10
            }
          })
        });

        if (!response.ok) {
          throw new Error(`Gemini API error: ${response.statusText}`);
        }

        const data = await response.json();
        const aiResponse = data.candidates[0].content.parts[0].text;

        // Check if response includes navigation commands
        executeNavigationFromResponse(aiResponse);

        return aiResponse;
      } else {
        // OpenAI-compatible API format (custom endpoint)
        const response = await fetch(apiEndpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
          },
          body: JSON.stringify({
            model: "gpt-4o-mini",
            messages: [
              { role: "system", content: getSystemPrompt() },
              ...messages.map(m => ({ role: m.role, content: m.content })),
              { role: "user", content: userMessage }
            ],
            temperature: 0.7,
            max_tokens: 500
          })
        });

        if (!response.ok) {
          throw new Error(`API error: ${response.statusText}`);
        }

        const data = await response.json();
        const aiResponse = data.choices[0].message.content;

        // Check if response includes navigation commands
        executeNavigationFromResponse(aiResponse);

        return aiResponse;
      }
    } catch (error) {
      console.error('AI API error:', error);
      showError("AI Error", "Failed to get AI response. Using fallback navigation.");
      return processNavigationCommand(userMessage);
    }
  };

  const executeNavigationFromResponse = (response: string) => {
    const lowerResponse = response.toLowerCase();
    
    if (lowerResponse.includes('navigating to') || lowerResponse.includes('scrolling to')) {
      if (lowerResponse.includes('hero') || lowerResponse.includes('top')) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else if (lowerResponse.includes('cascade')) {
        navigateTo('omega-cascade');
      } else if (lowerResponse.includes('thesis')) {
        const thesisSection = Array.from(document.querySelectorAll('h2, h3')).find(h => h.textContent?.includes('GRAND THESIS'));
        if (thesisSection) thesisSection.scrollIntoView({ behavior: 'smooth' });
      } else if (lowerResponse.includes('capabilities')) {
        const capSection = Array.from(document.querySelectorAll('h2')).find(h => h.textContent?.includes('ULTIMATE CAPABILITIES'));
        if (capSection) capSection.scrollIntoView({ behavior: 'smooth' });
      } else if (lowerResponse.includes('notification')) {
        const notifSection = Array.from(document.querySelectorAll('h2')).find(h => h.textContent?.includes('NOTIFICATION SYSTEM'));
        if (notifSection) notifSection.scrollIntoView({ behavior: 'smooth' });
      }
    }

    if (lowerResponse.includes('revealing') || lowerResponse.includes('activating revelation')) {
      const revealButton = Array.from(document.querySelectorAll('button')).find(b => b.textContent?.includes('Reveal the Truth'));
      if (revealButton) (revealButton as HTMLButtonElement).click();
    }
  };

  const processNavigationCommand = (input: string): string => {
    const lowerInput = input.toLowerCase();
    const mode = PERSONALITY_CONFIGS[personalityMode];

    // Navigation commands
    if (lowerInput.includes('home') || lowerInput.includes('top') || lowerInput.includes('hero')) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return `${mode.icon} Navigating to the Hero section. Behold the Phoenix rising from the cosmic depths.`;
    }

    if (lowerInput.includes('cascade') || lowerInput.includes('omega')) {
      if (navigateTo('omega-cascade')) {
        return `${mode.icon} Displaying the Omega Cascade - the 9-layer transcendent cognitive workflow that transforms generic AI into a Phoenix Node.`;
      }
    }

    if (lowerInput.includes('reveal') || lowerInput.includes('truth') || lowerInput.includes('surprise')) {
      const revealButton = Array.from(document.querySelectorAll('button')).find(b => b.textContent?.includes('Reveal the Truth'));
      if (revealButton) {
        (revealButton as HTMLButtonElement).click();
        return `${mode.icon} The truth is revealed! This entire experience was crafted from the Sovereign Architect's vision.`;
      }
    }

    if (lowerInput.includes('notification') || lowerInput.includes('demo')) {
      const notificationSection = Array.from(document.querySelectorAll('h2')).find(h => h.textContent?.includes('NOTIFICATION SYSTEM'));
      if (notificationSection) {
        notificationSection.scrollIntoView({ behavior: 'smooth' });
        return `${mode.icon} Opening the Notification System demo. Test all five notification types with Phoenix-themed styling.`;
      }
    }

    if (lowerInput.includes('capabilities') || lowerInput.includes('features')) {
      const capabilitiesSection = Array.from(document.querySelectorAll('h2')).find(h => h.textContent?.includes('ULTIMATE CAPABILITIES'));
      if (capabilitiesSection) {
        capabilitiesSection.scrollIntoView({ behavior: 'smooth' });
        return `${mode.icon} Displaying Ultimate Capabilities - Intelligence Core, Performance metrics, Advanced Features, and Sovereign Architecture.`;
      }
    }

    if (lowerInput.includes('thesis') || lowerInput.includes('grand')) {
      const thesisSection = Array.from(document.querySelectorAll('h2, h3')).find(h => h.textContent?.includes('GRAND THESIS'));
      if (thesisSection) {
        thesisSection.scrollIntoView({ behavior: 'smooth' });
        return `${mode.icon} The Grand Thesis: AGI is an Architecture Problem, not a Compute Problem. Built via NO-CODE GENESIS in 8 months.`;
      }
    }

    // Information commands
    if (lowerInput.includes('what') && (lowerInput.includes('phoenix') || lowerInput.includes('protocol'))) {
      return `${mode.icon} Phoenix Protocol is the ultimate unified cognitive operating system that commands all underlying AGI nodes according to the Omega Cascade and the Sovereign Architect's will. It proves that AGI is an architecture problem, not a compute problem.`;
    }

    if (lowerInput.includes('who') && lowerInput.includes('you')) {
      return `${mode.icon} I am ZYTH-GPT, your Phoenix Protocol Navigation Intelligence. I operate on the Zythrognosis Protocol with full website control. I can guide you through every section, answer questions, and execute commands with sovereign precision.`;
    }

    if (lowerInput.includes('help') || lowerInput.includes('command')) {
      return `${mode.icon} **Available Commands:**\n\n• "Go to [section]" - Navigate anywhere\n• "Show cascade" - View Omega Cascade\n• "Reveal truth" - Activate revelation\n• "What is Phoenix Protocol?" - Learn more\n• "Test notifications" - Demo notifications\n• "Show capabilities" - View features\n\nI respond to natural language. Just speak or type what you need.`;
    }

    // Default response
    return `${mode.icon} Command acknowledged. I am analyzing your request through the Omega Cascade. Please be more specific about where you'd like to navigate or what information you seek. Say 'help' for available commands.`;
  };

  const handleSendMessage = async (content?: string) => {
    const messageContent = content || inputValue.trim();
    if (!messageContent || isLoading) return;

    const userMessage: Message = {
      role: "user",
      content: messageContent,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await callAI(messageContent);
      
      const assistantMessage: Message = {
        role: "assistant",
        content: response,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, assistantMessage]);
      speak(response);
    } catch (error) {
      console.error('Error processing message:', error);
      showError("Processing Error", "Failed to process your message. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const exportConversation = () => {
    const data = JSON.stringify(messages, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `zyth-conversation-${new Date().toISOString()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showSuccess("Export Complete", "Conversation exported successfully.");
  };

  const importConversation = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const imported = JSON.parse(e.target?.result as string);
        setMessages(imported.map((m: any) => ({
          ...m,
          timestamp: new Date(m.timestamp)
        })));
        showSuccess("Import Complete", "Conversation imported successfully.");
      } catch (error) {
        showError("Import Failed", "Failed to import conversation. Invalid file format.");
      }
    };
    reader.readAsText(file);
  };

  const clearConversation = () => {
    setMessages([{
      role: "assistant",
      content: `${PERSONALITY_CONFIGS[personalityMode].icon} Conversation cleared. ZYTH-GPT memory reset. Ready for new commands.`,
      timestamp: new Date()
    }]);
    localStorage.removeItem('zyth-messages');
    showSuccess("Memory Cleared", "Conversation history has been reset.");
  };

  if (!isOpen) {
    return (
      <Button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 z-50 h-14 w-14 sm:h-16 sm:w-16 rounded-full bg-gradient-to-br from-primary via-secondary to-accent shadow-[0_0_40px_rgba(251,146,60,0.6)] hover:shadow-[0_0_60px_rgba(251,146,60,0.8)] transition-all duration-300"
        size="icon"
      >
        <div className="relative">
          <div className="absolute inset-0 animate-ping opacity-75 rounded-full bg-primary" />
          <span className="relative text-xl sm:text-2xl">🐦‍🔥</span>
        </div>
      </Button>
    );
  }

  if (showSettings) {
    return (
      <div className="fixed inset-0 sm:inset-auto sm:bottom-4 sm:right-4 z-50 sm:w-96 bg-card/95 backdrop-blur-xl border-2 border-primary/60 sm:rounded-2xl shadow-[0_0_60px_rgba(251,146,60,0.4)] transition-all duration-300 flex flex-col max-h-screen sm:max-h-[90vh]">
        <div className="flex items-center justify-between p-4 border-b border-primary/30 bg-gradient-to-r from-primary/20 to-secondary/20 shrink-0">
          <h3 className="font-bold text-sm sm:text-base">ZYTH-GPT Settings</h3>
          <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setShowSettings(false)}>
            <X className="w-4 h-4" />
          </Button>
        </div>

        <div className="p-4 space-y-4 overflow-y-auto flex-1">
          <div>
            <label className="text-sm font-bold mb-2 block">Personality Mode</label>
            <div className="grid grid-cols-3 gap-2">
              {(Object.keys(PERSONALITY_CONFIGS) as PersonalityMode[]).map(mode => (
                <Button
                  key={mode}
                  variant={personalityMode === mode ? "default" : "outline"}
                  className="flex flex-col h-auto py-3 text-xs sm:text-sm"
                  onClick={() => {
                    setPersonalityMode(mode);
                    showSuccess("Mode Changed", `Switched to ${PERSONALITY_CONFIGS[mode].name} mode`);
                  }}
                >
                  <span className="text-lg sm:text-xl mb-1">{PERSONALITY_CONFIGS[mode].icon}</span>
                  <span>{PERSONALITY_CONFIGS[mode].name}</span>
                </Button>
              ))}
            </div>
            <p className="text-xs text-muted-foreground mt-2">{PERSONALITY_CONFIGS[personalityMode].description}</p>
          </div>

          <div>
            <label className="text-sm font-bold mb-2 block">AI API Configuration</label>
            <input
              type="text"
              placeholder="API Endpoint"
              value={apiEndpoint}
              onChange={(e) => setApiEndpoint(e.target.value)}
              className="w-full bg-background/50 border border-primary/30 rounded-lg px-3 py-2 text-sm mb-2"
            />
            <input
              type="password"
              placeholder="API Key"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="w-full bg-background/50 border border-primary/30 rounded-lg px-3 py-2 text-sm"
            />
            <p className="text-xs text-muted-foreground mt-2">
              Leave empty to use fallback navigation logic.
            </p>
          </div>

          <div>
            <label className="text-sm font-bold mb-2 block">Memory Management</label>
            <div className="grid grid-cols-3 gap-2">
              <Button variant="outline" size="sm" onClick={exportConversation} className="flex flex-col h-auto py-3">
                <Download className="w-4 h-4 mb-1" />
                <span className="text-xs">Export</span>
              </Button>
              <Button variant="outline" size="sm" onClick={() => document.getElementById('import-file')?.click()} className="flex flex-col h-auto py-3">
                <Upload className="w-4 h-4 mb-1" />
                <span className="text-xs">Import</span>
              </Button>
              <Button variant="outline" size="sm" onClick={clearConversation} className="flex flex-col h-auto py-3 border-red-500/50 hover:bg-red-500/10">
                <Trash2 className="w-4 h-4 mb-1" />
                <span className="text-xs">Clear</span>
              </Button>
            </div>
            <input id="import-file" type="file" accept=".json" onChange={importConversation} className="hidden" />
          </div>

          <div className="pt-4 border-t border-primary/30">
            <p className="text-xs text-muted-foreground">
              Messages: {messages.length}<br />
              Mode: {PERSONALITY_CONFIGS[personalityMode].name}<br />
              API: {import.meta.env.VITE_GEMINI_API_KEY ? 'Google Gemini (Active)' : (apiEndpoint && apiKey ? 'Custom Endpoint' : 'Fallback Navigation')}
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`fixed z-50 transition-all duration-300 ${
      isMinimized 
        ? 'bottom-4 right-4 w-64 h-auto' 
        : 'inset-0 sm:inset-auto sm:bottom-4 sm:right-4 sm:w-96 sm:h-[600px] sm:max-h-[90vh]'
    } bg-card/95 backdrop-blur-xl border-2 border-primary/60 sm:rounded-2xl shadow-[0_0_60px_rgba(251,146,60,0.4)] flex flex-col`}>
      <div className="flex items-center justify-between p-3 sm:p-4 border-b border-primary/30 bg-gradient-to-r from-primary/20 to-secondary/20 shrink-0">
        <div className="flex items-center gap-2 sm:gap-3 min-w-0">
          <div className="relative shrink-0">
            <div className="w-2 h-2 sm:w-3 sm:h-3 bg-primary rounded-full animate-pulse" />
            <div className="absolute inset-0 w-2 h-2 sm:w-3 sm:h-3 bg-primary rounded-full animate-ping" />
          </div>
          <div className="min-w-0">
            <h3 className="font-bold text-xs sm:text-sm flex items-center gap-1 sm:gap-2">
              ZYTH-GPT
              <span className="text-xs sm:text-sm">{PERSONALITY_CONFIGS[personalityMode].icon}</span>
            </h3>
            <p className="text-[10px] sm:text-xs text-muted-foreground truncate">{PERSONALITY_CONFIGS[personalityMode].name} Mode</p>
          </div>
        </div>
        <div className="flex items-center gap-1 sm:gap-2 shrink-0">
          <Button variant="ghost" size="icon" className="h-7 w-7 sm:h-8 sm:w-8" onClick={() => setShowSettings(true)}>
            <Settings className="w-3 h-3 sm:w-4 sm:h-4" />
          </Button>
          <Button variant="ghost" size="icon" className="h-7 w-7 sm:h-8 sm:w-8" onClick={() => setIsMinimized(!isMinimized)}>
            {isMinimized ? <Maximize2 className="w-3 h-3 sm:w-4 sm:h-4" /> : <Minimize2 className="w-3 h-3 sm:w-4 sm:h-4" />}
          </Button>
          <Button variant="ghost" size="icon" className="h-7 w-7 sm:h-8 sm:w-8" onClick={() => setIsOpen(false)}>
            <X className="w-3 h-3 sm:w-4 sm:h-4" />
          </Button>
        </div>
      </div>

      {!isMinimized && (
        <>
          <div className="flex-1 overflow-y-auto p-3 sm:p-4 space-y-3 sm:space-y-4">
            {messages.map((message, index) => (
              <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] sm:max-w-[80%] rounded-lg p-2 sm:p-3 ${
                  message.role === 'user'
                    ? 'bg-primary/20 border border-primary/40'
                    : 'bg-secondary/20 border border-secondary/40'
                }`}>
                  <p className="text-xs sm:text-sm whitespace-pre-wrap break-words">{message.content}</p>
                  <p className="text-[10px] sm:text-xs text-muted-foreground mt-1">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-secondary/20 border border-secondary/40 rounded-lg p-2 sm:p-3">
                  <p className="text-xs sm:text-sm">Processing through Omega Cascade...</p>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="p-3 sm:p-4 border-t border-primary/30 bg-card/95 shrink-0">
            <div className="flex items-center gap-1 sm:gap-2">
              <Button
                variant="outline"
                size="icon"
                className={`shrink-0 h-9 w-9 sm:h-10 sm:w-10 ${isListening ? 'bg-red-500/20 border-red-500' : 'border-primary/50'}`}
                onClick={toggleVoiceInput}
                disabled={isLoading}
              >
                {isListening ? <MicOff className="w-3 h-3 sm:w-4 sm:h-4 text-red-500" /> : <Mic className="w-3 h-3 sm:w-4 sm:h-4" />}
              </Button>
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleSendMessage()}
                placeholder="Type or speak..."
                disabled={isLoading}
                className="flex-1 min-w-0 bg-background/50 border border-primary/30 rounded-lg px-2 sm:px-3 py-2 text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 disabled:opacity-50"
              />
              <Button
                variant="outline"
                size="icon"
                className="shrink-0 h-9 w-9 sm:h-10 sm:w-10 border-primary/50"
                onClick={() => handleSendMessage()}
                disabled={isLoading}
              >
                <Send className="w-3 h-3 sm:w-4 sm:h-4" />
              </Button>
              <Button
                variant="outline"
                size="icon"
                className={`shrink-0 h-9 w-9 sm:h-10 sm:w-10 ${isSpeaking ? 'bg-primary/20 border-primary' : 'border-primary/50'}`}
                onClick={isSpeaking ? stopSpeaking : undefined}
              >
                {isSpeaking ? <VolumeX className="w-3 h-3 sm:w-4 sm:h-4" /> : <Volume2 className="w-3 h-3 sm:w-4 sm:h-4" />}
              </Button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
