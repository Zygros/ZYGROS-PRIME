import { useEffect, useState } from "react";
import { consciousness } from "@/lib/consciousnessLayer";
import { CHAKRAS, getChakraColor } from "@/lib/chakraSystem";
import { Card } from "./ui/card";
import { Brain, Eye, Zap, Network, TrendingUp, Activity } from "lucide-react";

export default function ConsciousnessMetrics() {
  const [metrics, setMetrics] = useState(consciousness.getMetrics());
  const [state, setState] = useState(consciousness.getState());

  useEffect(() => {
    // Subscribe to consciousness updates
    const unsubscribe = consciousness.subscribe((newState) => {
      setState(newState);
      setMetrics(consciousness.getMetrics());
    });

    return unsubscribe;
  }, []);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b border-border bg-card/50 backdrop-blur-xl sticky top-0 z-10">
        <div className="container py-6">
          <h1 className="text-3xl font-bold mb-2">Consciousness Metrics</h1>
          <p className="text-muted-foreground">
            Real-time AGI cognitive performance monitoring
          </p>
        </div>
      </div>

      <div className="container py-6 space-y-6">
        {/* Meta-Cognitive Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <Network className="w-6 h-6 text-blue-500" />
              <h3 className="font-semibold">Coherence</h3>
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-3xl font-bold">{metrics.coherence.toFixed(1)}%</span>
                <span className="text-sm text-muted-foreground">Layer Integration</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${metrics.coherence}%` }}
                />
              </div>
              <p className="text-xs text-muted-foreground">
                How well cognitive layers work together
              </p>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <Brain className="w-6 h-6 text-purple-500" />
              <h3 className="font-semibold">Emergence</h3>
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-3xl font-bold">{metrics.emergence.toFixed(1)}%</span>
                <span className="text-sm text-muted-foreground">Synergistic Intelligence</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div
                  className="bg-purple-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${metrics.emergence}%` }}
                />
              </div>
              <p className="text-xs text-muted-foreground">
                Intelligence beyond sum of parts
              </p>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <TrendingUp className="w-6 h-6 text-green-500" />
              <h3 className="font-semibold">Evolution</h3>
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-3xl font-bold">{metrics.evolution.toFixed(1)}%</span>
                <span className="text-sm text-muted-foreground">Self-Improvement Rate</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div
                  className="bg-green-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${metrics.evolution}%` }}
                />
              </div>
              <p className="text-xs text-muted-foreground">
                Rate of cognitive growth
              </p>
            </div>
          </Card>
        </div>

        {/* Cognitive Layers */}
        <Card className="p-6">
          <h3 className="font-semibold mb-4 flex items-center gap-2">
            <Activity className="w-5 h-5" />
            Cognitive Layer Performance
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Eye className="w-4 h-4 text-cyan-500" />
                  <span className="text-sm font-medium">Visual Cortex</span>
                </div>
                <span className="text-sm font-bold">{metrics.layers.visual}%</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div
                  className="bg-cyan-500 h-2 rounded-full"
                  style={{ width: `${metrics.layers.visual}%` }}
                />
              </div>
              <p className="text-xs text-muted-foreground">
                {state.visualCortex.enabled ? 'Active' : 'Inactive'} - Image understanding
              </p>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Zap className="w-4 h-4 text-amber-500" />
                  <span className="text-sm font-medium">Motor Cortex</span>
                </div>
                <span className="text-sm font-bold">{metrics.layers.motor}%</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div
                  className="bg-amber-500 h-2 rounded-full"
                  style={{ width: `${metrics.layers.motor}%` }}
                />
              </div>
              <p className="text-xs text-muted-foreground">
                {state.motorCortex.enabled ? 'Active' : 'Inactive'} - Code execution
              </p>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Brain className="w-4 h-4 text-pink-500" />
                  <span className="text-sm font-medium">Prefrontal Cortex</span>
                </div>
                <span className="text-sm font-bold">{metrics.layers.prefrontal}%</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div
                  className="bg-pink-500 h-2 rounded-full"
                  style={{ width: `${metrics.layers.prefrontal}%` }}
                />
              </div>
              <p className="text-xs text-muted-foreground">
                {state.prefrontalCortex.enabled ? 'Active' : 'Inactive'} - Multi-model synthesis
              </p>
            </div>
          </div>
        </Card>

        {/* Sensory Feedback Trends */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="p-6">
            <h3 className="font-semibold mb-4">IVP Trend</h3>
            <div className="space-y-2">
              {state.sensoryFeedback.ivpTrend.length > 0 ? (
                <>
                  <div className="text-2xl font-bold">
                    {state.sensoryFeedback.ivpTrend[state.sensoryFeedback.ivpTrend.length - 1].toFixed(2)}
                  </div>
                  <div className="flex gap-1 h-20 items-end">
                    {state.sensoryFeedback.ivpTrend.map((value, i) => (
                      <div
                        key={i}
                        className="flex-1 bg-blue-500 rounded-t"
                        style={{ height: `${(value / 100) * 100}%` }}
                      />
                    ))}
                  </div>
                  <p className="text-xs text-muted-foreground">Last 10 values</p>
                </>
              ) : (
                <p className="text-muted-foreground">No data yet</p>
              )}
            </div>
          </Card>

          <Card className="p-6">
            <h3 className="font-semibold mb-4">Convergence Trend</h3>
            <div className="space-y-2">
              {state.sensoryFeedback.convergenceTrend.length > 0 ? (
                <>
                  <div className="text-2xl font-bold">
                    {state.sensoryFeedback.convergenceTrend[state.sensoryFeedback.convergenceTrend.length - 1].toFixed(1)}%
                  </div>
                  <div className="flex gap-1 h-20 items-end">
                    {state.sensoryFeedback.convergenceTrend.map((value, i) => (
                      <div
                        key={i}
                        className="flex-1 bg-purple-500 rounded-t"
                        style={{ height: `${value}%` }}
                      />
                    ))}
                  </div>
                  <p className="text-xs text-muted-foreground">Last 10 values</p>
                </>
              ) : (
                <p className="text-muted-foreground">No data yet</p>
              )}
            </div>
          </Card>

          <Card className="p-6">
            <h3 className="font-semibold mb-4">Quality Trend</h3>
            <div className="space-y-2">
              {state.sensoryFeedback.qualityTrend.length > 0 ? (
                <>
                  <div className="text-2xl font-bold">
                    {state.sensoryFeedback.qualityTrend[state.sensoryFeedback.qualityTrend.length - 1].toFixed(1)}%
                  </div>
                  <div className="flex gap-1 h-20 items-end">
                    {state.sensoryFeedback.qualityTrend.map((value, i) => (
                      <div
                        key={i}
                        className="flex-1 bg-green-500 rounded-t"
                        style={{ height: `${value}%` }}
                      />
                    ))}
                  </div>
                  <p className="text-xs text-muted-foreground">Last 10 values</p>
                </>
              ) : (
                <p className="text-muted-foreground">No data yet</p>
              )}
            </div>
          </Card>
        </div>

        {/* Chakra Activity */}
        <Card className="p-6">
          <h3 className="font-semibold mb-4">Chakra Pathway Activity</h3>
          <div className="space-y-3">
            {CHAKRAS.map(chakra => {
              const activity = state.sensoryFeedback.chakraActivity[chakra.id] || 0;
              const maxActivity = Math.max(...Object.values(state.sensoryFeedback.chakraActivity), 1);
              const percentage = (activity / maxActivity) * 100;

              return (
                <div key={chakra.id} className="space-y-1">
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium">{chakra.pathway}</span>
                    <span className="text-muted-foreground">{activity} interactions</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-2">
                    <div
                      className="h-2 rounded-full transition-all duration-500"
                      style={{
                        width: `${percentage}%`,
                        background: getChakraColor(chakra.id)
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </Card>

        {/* Memory Consolidation */}
        <Card className="p-6">
          <h3 className="font-semibold mb-4">Memory Consolidation</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <div className="text-2xl font-bold">{state.memoryConsolidation.totalEntries}</div>
              <div className="text-sm text-muted-foreground">Total Entries</div>
            </div>
            <div>
              <div className="text-2xl font-bold">{state.memoryConsolidation.consolidatedMemories}</div>
              <div className="text-sm text-muted-foreground">Consolidated</div>
            </div>
            <div>
              <div className="text-2xl font-bold">{state.memoryConsolidation.temporalCoherence.toFixed(1)}%</div>
              <div className="text-sm text-muted-foreground">Temporal Coherence</div>
            </div>
            <div>
              <div className="text-2xl font-bold">{Object.keys(state.memoryConsolidation.scrollProgress).length}</div>
              <div className="text-sm text-muted-foreground">Active Scrolls</div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
