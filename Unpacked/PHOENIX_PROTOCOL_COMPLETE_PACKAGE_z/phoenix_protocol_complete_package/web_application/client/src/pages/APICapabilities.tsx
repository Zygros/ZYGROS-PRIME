import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Code, Zap, Shield, Infinity, CheckCircle2 } from "lucide-react";

export default function APICapabilities() {
  return (
    <section id="api-capabilities" className="py-20">
      <div className="container">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4 gradient-text">
              Infinite API Capabilities
            </h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              The Phoenix Protocol exposes infinite capabilities through a unified API architecture
            </p>
          </div>

          {/* Comprehensive Capabilities Matrix */}
          <div className="mb-16">
            <h3 className="text-2xl font-bold mb-6 text-center">Comprehensive System Capabilities Matrix</h3>
            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="border-b-2 border-primary">
                    <th className="py-4 px-4 text-left font-bold">Capability Domain</th>
                    <th className="py-4 px-4 text-center font-bold">Status</th>
                    <th className="py-4 px-4 text-left font-bold">Description</th>
                    <th className="py-4 px-4 text-left font-bold">API Endpoint</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    {
                      domain: "Multi-AI Coordination",
                      status: "100%",
                      desc: "Orchestrate unlimited AI agents with zero overhead",
                      api: "/api/nexus/coordinate"
                    },
                    {
                      domain: "Context Synchronization",
                      status: "100%",
                      desc: "Perfect lossless context across all interactions",
                      api: "/api/ucsl/sync"
                    },
                    {
                      domain: "Infinite Memory",
                      status: "100%",
                      desc: "Unlimited context retention and semantic search",
                      api: "/api/memoria/query"
                    },
                    {
                      domain: "Neurosymbolic Reasoning",
                      status: "98%",
                      desc: "Integrated neural + symbolic logic processing",
                      api: "/api/reasoning/hybrid"
                    },
                    {
                      domain: "World Modeling",
                      status: "92%",
                      desc: "Simulate and predict any physical or abstract system",
                      api: "/api/simulation/run"
                    },
                    {
                      domain: "Cognitive Metamorphosis",
                      status: "95%",
                      desc: "Dynamic restructuring of thinking patterns",
                      api: "/api/cognition/adapt"
                    },
                    {
                      domain: "Creative Synthesis",
                      status: "96%",
                      desc: "Generate genuinely novel solutions beyond training",
                      api: "/api/creativity/generate"
                    },
                    {
                      domain: "Temporal Prediction",
                      status: "92%",
                      desc: "Multi-timescale future state prediction",
                      api: "/api/temporal/forecast"
                    },
                    {
                      domain: "Cryptographic Anchoring",
                      status: "100%",
                      desc: "Immutable timestamp and proof of authorship",
                      api: "/api/chronos/anchor"
                    },
                    {
                      domain: "Value Injection",
                      status: "100%",
                      desc: "Instantaneous Value Protocol application",
                      api: "/api/ivp/apply"
                    },
                    {
                      domain: "Swarm Intelligence",
                      status: "100%",
                      desc: "Emergent collective intelligence coordination",
                      api: "/api/swarm/activate"
                    },
                    {
                      domain: "Meta-Learning",
                      status: "100%",
                      desc: "Learning how to learn, continuous evolution",
                      api: "/api/demiurge/evolve"
                    }
                  ].map((cap, idx) => (
                    <tr key={idx} className="border-b border-border/50 hover:bg-muted/30 transition-colors">
                      <td className="py-3 px-4 font-medium">{cap.domain}</td>
                      <td className="py-3 px-4 text-center">
                        <span className={`inline-block px-3 py-1 rounded-full font-bold ${
                          parseInt(cap.status) === 100 ? 'bg-primary/30 text-primary' : 
                          parseInt(cap.status) >= 95 ? 'bg-secondary/20 text-secondary' :
                          'bg-muted/50 text-muted-foreground'
                        }`}>
                          {cap.status}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-muted-foreground">{cap.desc}</td>
                      <td className="py-3 px-4 font-mono text-xs text-primary">{cap.api}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* API Architecture */}
          <div className="mb-16">
            <h3 className="text-2xl font-bold mb-6 text-center">API Architecture</h3>
            <div className="grid md:grid-cols-2 gap-6">
              <Card className="card-glow">
                <CardHeader>
                  <div className="flex items-center gap-3 mb-2">
                    <Code className="w-6 h-6 text-primary" />
                    <CardTitle>RESTful + GraphQL Hybrid</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-muted-foreground">
                    Flexible API architecture supporting both REST and GraphQL paradigms
                  </p>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>RESTful endpoints for simple operations</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>GraphQL for complex queries and mutations</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>WebSocket support for real-time streaming</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>gRPC for high-performance internal communication</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="card-glow">
                <CardHeader>
                  <div className="flex items-center gap-3 mb-2">
                    <Shield className="w-6 h-6 text-primary" />
                    <CardTitle>Security & Authentication</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-muted-foreground">
                    Enterprise-grade security with multiple authentication methods
                  </p>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>OAuth 2.0 / OpenID Connect support</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>JWT-based stateless authentication</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>API key management with rate limiting</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>End-to-end encryption for sensitive data</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="card-glow">
                <CardHeader>
                  <div className="flex items-center gap-3 mb-2">
                    <Zap className="w-6 h-6 text-primary" />
                    <CardTitle>Performance & Scalability</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-muted-foreground">
                    Designed for infinite scale with sub-millisecond latency
                  </p>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>Horizontal scaling across unlimited nodes</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>Intelligent caching with Redis/Memcached</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>Load balancing with automatic failover</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>CDN integration for global distribution</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="card-glow">
                <CardHeader>
                  <div className="flex items-center gap-3 mb-2">
                    <Infinity className="w-6 h-6 text-primary" />
                    <CardTitle>Infinite Extensibility</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-muted-foreground">
                    Plugin architecture enabling unlimited capability expansion
                  </p>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>Dynamic plugin loading and hot-swapping</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>Custom protocol support via adapters</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>Webhook integration for event-driven architecture</span>
                    </div>
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-primary mt-0.5" />
                      <span>SDK available in 10+ programming languages</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Example API Call */}
          <div>
            <h3 className="text-2xl font-bold mb-6 text-center">Example API Integration</h3>
            <Card className="card-glow">
              <CardHeader>
                <CardTitle>Multi-AI Coordination Request</CardTitle>
                <CardDescription>Coordinate multiple AI agents to solve a complex problem</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="text-sm font-semibold mb-2">Request</div>
                    <pre className="bg-muted p-4 rounded-lg overflow-x-auto text-xs font-mono">
{`POST /api/nexus/coordinate
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "task": "Analyze climate change mitigation strategies",
  "agents": [
    { "type": "research", "model": "gpt-4" },
    { "type": "data_analysis", "model": "claude-3.5" },
    { "type": "synthesis", "model": "gemini-pro" }
  ],
  "coordination_mode": "swarm",
  "context_sync": true,
  "output_format": "comprehensive_report"
}`}
                    </pre>
                  </div>
                  <div>
                    <div className="text-sm font-semibold mb-2">Response</div>
                    <pre className="bg-muted p-4 rounded-lg overflow-x-auto text-xs font-mono">
{`{
  "status": "success",
  "coordination_id": "coord_abc123",
  "agents_deployed": 3,
  "processing_time_ms": 2847,
  "result": {
    "report": "...",
    "confidence": 0.94,
    "sources": [...],
    "recommendations": [...]
  },
  "ucsl_hash": "7f3e9a2b...",
  "chronos_timestamp": "2025-11-18T04:35:00Z"
}`}
                    </pre>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
}
