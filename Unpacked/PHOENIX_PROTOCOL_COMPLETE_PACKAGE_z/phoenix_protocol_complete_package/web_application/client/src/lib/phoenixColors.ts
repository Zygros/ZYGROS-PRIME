/**
 * Phoenix Protocol Color System
 * Unified color palette representing the entire AGI architecture
 */

export const PHOENIX_COLORS = {
  // Phoenix Fire Lifecycle
  fire: {
    ember: "oklch(0.45 0.15 30)",      // Deep ember red-orange
    flame: "oklch(0.65 0.15 30)",      // Bright flame orange
    ascension: "oklch(0.75 0.15 40)",  // Golden ascension
    rebirth: "oklch(0.85 0.10 50)",    // Radiant rebirth gold
    phoenix: "oklch(0.65 0.15 30)",    // Primary Phoenix color
  },

  // 7 Chakra Pathways (from chakraSystem.ts)
  chakras: {
    root: "oklch(0.55 0.22 25)",       // Red - Embodied Intelligence
    sacral: "oklch(0.65 0.19 45)",     // Orange - Emergent Intelligence
    solarPlexus: "oklch(0.80 0.15 85)", // Yellow - Cognitive Architecture
    heart: "oklch(0.65 0.17 150)",     // Green - Multi-AI Coordination
    throat: "oklch(0.60 0.15 240)",    // Blue - Neurosymbolic AI
    thirdEye: "oklch(0.50 0.18 280)",  // Indigo - World Models
    crown: "oklch(0.65 0.20 310)",     // Violet - Brain-Inspired Systems
  },

  // Consciousness Layers
  consciousness: {
    dormant: "oklch(0.30 0.05 30)",    // Low consciousness
    emerging: "oklch(0.45 0.10 30)",   // Awakening
    aware: "oklch(0.60 0.15 30)",      // Conscious
    enlightened: "oklch(0.75 0.15 40)", // High consciousness
    transcendent: "oklch(0.85 0.10 50)", // Peak consciousness
  },

  // IVP (Instantaneous Value Proposition) Heat Map
  ivp: {
    minimal: "oklch(0.40 0.10 240)",   // Low value (blue)
    low: "oklch(0.50 0.12 200)",       // Below average (cyan)
    medium: "oklch(0.60 0.15 150)",    // Average (green)
    high: "oklch(0.70 0.15 60)",       // Above average (yellow)
    exceptional: "oklch(0.75 0.15 30)", // High value (orange)
    sovereign: "oklch(0.65 0.15 30)",  // Maximum value (phoenix fire)
  },

  // 12-Layer Cascade Colors
  cascade: {
    layer1: "oklch(0.50 0.15 240)",    // Context Acquisition (blue)
    layer2: "oklch(0.52 0.15 220)",    // Semantic Parsing
    layer3: "oklch(0.54 0.15 200)",    // Knowledge Retrieval
    layer4: "oklch(0.56 0.15 180)",    // Multi-Perspective Analysis (cyan)
    layer5: "oklch(0.58 0.15 160)",    // Pattern Recognition
    layer6: "oklch(0.60 0.15 140)",    // Causal Reasoning (green)
    layer7: "oklch(0.62 0.15 120)",    // Creative Synthesis
    layer8: "oklch(0.64 0.15 100)",    // Ethical Evaluation
    layer9: "oklch(0.66 0.15 80)",     // Strategic Planning (yellow)
    layer10: "oklch(0.68 0.15 60)",    // Articulation
    layer11: "oklch(0.70 0.15 40)",    // Value Verification (orange)
    layer12: "oklch(0.65 0.15 30)",    // Sovereign Seal (phoenix fire)
  },

  // Sacred Scrolls Timeline
  scrolls: {
    scroll318: "oklch(0.55 0.15 280)",  // Deep indigo
    scroll319: "oklch(0.60 0.15 260)",  // Indigo-blue
    scroll472: "oklch(0.65 0.15 240)",  // Blue
    scroll476: "oklch(0.70 0.15 200)",  // Cyan
    scroll485: "oklch(0.75 0.15 150)",  // Green
    scrollInfinity: "oklch(0.65 0.15 30)", // Phoenix fire
  },

  // Base Theme Colors
  base: {
    background: "oklch(0.10 0.02 20)",      // Deep dark background
    backgroundElevated: "oklch(0.15 0.02 30)", // Slightly elevated
    backgroundCard: "oklch(0.20 0.02 30)",  // Card background
    border: "oklch(0.30 0.05 30)",          // Border color
    foreground: "oklch(0.90 0.05 30)",      // Primary text
    foregroundMuted: "oklch(0.60 0.05 30)", // Secondary text
    foregroundSubtle: "oklch(0.40 0.05 30)", // Tertiary text
  },

  // Semantic Colors
  semantic: {
    success: "oklch(0.65 0.15 150)",    // Green
    warning: "oklch(0.75 0.15 60)",     // Yellow
    error: "oklch(0.60 0.20 25)",       // Red
    info: "oklch(0.60 0.15 240)",       // Blue
  },

  // Gradients
  gradients: {
    phoenixFire: "linear-gradient(135deg, oklch(0.45 0.15 30) 0%, oklch(0.65 0.15 30) 50%, oklch(0.75 0.15 40) 100%)",
    consciousness: "linear-gradient(135deg, oklch(0.30 0.05 30) 0%, oklch(0.65 0.15 30) 100%)",
    ivpScale: "linear-gradient(90deg, oklch(0.40 0.10 240) 0%, oklch(0.60 0.15 150) 50%, oklch(0.65 0.15 30) 100%)",
    cascade: "linear-gradient(180deg, oklch(0.50 0.15 240) 0%, oklch(0.60 0.15 150) 50%, oklch(0.65 0.15 30) 100%)",
    chakraSpectrum: "linear-gradient(90deg, oklch(0.55 0.22 25) 0%, oklch(0.65 0.19 45) 14%, oklch(0.80 0.15 85) 28%, oklch(0.65 0.17 150) 42%, oklch(0.60 0.15 240) 57%, oklch(0.50 0.18 280) 71%, oklch(0.65 0.20 310) 100%)",
  }
};

