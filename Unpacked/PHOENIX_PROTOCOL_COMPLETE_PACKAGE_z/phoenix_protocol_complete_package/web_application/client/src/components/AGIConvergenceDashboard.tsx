import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Brain, Network, Zap, TrendingUp, Activity, CheckCircle2 } from "lucide-react";
import { CHAKRAS } from "@/lib/chakraSystem";
import { memoriaOmnia } from "@/lib/infiniteScroll";
import { ucsl } from "@/lib/protocols";

interface PathwayMetrics {
  id: number;
  name: string;
  convergence: number;
  activity: number;
  trend: "up" | "stable" | "down";
}

export default function AGIConvergenceDashboard() {
  const [pathwayMetrics, setPathwayMetrics] = useState<PathwayMetrics[]>([]);
  const [overallConvergence, setOverallConvergence] = useState(0);
  const [totalMessages, setTotalMessages] = useState(0);
  const [systemHealth, setSystemHealth] = useState(100);

  useEffect(() => {
    // Calculate metrics from Memoria Omnia
    const messages = memoriaOmnia.getRecent(100);
    setTotalMessages(memoriaOmnia.getCount());

    // Calculate pathway-specific metrics
    const metrics: PathwayMetrics[] = CHAKRAS.map(chakra => {
      const chakraMessages = messages.filter(m => m.chakraId === chakra.id);
      const activity = (chakraMessages.length / messages.length) * 100 || 0;
      
      // Calculate convergence based on IVP values
      const avgIVP = chakraMessages.reduce((sum, m) => sum + (m.metadata?.ivpValue || 0), 0) / chakraMessages.length || 0;
      const convergence = Math.min(100, (avgIVP / 100) * 100);

      return {
        id: chakra.id,
        name: chakra.name,
        convergence: Math.round(convergence),
        activity: Math.round(activity),
        trend: activity > 15 ? "up" : activity > 5 ? "stable" : "down"
      };
    });

    setPathwayMetrics(metrics);

    // Calculate overall convergence
    const avgConvergence = metrics.reduce((sum, m) => sum + m.convergence, 0) / metrics.length;
    setOverallConvergence(Math.round(avgConvergence));

    // System health based on UCSL version and activity
    const ucslVersion = ucsl.getVersion();
    const healthScore = Math.min(100, 80 + (ucslVersion) + (messages.length > 0 ? 10 : 0));
    setSystemHealth(Math.round(healthScore));
  }, []);

  const getConvergenceColor = (value: number) => {
    if (value >= 90) return "text-green-400";
    if (value >= 70) return "text-blue-400";
    if (value >= 50) return "text-yellow-400";
    return "text-orange-400";
  };

  const getTrendIcon = (trend: "up" | "stable" | "down") => {
    if (trend === "up") return "↗";
    if (trend === "stable") return "→";
    return "↘";
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-black py-20">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-green-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
            AGI Convergence Dashboard
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Real-time metrics across all 7 AGI pathways
          </p>
        </div>

        {/* Overall Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12 max-w-6xl mx-auto">
          <Card className="bg-gray-900/50 border-gray-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm text-gray-400 flex items-center gap-2">
                <Brain className="w-4 h-4" />
                Overall Convergence
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className={`text-4xl font-bold ${getConvergenceColor(overallConvergence)}`}>
                {overallConvergence}%
              </div>
              <Progress value={overallConvergence} className="mt-2" />
            </CardContent>
          </Card>

          <Card className="bg-gray-900/50 border-gray-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm text-gray-400 flex items-center gap-2">
                <Activity className="w-4 h-4" />
                System Health
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-green-400">
                {systemHealth}%
              </div>
              <Progress value={systemHealth} className="mt-2" />
            </CardContent>
          </Card>

          <Card className="bg-gray-900/50 border-gray-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm text-gray-400 flex items-center gap-2">
                <Network className="w-4 h-4" />
                Active Pathways
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-blue-400">
                {pathwayMetrics.filter(p => p.activity > 0).length}/7
              </div>
              <div className="text-xs text-gray-500 mt-2">
                {pathwayMetrics.filter(p => p.convergence >= 70).length} converged
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gray-900/50 border-gray-700">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm text-gray-400 flex items-center gap-2">
                <Zap className="w-4 h-4" />
                Total Messages
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-purple-400">
                {totalMessages}
              </div>
              <div className="text-xs text-gray-500 mt-2">
                UCSL v{ucsl.getVersion()}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Pathway Metrics */}
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold text-white mb-6">7 AGI Pathways</h2>
          <div className="grid grid-cols-1 gap-4">
            {pathwayMetrics.map((metric, index) => {
              const chakra = CHAKRAS[index];
              return (
                <Card 
                  key={metric.id}
                  className="bg-gray-900/50 border-gray-700 hover:border-purple-500/50 transition-all duration-300"
                >
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div 
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: chakra.color }}
                        />
                        <div>
                          <CardTitle className="text-lg text-white">{metric.name}</CardTitle>
                          <CardDescription className="text-sm">{chakra.pathway}</CardDescription>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="text-right">
                          <div className={`text-2xl font-bold ${getConvergenceColor(metric.convergence)}`}>
                            {metric.convergence}%
                          </div>
                          <div className="text-xs text-gray-500">convergence</div>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-bold text-gray-400">
                            {metric.activity}%
                          </div>
                          <div className="text-xs text-gray-500">activity</div>
                        </div>
                        <div className="text-3xl">
                          {getTrendIcon(metric.trend)}
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-xs text-gray-400">
                        <span>Convergence Progress</span>
                        <span>{metric.convergence}%</span>
                      </div>
                      <Progress value={metric.convergence} className="h-2" />
                      
                      <div className="flex items-center justify-between text-xs text-gray-400 mt-3">
                        <span>Activity Level</span>
                        <span>{metric.activity}%</span>
                      </div>
                      <Progress value={metric.activity} className="h-2" />
                    </div>

                    {metric.convergence >= 70 && (
                      <div className="mt-4 flex items-center gap-2 text-xs text-green-400">
                        <CheckCircle2 className="w-4 h-4" />
                        <span>Pathway Converged</span>
                      </div>
                    )}
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>

        {/* System Status */}
        <div className="max-w-6xl mx-auto mt-12">
          <Card className="bg-gray-900/50 border-gray-700">
            <CardHeader>
              <CardTitle className="text-white">System Status</CardTitle>
              <CardDescription>Phoenix Protocol operational metrics</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-4 bg-gray-800/50 rounded-lg">
                  <div className="text-sm text-gray-400 mb-1">Memoria Omnia</div>
                  <Badge variant="outline" className="text-green-400 border-green-400">
                    OPERATIONAL
                  </Badge>
                </div>
                <div className="text-center p-4 bg-gray-800/50 rounded-lg">
                  <div className="text-sm text-gray-400 mb-1">IVP Calculator</div>
                  <Badge variant="outline" className="text-green-400 border-green-400">
                    OPERATIONAL
                  </Badge>
                </div>
                <div className="text-center p-4 bg-gray-800/50 rounded-lg">
                  <div className="text-sm text-gray-400 mb-1">CHRONOS KEY</div>
                  <Badge variant="outline" className="text-green-400 border-green-400">
                    OPERATIONAL
                  </Badge>
                </div>
                <div className="text-center p-4 bg-gray-800/50 rounded-lg">
                  <div className="text-sm text-gray-400 mb-1">UCSL Sync</div>
                  <Badge variant="outline" className="text-green-400 border-green-400">
                    OPERATIONAL
                  </Badge>
                </div>
                <div className="text-center p-4 bg-gray-800/50 rounded-lg">
                  <div className="text-sm text-gray-400 mb-1">Recognition</div>
                  <Badge variant="outline" className="text-green-400 border-green-400">
                    OPERATIONAL
                  </Badge>
                </div>
                <div className="text-center p-4 bg-gray-800/50 rounded-lg">
                  <div className="text-sm text-gray-400 mb-1">ZAAI System</div>
                  <Badge variant="outline" className="text-green-400 border-green-400">
                    OPERATIONAL
                  </Badge>
                </div>
                <div className="text-center p-4 bg-gray-800/50 rounded-lg">
                  <div className="text-sm text-gray-400 mb-1">12-Layer Cascade</div>
                  <Badge variant="outline" className="text-green-400 border-green-400">
                    OPERATIONAL
                  </Badge>
                </div>
                <div className="text-center p-4 bg-gray-800/50 rounded-lg">
                  <div className="text-sm text-gray-400 mb-1">Zythrognosis Stack</div>
                  <Badge variant="outline" className="text-green-400 border-green-400">
                    OPERATIONAL
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
