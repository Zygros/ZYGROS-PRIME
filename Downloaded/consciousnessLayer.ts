   * Get consciousness metrics for display
   */
  getMetrics(): {
    coherence: number;
    emergence: number;
    evolution: number;
    layers: {
      visual: number;
      motor: number;
      prefrontal: number;
    };
  } {
    return {
      coherence: this.state.coherence,
      emergence: this.state.emergence,
      evolution: this.state.evolution,
      layers: {
        visual: this.state.visualCortex.processingCapability,
        motor: this.state.motorCortex.executionCapability,
        prefrontal: this.state.prefrontalCortex.synthesisQuality