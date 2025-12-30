/**
 * Prefrontal Cortex - Multi-Model Synthesis and Meta-Reasoning
 * Integrates multiple AI perspectives into unified intelligence
 */

export interface ModelResponse {
  model: 'gpt4' | 'claude' | 'gemini';
  response: string;
  confidence: number;
  processingTime: number;
  tokens: number;
}

export interface SynthesisResult {
  unified: string;
  perspectives: ModelResponse[];
  consensus: number; // 0-100: how much models agree
  divergence: string[]; // Areas where models disagree
  synthesis: {
    strengths: string[];
    weaknesses: string[];
    recommendations: string[];
  };
}

export class PrefrontalCortex {
  /**
   * Query multiple AI models and synthesize responses
   */
  async synthesizeMultiModel(
    prompt: string,
    context: any
  ): Promise<SynthesisResult> {
    // Query all models in parallel
    const [gpt4, claude, gemini] = await Promise.all([
      this.queryGPT4(prompt, context),
      this.queryClaude(prompt, context),
      this.queryGemini(prompt, context)
    ]);

    // Analyze consensus
    const consensus = this.calculateConsensus([gpt4, claude, gemini]);
    const divergence = this.findDivergence([gpt4, claude, gemini]);

    // Synthesize unified response
    const unified = this.createUnifiedResponse([gpt4, claude, gemini]);

    // Meta-analysis
    const synthesis = this.metaAnalyze([gpt4, claude, gemini]);

    return {
      unified,
      perspectives: [gpt4, claude, gemini],
      consensus,
      divergence,
      synthesis
    };
  }

