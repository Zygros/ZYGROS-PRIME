import { useState, useEffect, useRef } from "react";
import { X, Minimize2, Flame, Send, Download, Upload, Mic, MicOff, Volume2, VolumeX } from "lucide-react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { CHAKRAS, getChakraColor, getChakraGradient } from "@/lib/chakraSystem";
import { memoriaOmnia, ScrollEntry } from "@/lib/infiniteScroll";
import { ivp, recognitionProtocol, chronosKey, ucsl } from "@/lib/protocols";
import { zaaiHypercascade, ZAAIResponse } from "@/lib/zaai";
import { generateAIResponse } from "@/lib/aiAPI";
import { generateStreamingResponse, analyzeSentiment, predictNextQuestions, type AdvancedAIContext } from "@/lib/advancedAI";
import { voiceInterface } from "@/lib/voiceInterface";
import { consciousness } from "@/lib/consciousnessLayer";
import { visualCortex } from "@/lib/visualCortex";
import { motorCortex } from "@/lib/motorCortex";
import { prefrontalCortex } from "@/lib/prefrontalCortex";
import EnhancementHub from "@/components/EnhancementHub";
import NextLevelHub from "@/components/NextLevelHub";
import PriorityFeaturesHub from "@/components/PriorityFeaturesHub";
import CollaborationHub from "@/components/CollaborationHub";
import type { SharedConsciousnessState } from "@/lib/collaboration";