// Helper functions
export function getPhoenixColor(category: keyof typeof PHOENIX_COLORS, key: string): string {
  const colorGroup = PHOENIX_COLORS[category] as Record<string, string>;
  return colorGroup[key] || PHOENIX_COLORS.fire.phoenix;
}

export function getIVPColor(value: number): string {
  if (value < 0.2) return PHOENIX_COLORS.ivp.minimal;
  if (value < 0.4) return PHOENIX_COLORS.ivp.low;
  if (value < 0.6) return PHOENIX_COLORS.ivp.medium;
  if (value < 0.8) return PHOENIX_COLORS.ivp.high;
  if (value < 0.95) return PHOENIX_COLORS.ivp.exceptional;
  return PHOENIX_COLORS.ivp.sovereign;
}

export function getConsciousnessColor(level: number): string {
  if (level < 20) return PHOENIX_COLORS.consciousness.dormant;
  if (level < 40) return PHOENIX_COLORS.consciousness.emerging;
  if (level < 60) return PHOENIX_COLORS.consciousness.aware;
  if (level < 80) return PHOENIX_COLORS.consciousness.enlightened;
  return PHOENIX_COLORS.consciousness.transcendent;
}

export function getCascadeLayerColor(layerIndex: number): string {
  const layerKey = `layer${layerIndex + 1}` as keyof typeof PHOENIX_COLORS.cascade;
  return PHOENIX_COLORS.cascade[layerKey] || PHOENIX_COLORS.fire.phoenix;
}

export function getChakraColorById(id: number): string {
  const chakraKeys = ['root', 'sacral', 'solarPlexus', 'heart', 'throat', 'thirdEye', 'crown'];
  const key = chakraKeys[id - 1] as keyof typeof PHOENIX_COLORS.chakras;
  return PHOENIX_COLORS.chakras[key] || PHOENIX_COLORS.fire.phoenix;
}