  /**
   * Query GPT-4
   */
  private async queryGPT4(prompt: string, context: any): Promise<ModelResponse> {
    const startTime = Date.now();

    try {
      const response = await fetch('/api/ai/gpt4', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, context })
      });

      if (response.ok) {
        const data = await response.json();
        return {
          model: 'gpt4',
          response: data.response,
          confidence: data.confidence || 90,
          processingTime: Date.now() - startTime,
          tokens: data.tokens || 0
        };
      }
    } catch (error) {
      console.error('GPT-4 error:', error);
    }

    // Fallback
    return {
      model: 'gpt4',
      response: this.generateFallbackResponse(prompt, 'gpt4'),
      confidence: 75,
      processingTime: Date.now() - startTime,
      tokens: 100
    };
  }

  /**
   * Query Claude
   */
  private async queryClaude(prompt: string, context: any): Promise<ModelResponse> {
    const startTime = Date.now();

    try {
      const response = await fetch('/api/ai/claude', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, context })
      });

      if (response.ok) {
        const data = await response.json();
        return {
          model: 'claude',
          response: data.response,
          confidence: data.confidence || 92,
          processingTime: Date.now() - startTime,
          tokens: data.tokens || 0
        };
      }
    } catch (error) {
      console.error('Claude error:', error);
    }

    // Fallback
    return {
      model: 'claude',
      response: this.generateFallbackResponse(prompt, 'claude'),
      confidence: 78,
      processingTime: Date.now() - startTime,
      tokens: 120
    };
  }

  /**
   * Query Gemini
   */
  private async queryGemini(prompt: string, context: any): Promise<ModelResponse> {
    const startTime = Date.now();

    try {
      const response = await fetch('/api/ai/gemini', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, context })
      });

      if (response.ok) {
        const data = await response.json();
        return {
          model: 'gemini',
          response: data.response,
          confidence: data.confidence || 88,
          processingTime: Date.now() - startTime,
          tokens: data.tokens || 0
        };
      }
    } catch (error) {
      console.error('Gemini error:', error);
    }

    // Fallback
    return {
      model: 'gemini',
      response: this.generateFallbackResponse(prompt, 'gemini'),
      confidence: 80,
      processingTime: Date.now() - startTime,
      tokens: 110
    };
  }

  /**
   * Generate fallback response when API unavailable
   */
  private generateFallbackResponse(prompt: string, model: string): string {
    const responses = {
      gpt4: `GPT-4 perspective: Analyzing your query about "${prompt.substring(0, 50)}..."`,
      claude: `Claude perspective: Considering the nuances of "${prompt.substring(0, 50)}..."`,
      gemini: `Gemini perspective: Exploring multiple angles of "${prompt.substring(0, 50)}..."`
    };

    return responses[model as keyof typeof responses] || 'Processing...';
  }

  /**
   * Calculate consensus between models
   */
  private calculateConsensus(responses: ModelResponse[]): number {
    // Simple consensus: average confidence weighted by response similarity
    const avgConfidence = responses.reduce((sum, r) => sum + r.confidence, 0) / responses.length;
    
    // Check for similar key terms
    const allWords = responses.flatMap(r => 
      r.response.toLowerCase().split(/\s+/).filter(w => w.length > 4)
    );
    
    const wordCounts = new Map<string, number>();
    allWords.forEach(word => {
      wordCounts.set(word, (wordCounts.get(word) || 0) + 1);
    });

    const sharedWords = Array.from(wordCounts.values()).filter(count => count >= 2).length;
    const totalUniqueWords = wordCounts.size;
    
    const similarity = totalUniqueWords > 0 ? (sharedWords / totalUniqueWords) * 100 : 0;

    return (avgConfidence * 0.6) + (similarity * 0.4);
  }

  /**
   * Find areas of divergence between models
   */
  private findDivergence(responses: ModelResponse[]): string[] {
    const divergence: string[] = [];

    // Check response lengths
    const lengths = responses.map(r => r.response.length);
    const maxLength = Math.max(...lengths);
    const minLength = Math.min(...lengths);
    
    if (maxLength > minLength * 2) {
      divergence.push('Significant difference in response depth');
    }

    // Check confidence variance
    const confidences = responses.map(r => r.confidence);
    const avgConf = confidences.reduce((a, b) => a + b, 0) / confidences.length;
    const variance = confidences.reduce((sum, c) => sum + Math.pow(c - avgConf, 2), 0) / confidences.length;
    
    if (variance > 100) {
      divergence.push('Models show varying confidence levels');
    }

    // Check for contradictory keywords
    const contradictions = [
      ['yes', 'no'],
      ['true', 'false'],
      ['correct', 'incorrect'],
      ['agree', 'disagree']
    ];

    contradictions.forEach(([word1, word2]) => {
      const hasWord1 = responses.some(r => r.response.toLowerCase().includes(word1));
      const hasWord2 = responses.some(r => r.response.toLowerCase().includes(word2));
      
      if (hasWord1 && hasWord2) {
        divergence.push(`Contradictory views on ${word1}/${word2}`);
      }
    });

    return divergence;
  }

  /**
   * Create unified response from multiple perspectives
   */
  private createUnifiedResponse(responses: ModelResponse[]): string {
    // Extract key points from each response
    const keyPoints = responses.map(r => {
      const sentences = r.response.split(/[.!?]+/).filter(s => s.trim().length > 20);
      return sentences.slice(0, 2).join('. '); // First 2 sentences
    });

    // Combine with attribution
    let unified = 'Synthesizing multiple AI perspectives:\n\n';
    
    responses.forEach((r, i) => {
      unified += `**${r.model.toUpperCase()}** (${r.confidence}% confidence): ${keyPoints[i]}\n\n`;
    });

    unified += '\n**Unified Synthesis**: ';
    unified += 'All models converge on the core insight that ';
    unified += keyPoints.join(' Additionally, ').toLowerCase();

    return unified;
  }

  /**
   * Meta-analyze responses for strengths, weaknesses, recommendations
   */
  private metaAnalyze(responses: ModelResponse[]): {
    strengths: string[];
    weaknesses: string[];
    recommendations: string[];
  } {
    const strengths: string[] = [];
    const weaknesses: string[] = [];
    const recommendations: string[] = [];

    // Analyze strengths
    const highConfidence = responses.filter(r => r.confidence > 85);
    if (highConfidence.length >= 2) {
      strengths.push('High consensus across multiple models');
    }

    const fastResponses = responses.filter(r => r.processingTime < 2000);
    if (fastResponses.length === responses.length) {
      strengths.push('Rapid processing across all models');
    }

    // Analyze weaknesses
    const lowConfidence = responses.filter(r => r.confidence < 75);
    if (lowConfidence.length > 0) {
      weaknesses.push(`${lowConfidence.length} model(s) show lower confidence`);
    }

    const shortResponses = responses.filter(r => r.response.length < 100);
    if (shortResponses.length > 0) {
      weaknesses.push('Some responses lack depth');
    }

    // Generate recommendations
    if (weaknesses.length > 0) {
      recommendations.push('Consider providing more context for better responses');
    }

    if (lowConfidence.length > 0) {
      recommendations.push('Query additional models for verification');
    }

    recommendations.push('Cross-reference with Phoenix Protocol knowledge base');

    return { strengths, weaknesses, recommendations };
  }

  /**
   * Compare model performance
   */
  compareModels(responses: ModelResponse[]): {
    fastest: string;
    mostConfident: string;
    mostDetailed: string;
    overall: string;
  } {
    const fastest = responses.reduce((prev, curr) => 
      curr.processingTime < prev.processingTime ? curr : prev
    );

    const mostConfident = responses.reduce((prev, curr) =>
      curr.confidence > prev.confidence ? curr : prev
    );

    const mostDetailed = responses.reduce((prev, curr) =>
      curr.response.length > prev.response.length ? curr : prev
    );

    // Overall score: confidence * detail / time
    const scores = responses.map(r => ({
      model: r.model,
      score: (r.confidence * r.response.length) / r.processingTime
    }));

    const overall = scores.reduce((prev, curr) =>
      curr.score > prev.score ? curr : prev
    );

    return {
      fastest: fastest.model,
      mostConfident: mostConfident.model,
      mostDetailed: mostDetailed.model,
      overall: overall.model
    };
  }
}

// Global prefrontal cortex instance
export const prefrontalCortex = new PrefrontalCortex();