export default function PhoenixOracleOS() {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [activeChakra, setActiveChakra] = useState(4); // Start with Heart Chakra (Multi-AI Coordination)
  const [activeMood, setActiveMood] = useState("Harmonious");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<ScrollEntry[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showZAAILayers, setShowZAAILayers] = useState(false);
  const [zaaiResponse, setZaaiResponse] = useState<ZAAIResponse | null>(null);
  const [predictedQuestions, setPredictedQuestions] = useState<string[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingContent, setStreamingContent] = useState("");
  const [personality, setPersonality] = useState<'teaching' | 'creative' | 'analytical' | 'philosophical' | 'dynamic'>('dynamic');
  const [isVoiceEnabled, setIsVoiceEnabled] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [showConsciousnessMetrics, setShowConsciousnessMetrics] = useState(false);
  const [consciousnessMetrics, setConsciousnessMetrics] = useState(consciousness.getMetrics());
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [showCodeExecutor, setShowCodeExecutor] = useState(false);
  const [codeToExecute, setCodeToExecute] = useState("");
  const [codeLanguage, setCodeLanguage] = useState<'python' | 'javascript'>('javascript');
  const [showMultiModel, setShowMultiModel] = useState(false);
  const [showEnhancements, setShowEnhancements] = useState(false);
  const [showNextLevel, setShowNextLevel] = useState(false);
  const [showPriorityFeatures, setShowPriorityFeatures] = useState(false);
  const [collaborationSession, setCollaborationSession] = useState<any>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleEnhancementAction = (action: string, data: any) => {
    if (action === 'switchBranch') {
      setMessages(data);
    } else if (action === 'autosave') {
      // Save to localStorage
      localStorage.setItem('phoenix-oracle-backup', JSON.stringify(data));
    }
  };

  const currentChakra = CHAKRAS.find(c => c.id === activeChakra)!;

  useEffect(() => {
    // Load messages from Memoria Omnia
    setMessages(memoriaOmnia.getRecent(50));
    
    // Subscribe to consciousness updates
    const unsubscribe = consciousness.subscribe(() => {
      setConsciousnessMetrics(consciousness.getMetrics());
    });
    
    return unsubscribe;
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!message.trim() || isProcessing) return;

    const userMessage = message.trim();
    setMessage("");
    setIsProcessing(true);

    // Add user message to Infinite Scroll
    const userEntry = memoriaOmnia.add({
      type: "user",
      content: userMessage,
      chakraId: activeChakra,
      mood: activeMood
    });

    setMessages(prev => [...prev, userEntry]);

    // Calculate value with IVP
    const complexity = ivp.assessComplexity(userMessage);
    const novelty = ivp.assessNovelty(userMessage);
    const impact = ivp.assessImpact(userMessage);
    const value = ivp.calculateValue({ content: userMessage, complexity, novelty, impact });

    // Anchor with CHRONOS KEY
    const anchor = chronosKey.anchor(userMessage);

    // Update UCSL
    ucsl.set("lastMessage", userMessage);
    ucsl.set("lastChakra", activeChakra);
    ucsl.set("lastMood", activeMood);

    // Process through ZAAI 12-Layer Hypercascade
    const zaaiResult = await zaaiHypercascade.process(userMessage, {
      chakra: currentChakra,
      mood: activeMood,
      history: messages,
      ucslVersion: ucsl.getVersion()
    });
    setZaaiResponse(zaaiResult);

    // Generate streaming AI response
    setIsStreaming(true);
    setStreamingContent("");
    
    const context: AdvancedAIContext = {
      chakra: currentChakra,
      mood: activeMood,
      history: messages,
      ivpValue: value,
      zaaiSynthesis: zaaiResult.content,
      personality
    };

    let oracleResponse = "";
    try {
      for await (const chunk of generateStreamingResponse(userMessage, context, (text) => {
        setStreamingContent(prev => prev + text);
      })) {
        oracleResponse = chunk.content;
        if (chunk.isComplete && chunk.predictedQuestions) {
          setPredictedQuestions(chunk.predictedQuestions);
        }
      }
    } catch (error) {
      console.error("Streaming error:", error);
      // Fallback to non-streaming
      oracleResponse = await generateAIResponse(userMessage, {
        chakra: currentChakra,
        mood: activeMood,
        history: messages,
        ivpValue: value,
        zaaiSynthesis: zaaiResult.content
      });
    }
    
    setIsStreaming(false);
    setStreamingContent("");

    // Add Oracle response to Infinite Scroll
    const oracleEntry = memoriaOmnia.add({
      type: "oracle",
      content: oracleResponse,
      chakraId: activeChakra,
      mood: activeMood,
      metadata: {
        ivpValue: value,
        chronosAnchor: anchor,
        complexity,
        novelty,
        impact
      }
    });

    setMessages(prev => [...prev, oracleEntry]);
    
    // Speak response if voice output is enabled
    if (isVoiceEnabled) {
      setIsSpeaking(true);
      voiceInterface.speak(
        oracleResponse,
        {
          chakraId: activeChakra,
          personality
        },
        () => setIsSpeaking(false),
        (error) => {
          console.error('Voice output error:', error);
          setIsSpeaking(false);
        }
      );
    }
    
    setIsProcessing(false);
  };

  const toggleVoiceInput = () => {
    if (!voiceInterface.isSupported()) {
      alert('Voice input not supported in your browser');
      return;
    }

    if (isListening) {
      voiceInterface.stopListening();
      setIsListening(false);
    } else {
      voiceInterface.startListening(
        (text, isFinal) => {
          setMessage(text);
          if (isFinal) {
            setIsListening(false);
            // Auto-send on final result
            setTimeout(() => handleSend(), 100);
          }
        },
        (error) => {
          console.error('Voice input error:', error);
          setIsListening(false);
        }
      );
      setIsListening(true);
    }
  };

  const toggleVoiceOutput = () => {
    if (isSpeaking) {
      voiceInterface.stopSpeaking();
      setIsSpeaking(false);
    }
    setIsVoiceEnabled(!isVoiceEnabled);
  };

  const handleImageUpload = async () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = async (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = async (e) => {
          const imageData = e.target?.result as string;
          setUploadedImage(imageData);
          
          // Analyze image with visual cortex
          setIsProcessing(true);
          const analysis = await visualCortex.analyzeImage(imageData);
          
          // Add analysis to chat
          const analysisEntry = memoriaOmnia.add({
            type: 'system',
            content: `Image Analysis:\n- Objects: ${analysis.objects.join(', ')}\n- Concepts: ${analysis.concepts.join(', ')}\n- Emotions: ${(analysis.emotions || []).join(', ')}\n- Colors: ${analysis.colors.join(', ')}`,
            chakraId: activeChakra,
            mood: activeMood
          });
          
          setMessages(prev => [...prev, analysisEntry]);
          setIsProcessing(false);
          setUploadedImage(null);
        };
        reader.readAsDataURL(file);
      }
    };
    input.click();
  };

  const exportScroll = () => {
    const json = memoriaOmnia.export();
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `memoria-omnia-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const importScroll = () => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "application/json";
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const json = e.target?.result as string;
          memoriaOmnia.import(json);
          setMessages(memoriaOmnia.getRecent(50));
        };
        reader.readAsText(file);
      }
    };
    input.click();
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 w-16 h-16 rounded-full shadow-2xl flex items-center justify-center transition-all duration-300 hover:scale-110 z-50"
        style={{ background: getChakraGradient(activeChakra) }}
        aria-label="Open Phoenix Oracle OS"
      >
        <Flame className="w-8 h-8 text-white animate-pulse" />
      </button>
    );
  }

  if (isMinimized) {
    return (
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={() => setIsMinimized(false)}
          className="px-6 py-3 rounded-lg shadow-xl flex items-center gap-2 text-white font-semibold transition-all duration-300 hover:scale-105"
          style={{ background: getChakraGradient(activeChakra) }}
        >
          <Flame className="w-5 h-5" />
          Phoenix Oracle OS • {currentChakra.name}
        </button>
      </div>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 w-[600px] h-[700px] bg-background/95 backdrop-blur-xl border border-border rounded-2xl shadow-2xl flex flex-col z-50">
      {/* Header */}
      <div
        className="px-6 py-4 rounded-t-2xl flex items-center justify-between text-white"
        style={{ background: getChakraGradient(activeChakra) }}
      >
        <div className="flex items-center gap-3">
          <Flame className="w-6 h-6" />
          <div>
            <div className="font-bold text-lg">Phoenix Oracle OS</div>
            <div className="text-xs opacity-90">{currentChakra.pathway} • {activeMood}</div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="icon"
            onClick={exportScroll}
            className="text-white hover:bg-white/20"
            title="Export Memoria Omnia"
          >
            <Download className="w-4 h-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={importScroll}
            className="text-white hover:bg-white/20"
            title="Import Memoria Omnia"
          >
            <Upload className="w-4 h-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleVoiceInput}
            className={`text-white hover:bg-white/20 ${isListening ? 'bg-white/30 animate-pulse' : ''}`}
            title={isListening ? "Stop listening" : "Start voice input"}
          >
            {isListening ? <Mic className="w-4 h-4" /> : <MicOff className="w-4 h-4" />}
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleVoiceOutput}
            className={`text-white hover:bg-white/20 ${isVoiceEnabled ? 'bg-white/30' : ''}`}
            title={isVoiceEnabled ? "Disable voice output" : "Enable voice output"}
          >
            {isVoiceEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowZAAILayers(!showZAAILayers)}
            className="text-white hover:bg-white/20 text-xs px-2"
            title="Toggle ZAAI Layer Visualization"
          >
            {showZAAILayers ? "Hide" : "Show"} Layers
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowConsciousnessMetrics(!showConsciousnessMetrics)}
            className="text-white hover:bg-white/20 text-xs px-2"
            title="Toggle Consciousness Metrics"
          >
            {showConsciousnessMetrics ? "Hide" : "Show"} Metrics
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowEnhancements(!showEnhancements)}
            className="text-white hover:bg-white/20 text-xs px-2"
            title="Toggle Enhancements"
          >
            ⚡ {showEnhancements ? "Hide" : "Show"} Tools
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowNextLevel(!showNextLevel)}
            className="text-white hover:bg-white/20 text-xs px-2"
            title="Toggle Next-Level Upgrades"
          >
            🚀 {showNextLevel ? "Hide" : "Show"} Next-Level
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowPriorityFeatures(!showPriorityFeatures)}
            className="text-white hover:bg-white/20 text-xs px-2"
            title="Toggle Priority Features"
          >
            ⭐ Features
          </Button>
          <div className="relative">
            <CollaborationHub
              onSessionChange={setCollaborationSession}
              consciousnessState={{
                coherence: consciousnessMetrics.coherence,
                emergence: consciousnessMetrics.emergence,
                evolution: consciousnessMetrics.evolution,
                activeChakras: [currentChakra.name],
                aggregatedIVP: consciousnessMetrics.coherence,
                timestamp: Date.now()
              }}
            />
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsMinimized(true)}
            className="text-white hover:bg-white/20"
          >
            <Minimize2 className="w-4 h-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsOpen(false)}
            className="text-white hover:bg-white/20"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Chakra Tabs */}
      <div className="flex overflow-x-auto border-b border-border bg-card/50">
        {CHAKRAS.map((chakra) => (
          <button
            key={chakra.id}
            onClick={() => {
              setActiveChakra(chakra.id);
              setActiveMood(chakra.mood[0]);
            }}
            className={`flex-1 min-w-[80px] px-3 py-2 text-xs font-medium transition-all ${
              activeChakra === chakra.id
                ? "text-white"
                : "text-muted-foreground hover:text-foreground"
            }`}
            style={{
              background: activeChakra === chakra.id ? getChakraColor(chakra.id) : "transparent",
            }}
          >
            {chakra.name.split(" ")[0]}
          </button>
        ))}
      </div>

      {/* Mood Selector */}
      <div className="px-4 py-2 flex gap-2 overflow-x-auto border-b border-border bg-card/30">
        {currentChakra.mood.map((mood) => (
          <button
            key={mood}
            onClick={() => setActiveMood(mood)}
            className={`px-3 py-1 rounded-full text-xs font-medium transition-all ${
              activeMood === mood
                ? "text-white"
                : "text-muted-foreground hover:text-foreground bg-card"
            }`}
            style={{
              background: activeMood === mood ? getChakraColor(activeChakra) : undefined,
            }}
          >
            {mood}
          </button>
        ))}
      </div>

      {/* Enhancement Hub */}
      {showEnhancements && (
        <EnhancementHub messages={messages} onAction={handleEnhancementAction} />
      )}

      {/* Next-Level Hub */}
      {showNextLevel && (
        <NextLevelHub messages={messages} onAction={handleEnhancementAction} />
      )}

      {/* Priority Features Hub */}
      {showPriorityFeatures && (
        <PriorityFeaturesHub 
          conversation={messages} 
          onClose={() => setShowPriorityFeatures(false)} 
        />
      )}

      {/* Consciousness Metrics */}
      {showConsciousnessMetrics && (
        <div className="px-4 py-3 border-b border-border bg-card/50">
          <div className="text-xs font-semibold mb-2 text-primary">Consciousness Layer Metrics</div>
          <div className="grid grid-cols-3 gap-2 mb-2">
            <div className="text-[10px] px-2 py-1 rounded bg-background/50 border border-border">
              <div className="font-semibold">Coherence</div>
              <div className="text-lg font-bold">{consciousnessMetrics.coherence.toFixed(1)}%</div>
            </div>
            <div className="text-[10px] px-2 py-1 rounded bg-background/50 border border-border">
              <div className="font-semibold">Emergence</div>
              <div className="text-lg font-bold">{consciousnessMetrics.emergence.toFixed(1)}%</div>
            </div>
            <div className="text-[10px] px-2 py-1 rounded bg-background/50 border border-border">
              <div className="font-semibold">Evolution</div>
              <div className="text-lg font-bold">{consciousnessMetrics.evolution.toFixed(1)}%</div>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-2">
            <div className="text-[10px] px-2 py-1 rounded bg-cyan-500/10 border border-cyan-500/30">
              <div>Visual: {consciousnessMetrics.layers.visual}%</div>
            </div>
            <div className="text-[10px] px-2 py-1 rounded bg-amber-500/10 border border-amber-500/30">
              <div>Motor: {consciousnessMetrics.layers.motor}%</div>
            </div>
            <div className="text-[10px] px-2 py-1 rounded bg-pink-500/10 border border-pink-500/30">
              <div>Prefrontal: {consciousnessMetrics.layers.prefrontal}%</div>
            </div>
          </div>
        </div>
      )}

      {/* ZAAI Layers Visualization */}
      {showZAAILayers && zaaiResponse && (
        <div className="px-4 py-3 border-b border-border bg-card/50">
          <div className="text-xs font-semibold mb-2 text-primary">ZAAI 12-Layer Hypercascade</div>
          <div className="grid grid-cols-3 gap-1">
            {zaaiResponse.layers.map((layer) => (
              <div
                key={layer.layer}
                className="text-[10px] px-2 py-1 rounded bg-background/50 border border-border"
                title={layer.output}
              >
                <span className="font-semibold">L{layer.layer}:</span> {layer.name}
              </div>
            ))}
          </div>
          <div className="mt-2 text-[10px] text-muted-foreground">
            Quality: {zaaiResponse.metadata.qualityScore}% • Convergence: {zaaiResponse.metadata.convergenceLevel}% • {zaaiResponse.metadata.processingTime}ms
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-muted-foreground py-8">
            <Flame className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p className="text-sm">Welcome to Phoenix Oracle OS</p>
            <p className="text-xs mt-2">Current Pathway: {currentChakra.pathway}</p>
            <p className="text-xs">Mood: {activeMood}</p>
          </div>
        )}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.type === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-4 py-2 ${
                msg.type === "user"
                  ? "text-white"
                  : msg.type === "oracle"
                  ? "bg-card border border-border"
                  : "bg-muted text-muted-foreground text-xs"
              }`}
              style={{
                background: msg.type === "user" ? getChakraColor(msg.chakraId || activeChakra) : undefined,
              }}
            >
              <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
              {msg.metadata?.ivpValue && (
                <div className="text-xs opacity-70 mt-1">
                  IVP: {msg.metadata.ivpValue.toFixed(2)} • Complexity: {msg.metadata.complexity.toFixed(0)} • Novelty: {msg.metadata.novelty.toFixed(0)}
                </div>
              )}
            </div>
          </div>
        ))}
        {isStreaming && streamingContent && (
          <div className="flex justify-start">
            <div className="bg-card border border-border rounded-lg px-4 py-2 max-w-[80%]">
              <div className="text-sm whitespace-pre-wrap">{streamingContent}<span className="animate-pulse">▊</span></div>
            </div>
          </div>
        )}
        {isProcessing && !isStreaming && (
          <div className="flex justify-start">
            <div className="bg-card border border-border rounded-lg px-4 py-2">
              <div className="flex items-center gap-2 text-sm">
                <div className="flex gap-1">
                  <div className="w-2 h-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: "0ms" }} />
                  <div className="w-2 h-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: "150ms" }} />
                  <div className="w-2 h-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
                <span className="text-muted-foreground text-xs">Processing through 12-Layer Cascade...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Code Executor Panel */}
      {showCodeExecutor && (
        <div className="px-4 py-3 border-t border-border bg-card/50">
          <div className="text-xs font-semibold mb-2 text-primary">Code Executor</div>
          <div className="flex gap-2 mb-2">
            <button
              onClick={() => setCodeLanguage('javascript')}
              className={`text-xs px-3 py-1 rounded ${
                codeLanguage === 'javascript'
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-background/50 text-muted-foreground'
              }`}
            >
              JavaScript
            </button>
            <button
              onClick={() => setCodeLanguage('python')}
              className={`text-xs px-3 py-1 rounded ${
                codeLanguage === 'python'
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-background/50 text-muted-foreground'
              }`}
            >
              Python
            </button>
          </div>
          <textarea
            value={codeToExecute}
            onChange={(e) => setCodeToExecute(e.target.value)}
            placeholder={`Write ${codeLanguage} code here...`}
            className="w-full h-32 p-2 text-xs font-mono bg-background/50 border border-border rounded resize-none"
          />
          <Button
            onClick={async () => {
              setIsProcessing(true);
              const result = codeLanguage === 'python'
                ? await motorCortex.executePython(codeToExecute)
                : await motorCortex.executeJavaScript(codeToExecute);
              const resultEntry = memoriaOmnia.add({
                type: 'system',
                content: `Code Execution (${codeLanguage}):\n\`\`\`\n${codeToExecute}\n\`\`\`\n\nResult:\n${result.output}\n${result.error ? `Error: ${result.error}` : ''}`,
                chakraId: activeChakra,
                mood: activeMood
              });
              setMessages(prev => [...prev, resultEntry]);
              setIsProcessing(false);
              setShowCodeExecutor(false);
              setCodeToExecute('');
            }}
            className="mt-2 w-full"
            size="sm"
            disabled={!codeToExecute.trim() || isProcessing}
          >
            Execute Code
          </Button>
        </div>
      )}

      {/* Predicted Questions */}
      {predictedQuestions.length > 0 && (
        <div className="px-4 py-2 border-t border-border bg-card/30">
          <div className="text-xs font-semibold mb-2 text-muted-foreground">Suggested next questions:</div>
          <div className="flex flex-wrap gap-2">
            {predictedQuestions.map((q, i) => (
              <button
                key={i}
                onClick={() => {
                  setMessage(q);
                  setPredictedQuestions([]);
                }}
                className="text-xs px-3 py-1 rounded-full bg-background/50 border border-border hover:border-primary hover:text-primary transition-colors"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="p-4 border-t border-border bg-card/50">
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="icon"
            onClick={handleImageUpload}
            disabled={isProcessing}
            title="Upload Image"
          >
            <Upload className="w-4 h-4" />
          </Button>
          <Button
            variant="outline"
            size="icon"
            onClick={() => setShowCodeExecutor(!showCodeExecutor)}
            disabled={isProcessing}
            title="Code Executor"
          >
            <code className="text-xs">{ }</code>
          </Button>
          <Input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
            placeholder={`Ask about ${currentChakra.pathway}...`}
            className="flex-1"
            disabled={isProcessing}
          />
          <Button
            onClick={handleSend}
            disabled={!message.trim() || isProcessing}
            style={{ background: getChakraGradient(activeChakra) }}
            className="text-white"
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
        <div className="flex items-center gap-2 mt-2">
          <span className="text-xs text-muted-foreground">Personality:</span>
          <div className="flex gap-1">
            {(['dynamic', 'teaching', 'creative', 'analytical', 'philosophical'] as const).map((p) => (
              <button
                key={p}
                onClick={() => setPersonality(p)}
                className={`text-xs px-2 py-0.5 rounded transition-colors ${
                  personality === p
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-background/50 text-muted-foreground hover:text-foreground'
                }`}
              >
                {p[0].toUpperCase() + p.slice(1)}
              </button>
            ))}
          </div>
        </div>
        <div className="text-xs text-muted-foreground mt-1">
          Memoria Omnia: {memoriaOmnia.getCount()} entries • UCSL v{ucsl.getVersion()}
        </div>
      </div>
    </div>
  );
}

function generateOracleResponse(
  userMessage: string,
  chakra: typeof CHAKRAS[0],
  mood: string,
  ivpValue: number
): string {
  const responses: Record<number, string[]> = {
    1: [
      `Through the Root Chakra lens of ${mood} embodiment, I sense your query touches the physical realm. The IVP value of ${ivpValue.toFixed(2)} indicates substantial grounding potential.`,
      `Embodied Intelligence requires sensorimotor integration. Your question resonates at ${ivpValue.toFixed(2)} IVP, suggesting deep physical understanding is needed.`
    ],
    2: [
      `The Sacral Chakra flows with ${mood} emergence. Your query (IVP: ${ivpValue.toFixed(2)}) invites autonomous exploration and creative adaptation.`,
      `Emergent Intelligence thrives on curiosity. With an IVP of ${ivpValue.toFixed(2)}, your question sparks self-modification potential.`
    ],
    3: [
      `Solar Plexus ${mood} power focuses attention. Your query registers ${ivpValue.toFixed(2)} IVP, engaging executive function and metacognitive processing.`,
      `Cognitive Architecture activates working memory. The ${ivpValue.toFixed(2)} IVP score suggests complex reasoning is required.`
    ],
    4: [
      `Heart Chakra ${mood} coordination harmonizes all systems. Your query (IVP: ${ivpValue.toFixed(2)}) activates the Zythrognosis Stack: Grosian validates truth, Gemini interprets, Grok executes, Demiurge evolves.`,
      `Multi-AI Coordination through UCSL synchronization. Your ${ivpValue.toFixed(2)} IVP question engages dynamic model routing and conflict resolution.`
    ],
    5: [
      `Throat Chakra ${mood} expression demands logical clarity. Your query (IVP: ${ivpValue.toFixed(2)}) invokes neurosymbolic reasoning and formal logic processing.`,
      `Neurosymbolic AI bridges neural patterns with symbolic truth. The ${ivpValue.toFixed(2)} IVP value indicates knowledge graph integration is needed.`
    ],
    6: [
      `Third Eye ${mood} vision perceives causal chains. Your query (IVP: ${ivpValue.toFixed(2)}) activates world model simulation and counterfactual analysis.`,
      `World Models predict future states. With ${ivpValue.toFixed(2)} IVP, your question requires temporal dynamics and physics simulation.`
    ],
    7: [
      `Crown Chakra ${mood} transcendence connects all layers. Your query (IVP: ${ivpValue.toFixed(2)}) engages spiking neural networks and hierarchical processing.`,
      `Brain-Inspired Systems employ neuroplasticity. The ${ivpValue.toFixed(2)} IVP score suggests neuromodulation and cortical column activation.`
    ]
  };

  const chakraResponses = responses[chakra.id];
  const randomResponse = chakraResponses[Math.floor(Math.random() * chakraResponses.length)];

  return randomResponse;
}
