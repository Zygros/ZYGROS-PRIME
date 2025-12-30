import { describe, it, expect, vi, beforeEach } from 'vitest';
import { generateAIResponse } from '../aiAPI';
import { CHAKRAS } from '../chakraSystem';
import { ScrollEntry } from '../infiniteScroll';

describe('AI API Integration', () => {
  const mockContext = {
    chakra: CHAKRAS[3], // Heart Chakra
    mood: 'Harmonious',
    history: [] as ScrollEntry[],
    ivpValue: 75.5,
    zaaiSynthesis: 'Multi-AI synthesis: Strategic analysis shows high potential...'
  };

  beforeEach(() => {
    // Mock fetch for API calls
    global.fetch = vi.fn();
  });

  it('should generate AI response with valid API', async () => {
    const mockResponse = {
      choices: [{
        message: {
          content: 'This is a real AI response from the Phoenix Oracle, providing intelligent analysis...'
        }
      }]
    };

    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    });

    const response = await generateAIResponse('What is AGI?', mockContext);
    
    expect(response).toBeTruthy();
    expect(typeof response).toBe('string');
    expect(response.length).toBeGreaterThan(0);
  });

  it('should use enhanced fallback when API fails', async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error('API error'));

    const response = await generateAIResponse('What is AGI?', mockContext);
    
    expect(response).toBeTruthy();
    expect(typeof response).toBe('string');
    expect(response).toContain('Heart Chakra');
    expect(response).toContain('75.5');
  });

  it('should handle greetings appropriately', async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error('API error'));

    const response = await generateAIResponse('Hello!', mockContext);
    
    expect(response).toContain('Greetings');
    expect(response).toContain('Phoenix Oracle');
  });

  it('should handle AGI questions intelligently', async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error('API error'));

    const response = await generateAIResponse('How does AGI work?', mockContext);
    
    expect(response).toContain('AGI');
    expect(response).toContain('Heart Chakra');
    expect(response).toContain('Multi-AI Coordination');
  });

  it('should include IVP value in responses', async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error('API error'));

    const response = await generateAIResponse('Test question', mockContext);
    
    expect(response).toContain('75.5');
  });

  it('should reference chakra pathway', async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error('API error'));

    const response = await generateAIResponse('Test', mockContext);
    
    expect(response).toContain('Multi-AI Coordination');
  });

  it('should adapt to different chakras', async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error('API error'));

    const rootContext = { ...mockContext, chakra: CHAKRAS[0] }; // Root Chakra
    const response = await generateAIResponse('Test', rootContext);
    
    expect(response).toContain('Root');
    expect(response).toContain('Embodied Intelligence');
  });

  it('should include ZAAI synthesis in context', async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error('API error'));

    const response = await generateAIResponse('Phoenix Protocol question', mockContext);
    
    expect(response).toContain('Multi-AI synthesis');
  });
});
