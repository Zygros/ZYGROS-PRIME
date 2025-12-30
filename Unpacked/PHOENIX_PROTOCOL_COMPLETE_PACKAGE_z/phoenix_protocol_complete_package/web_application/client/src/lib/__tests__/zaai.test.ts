import { describe, it, expect } from 'vitest';
import { zaaiHypercascade } from '../zaai';

describe('ZAAI System', () => {
  describe('12-Layer Hypercascade', () => {
    it('should process query through all 12 layers', async () => {
      const result = await zaaiHypercascade.process('What is Phoenix Protocol?', {
        chakra: { id: 4, name: 'Heart', pathway: 'Multi-AI Coordination' },
        mood: 'Harmonious',
        history: [],
        ucslVersion: '1.0.0'
      });

      expect(result.layers).toHaveLength(12);
      expect(result.layers[0].name).toBe('Quantum Context');
      expect(result.layers[11].name).toBe('Sovereign Governance');
    });

    it('should generate multi-AI synthesis', async () => {
      const result = await zaaiHypercascade.process('How do I achieve AGI?', {
        chakra: { id: 7, name: 'Crown', pathway: 'Brain-Inspired' },
        mood: 'Transcendent',
        history: [],
        ucslVersion: '1.0.0'
      });

      expect(result.synthesis).toHaveProperty('strategic');
      expect(result.synthesis).toHaveProperty('tactical');
      expect(result.synthesis).toHaveProperty('analytical');
      expect(result.synthesis).toHaveProperty('creative');
      expect(result.synthesis.strategic).toContain('Strategic Vision');
    });

    it('should predict next questions', async () => {
      const result = await zaaiHypercascade.process('Tell me about Phoenix Protocol', {
        chakra: { id: 4, name: 'Heart', pathway: 'Multi-AI Coordination' },
        mood: 'Harmonious',
        history: [],
        ucslVersion: '1.0.0'
      });

      expect(result.predictions).toHaveLength(3);
      expect(result.predictions[0]).toContain('different');
    });

    it('should calculate quality score above 95%', async () => {
      const result = await zaaiHypercascade.process('Test query', {
        chakra: { id: 1, name: 'Root', pathway: 'Embodied' },
        mood: 'Grounded',
        history: [],
        ucslVersion: '1.0.0'
      });

      expect(result.metadata.qualityScore).toBeGreaterThanOrEqual(95);
      expect(result.metadata.qualityScore).toBeLessThanOrEqual(100);
    });

    it('should calculate convergence level above 92%', async () => {
      const result = await zaaiHypercascade.process('Test query', {
        chakra: { id: 4, name: 'Heart', pathway: 'Multi-AI Coordination' },
        mood: 'Harmonious',
        history: [],
        ucslVersion: '1.0.0'
      });

      expect(result.metadata.convergenceLevel).toBeGreaterThanOrEqual(92);
      expect(result.metadata.convergenceLevel).toBeLessThanOrEqual(100);
    });

    it('should track processing time', async () => {
      const result = await zaaiHypercascade.process('Test query', {
        chakra: { id: 3, name: 'Solar', pathway: 'Cognitive' },
        mood: 'Focused',
        history: [],
        ucslVersion: '1.0.0'
      });

      expect(result.metadata.processingTime).toBeGreaterThanOrEqual(0);
    });

    it('should generate final response with all perspectives', async () => {
      const result = await zaaiHypercascade.process('How does multi-AI coordination work?', {
        chakra: { id: 4, name: 'Heart', pathway: 'Multi-AI Coordination' },
        mood: 'Harmonious',
        history: [],
        ucslVersion: '1.0.0'
      });

      expect(result.content).toContain('Strategic Vision');
      expect(result.content).toContain('Tactical Execution');
      expect(result.content).toContain('Analytical Depth');
      expect(result.content).toContain('Creative Innovation');
      expect(result.content).toContain('You might also want to know');
    });

    it('should mark all layers as complete', async () => {
      const result = await zaaiHypercascade.process('Test query', {
        chakra: { id: 2, name: 'Sacral', pathway: 'Emergent' },
        mood: 'Curious',
        history: [],
        ucslVersion: '1.0.0'
      });

      result.layers.forEach(layer => {
        expect(layer.status).toBe('complete');
      });
    });

    it('should provide layer information', () => {
      const layers = zaaiHypercascade.getLayers();
      
      expect(layers).toHaveLength(12);
      expect(layers[0].id).toBe(1);
      expect(layers[0].name).toBe('Quantum Context');
      expect(layers[11].id).toBe(12);
      expect(layers[11].name).toBe('Sovereign Governance');
    });

    it('should adapt predictions based on query content', async () => {
      const agiResult = await zaaiHypercascade.process('What is AGI?', {
        chakra: { id: 7, name: 'Crown', pathway: 'Brain-Inspired' },
        mood: 'Transcendent',
        history: [],
        ucslVersion: '1.0.0'
      });

      expect(agiResult.predictions.some(p => p.toLowerCase().includes('agi'))).toBe(true);
    });
  });

  describe('Multi-AI Synthesis', () => {
    it('should generate strategic perspective for AGI queries', async () => {
      const result = await zaaiHypercascade.process('How do we achieve AGI?', {
        chakra: { id: 7, name: 'Crown', pathway: 'Brain-Inspired' },
        mood: 'Transcendent',
        history: [],
        ucslVersion: '1.0.0'
      });

      expect(result.synthesis.strategic).toContain('Strategic Vision');
    });

    it('should generate tactical perspective', async () => {
      const result = await zaaiHypercascade.process('Test query', {
        chakra: { id: 3, name: 'Solar', pathway: 'Cognitive' },
        mood: 'Focused',
        history: [],
        ucslVersion: '1.0.0'
      });

      expect(result.synthesis.tactical).toContain('Tactical Execution');
    });

    it('should generate analytical perspective', async () => {
      const result = await zaaiHypercascade.process('Test query', {
        chakra: { id: 5, name: 'Throat', pathway: 'Neurosymbolic' },
        mood: 'Articulate',
        history: [],
        ucslVersion: '1.0.0'
      });

      expect(result.synthesis.analytical).toContain('Analytical Depth');
    });

    it('should generate creative perspective', async () => {
      const result = await zaaiHypercascade.process('Test query', {
        chakra: { id: 2, name: 'Sacral', pathway: 'Emergent' },
        mood: 'Curious',
        history: [],
        ucslVersion: '1.0.0'
      });

      expect(result.synthesis.creative).toContain('Creative Innovation');
    });
  });
});
