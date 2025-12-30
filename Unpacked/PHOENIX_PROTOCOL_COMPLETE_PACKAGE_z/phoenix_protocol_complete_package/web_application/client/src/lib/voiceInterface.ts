/**
 * Voice Interface for Phoenix Oracle
 * Speech-to-text input and text-to-speech output with chakra-tuned voices
 */

export interface VoiceConfig {
  chakraId: number;
  personality: 'dynamic' | 'teaching' | 'creative' | 'analytical' | 'philosophical';
  rate?: number;
  pitch?: number;
  volume?: number;
}

export class VoiceInterface {
  private recognition: SpeechRecognition | null = null;
  private synthesis: SpeechSynthesis;
  private isListening = false;
  private voices: SpeechSynthesisVoice[] = [];

  constructor() {
    this.synthesis = window.speechSynthesis;
    
    // Initialize speech recognition if available
    if ('webkitSpeechRecognition' in window) {
      const recognition = new (window as any).webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = 'en-US';
      this.recognition = recognition;
    } else if ('SpeechRecognition' in window) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = 'en-US';
      this.recognition = recognition;
    }

    // Load available voices
    this.loadVoices();
    if (this.synthesis.onvoiceschanged !== undefined) {
      this.synthesis.onvoiceschanged = () => this.loadVoices();
    }
  }

  private loadVoices() {
    this.voices = this.synthesis.getVoices();
  }

  /**
   * Check if voice interface is supported
   */
  isSupported(): boolean {
    return this.recognition !== null && 'speechSynthesis' in window;
  }

  /**
   * Start listening for voice input
   */
  startListening(
    onResult: (text: string, isFinal: boolean) => void,
    onError?: (error: string) => void
  ): void {
    if (!this.recognition) {
      onError?.('Speech recognition not supported');
      return;
    }

    if (this.isListening) {
      this.stopListening();
    }

    this.recognition.onresult = (event) => {
      const result = event.results[event.results.length - 1];
      const transcript = result[0].transcript;
      onResult(transcript, result.isFinal);
    };

    this.recognition.onerror = (event) => {
      onError?.(event.error);
      this.isListening = false;
    };

    this.recognition.onend = () => {
      this.isListening = false;
    };

    try {
      this.recognition.start();
      this.isListening = true;
    } catch (error) {
      onError?.('Failed to start recognition');
    }
  }

  /**
   * Stop listening for voice input
   */
  stopListening(): void {
    if (this.recognition && this.isListening) {
      this.recognition.stop();
      this.isListening = false;
    }
  }

  /**
   * Check if currently listening
   */
  getIsListening(): boolean {
    return this.isListening;
  }

  /**
   * Speak text with chakra-tuned voice
   */
  speak(
    text: string,
    config: VoiceConfig,
    onEnd?: () => void,
    onError?: (error: string) => void
  ): void {
    // Cancel any ongoing speech
    this.synthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    
    // Select voice based on personality and chakra
    const voice = this.selectVoice(config);
    if (voice) {
      utterance.voice = voice;
    }

    // Configure voice parameters based on chakra
    const voiceParams = this.getChakraVoiceParams(config.chakraId, config.personality);
    utterance.rate = config.rate ?? voiceParams.rate;
    utterance.pitch = config.pitch ?? voiceParams.pitch;
    utterance.volume = config.volume ?? voiceParams.volume;

    utterance.onend = () => onEnd?.();
    utterance.onerror = (event) => onError?.(event.error);

    this.synthesis.speak(utterance);
  }

  /**
   * Stop speaking
   */
  stopSpeaking(): void {
    this.synthesis.cancel();
  }

  /**
   * Check if currently speaking
   */
  isSpeaking(): boolean {
    return this.synthesis.speaking;
  }

  /**
   * Select appropriate voice based on personality and chakra
   */
  private selectVoice(config: VoiceConfig): SpeechSynthesisVoice | null {
    if (this.voices.length === 0) return null;

    // Personality-based voice selection
    const personalityPreferences: Record<string, string[]> = {
      teaching: ['Google US English', 'Microsoft David', 'Alex'],
      creative: ['Google UK English Female', 'Samantha', 'Victoria'],
      analytical: ['Google US English Male', 'Microsoft Mark', 'Daniel'],
      philosophical: ['Google UK English Male', 'Oliver', 'Thomas'],
      dynamic: ['Google US English', 'Samantha', 'Alex']
    };

    const preferences = personalityPreferences[config.personality] || personalityPreferences.dynamic;

    // Try to find preferred voice
    for (const pref of preferences) {
      const voice = this.voices.find(v => v.name.includes(pref));
      if (voice) return voice;
    }

    // Fallback to first English voice
    return this.voices.find(v => v.lang.startsWith('en')) || this.voices[0];
  }

  /**
   * Get voice parameters tuned to chakra energy
   */
  private getChakraVoiceParams(chakraId: number, personality: string): {
    rate: number;
    pitch: number;
    volume: number;
  } {
    // Base parameters by personality
    const baseParams: Record<string, { rate: number; pitch: number; volume: number }> = {
      teaching: { rate: 0.9, pitch: 1.0, volume: 1.0 },
      creative: { rate: 1.1, pitch: 1.2, volume: 0.9 },
      analytical: { rate: 0.95, pitch: 0.9, volume: 1.0 },
      philosophical: { rate: 0.85, pitch: 0.95, volume: 0.95 },
      dynamic: { rate: 1.0, pitch: 1.0, volume: 1.0 }
    };

    const base = baseParams[personality] || baseParams.dynamic;

    // Chakra-specific modulation
    const chakraModulation: Record<number, { rate: number; pitch: number }> = {
      1: { rate: -0.1, pitch: -0.2 },  // Root: slower, deeper
      2: { rate: 0.0, pitch: -0.1 },   // Sacral: moderate, slightly deeper
      3: { rate: 0.05, pitch: 0.0 },   // Solar: slightly faster, neutral
      4: { rate: 0.0, pitch: 0.1 },    // Heart: balanced, slightly higher
      5: { rate: 0.1, pitch: 0.15 },   // Throat: faster, clearer
      6: { rate: 0.05, pitch: 0.2 },   // Third Eye: moderate, ethereal
      7: { rate: -0.05, pitch: 0.25 }  // Crown: slower, transcendent
    };

    const mod = chakraModulation[chakraId] || { rate: 0, pitch: 0 };

    return {
      rate: Math.max(0.5, Math.min(2.0, base.rate + mod.rate)),
      pitch: Math.max(0.5, Math.min(2.0, base.pitch + mod.pitch)),
      volume: base.volume
    };
  }

  /**
   * Get available voices
   */
  getAvailableVoices(): SpeechSynthesisVoice[] {
    return this.voices;
  }
}

// Global voice interface instance
export const voiceInterface = new VoiceInterface();

// Type declarations for Web Speech API
declare global {
  interface Window {
    SpeechRecognition: typeof SpeechRecognition;
    webkitSpeechRecognition: typeof SpeechRecognition;
  }
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  onresult: ((event: SpeechRecognitionEvent) => void) | null;
  onerror: ((event: SpeechRecognitionErrorEvent) => void) | null;
  onend: (() => void) | null;
  start(): void;
  stop(): void;
}

interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList;
}

interface SpeechRecognitionResultList {
  length: number;
  item(index: number): SpeechRecognitionResult;
  [index: number]: SpeechRecognitionResult;
}

interface SpeechRecognitionResult {
  isFinal: boolean;
  length: number;
  item(index: number): SpeechRecognitionAlternative;
  [index: number]: SpeechRecognitionAlternative;
}

interface SpeechRecognitionAlternative {
  transcript: string;
  confidence: number;
}

interface SpeechRecognitionErrorEvent extends Event {
  error: string;
  message: string;
}

declare var SpeechRecognition: {
  prototype: SpeechRecognition;
  new(): SpeechRecognition;
};
