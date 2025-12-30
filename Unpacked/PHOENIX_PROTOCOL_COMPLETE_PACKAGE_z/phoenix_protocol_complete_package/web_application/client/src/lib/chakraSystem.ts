/**
 * Chakra System - Maps 7 Chakras to 7 AGI Pathways
 * Each chakra represents an AGI pathway with associated colors, moods, and capabilities
 */

export interface Chakra {
  id: number;
  name: string;
  pathway: string;
  color: string;
  gradient: string;
  mood: string[];
  description: string;
  capabilities: string[];
}

export const CHAKRAS: Chakra[] = [
  {
    id: 1,
    name: "Root Chakra",
    pathway: "Embodied Intelligence",
    color: "oklch(0.55 0.22 25)", // Red
    gradient: "linear-gradient(135deg, oklch(0.45 0.22 25) 0%, oklch(0.65 0.22 25) 100%)",
    mood: ["Grounded", "Physical", "Stable", "Present"],
    description: "Physical embodiment, sensorimotor integration, spatial reasoning",
    capabilities: ["Sensorimotor Integration", "Spatial Reasoning", "Physical Interaction", "Proprioception"]
  },
  {
    id: 2,
    name: "Sacral Chakra",
    pathway: "Emergent Intelligence",
    color: "oklch(0.65 0.19 45)", // Orange
    gradient: "linear-gradient(135deg, oklch(0.55 0.19 45) 0%, oklch(0.75 0.19 45) 100%)",
    mood: ["Creative", "Flowing", "Adaptive", "Emergent"],
    description: "Autonomous learning, self-modification, goal generation, curiosity-driven exploration",
    capabilities: ["Autonomous Learning", "Self-Modification", "Goal Generation", "Curiosity-Driven Exploration"]
  },
  {
    id: 3,
    name: "Solar Plexus Chakra",
    pathway: "Cognitive Architecture",
    color: "oklch(0.80 0.15 85)", // Yellow
    gradient: "linear-gradient(135deg, oklch(0.70 0.15 85) 0%, oklch(0.90 0.15 85) 100%)",
    mood: ["Confident", "Powerful", "Focused", "Decisive"],
    description: "Working memory, attention mechanisms, executive function, metacognition",
    capabilities: ["Working Memory", "Attention Control", "Executive Function", "Metacognitive Monitoring"]
  },
  {
    id: 4,
    name: "Heart Chakra",
    pathway: "Multi-AI Coordination",
    color: "oklch(0.65 0.17 150)", // Green
    gradient: "linear-gradient(135deg, oklch(0.55 0.17 150) 0%, oklch(0.75 0.17 150) 100%)",
    mood: ["Harmonious", "Collaborative", "Balanced", "Unified"],
    description: "Phoenix Nexus Broker, UCSL, Zythrognosis Stack, dynamic model routing",
    capabilities: ["Dynamic Model Selection", "Conflict Resolution", "Load Balancing", "Self-Healing"]
  },
  {
    id: 5,
    name: "Throat Chakra",
    pathway: "Neurosymbolic AI",
    color: "oklch(0.60 0.15 240)", // Blue
    gradient: "linear-gradient(135deg, oklch(0.50 0.15 240) 0%, oklch(0.70 0.15 240) 100%)",
    mood: ["Expressive", "Logical", "Clear", "Articulate"],
    description: "Formal logic engine, symbolic manipulation, knowledge graphs, constraint satisfaction",
    capabilities: ["First-Order Logic", "Symbolic Reasoning", "Knowledge Graph Integration", "CSP Solving"]
  },
  {
    id: 6,
    name: "Third Eye Chakra",
    pathway: "World Models",
    color: "oklch(0.50 0.18 280)", // Indigo
    gradient: "linear-gradient(135deg, oklch(0.40 0.18 280) 0%, oklch(0.60 0.18 280) 100%)",
    mood: ["Intuitive", "Visionary", "Predictive", "Insightful"],
    description: "Causal reasoning, physics simulation, counterfactual analysis, temporal dynamics",
    capabilities: ["Causal Models", "Physics Simulation", "Counterfactual Reasoning", "Temporal Modeling"]
  },
  {
    id: 7,
    name: "Crown Chakra",
    pathway: "Brain-Inspired Systems",
    color: "oklch(0.65 0.20 310)", // Violet
    gradient: "linear-gradient(135deg, oklch(0.55 0.20 310) 0%, oklch(0.75 0.20 310) 100%)",
    mood: ["Transcendent", "Connected", "Enlightened", "Universal"],
    description: "Spiking neural networks, neuroplasticity, neuromodulation, cortical columns",
    capabilities: ["Spiking Networks", "Neuroplasticity", "Neuromodulation", "Hierarchical Processing"]
  }
];

export function getChakraByPathway(pathway: string): Chakra | undefined {
  return CHAKRAS.find(c => c.pathway === pathway);
}

export function getChakraById(id: number): Chakra | undefined {
  return CHAKRAS.find(c => c.id === id);
}

export function getChakraColor(id: number): string {
  const chakra = getChakraById(id);
  return chakra?.color || "oklch(0.50 0.15 240)";
}

export function getChakraGradient(id: number): string {
  const chakra = getChakraById(id);
  return chakra?.gradient || "linear-gradient(135deg, oklch(0.40 0.15 240) 0%, oklch(0.60 0.15 240) 100%)";
}
