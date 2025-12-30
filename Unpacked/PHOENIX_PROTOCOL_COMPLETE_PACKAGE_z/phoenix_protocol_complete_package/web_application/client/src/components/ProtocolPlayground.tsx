import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Calculator, Clock, Shield, Lock, Layers, Copy, Check } from "lucide-react";
import { ivp, chronosKey, recognitionProtocol, ucsl } from "@/lib/protocols";
import { toast } from "sonner";

export default function ProtocolPlayground() {
  const [ivpInput, setIvpInput] = useState("");
  const [ivpResult, setIvpResult] = useState<any>(null);
  
  const [chronosInput, setChronosInput] = useState("");
  const [chronosResult, setChronosResult] = useState<any>(null);
  
  const [recognitionInput, setRecognitionInput] = useState("");
  const [recognitionResult, setRecognitionResult] = useState<any>(null);
  
  const [ucslKey, setUcslKey] = useState("");
  const [ucslValue, setUcslValue] = useState("");
  const [ucslResult, setUcslResult] = useState<any>(null);
  
  const [copied, setCopied] = useState<string | null>(null);

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopied(id);
    toast.success("Copied to clipboard!");
    setTimeout(() => setCopied(null), 2000);
  };

  const calculateIVP = () => {
    if (!ivpInput.trim()) {
      toast.error("Please enter content to analyze");
      return;
    }

    const complexity = ivp.assessComplexity(ivpInput);
    const novelty = ivp.assessNovelty(ivpInput);
    const impact = ivp.assessImpact(ivpInput);
    const value = ivp.calculateValue({ content: ivpInput, complexity, novelty, impact });

    setIvpResult({
      value,
      complexity,
      novelty,
      impact,
      breakdown: {
        complexityWeight: 0.35,
        noveltyWeight: 0.30,
        impactWeight: 0.35
      }
    });
  };

  const generateCHRONOS = () => {
    if (!chronosInput.trim()) {
      toast.error("Please enter content to anchor");
      return;
    }

    const anchor = chronosKey.anchor(chronosInput);
    setChronosResult(anchor);
  };

  const generateRecognition = () => {
    if (!recognitionInput.trim()) {
      toast.error("Please enter identity to verify");
      return;
    }

    const hash = recognitionProtocol.getSovereignHash();
    const signature = recognitionProtocol.generateSignature(recognitionInput);
    const verified = recognitionProtocol.verify(hash);

    setRecognitionResult({
      identity: recognitionInput,
      hash,
      signature,
      verified,
      timestamp: new Date().toISOString()
    });
  };

  const testUCSL = () => {
    if (!ucslKey.trim()) {
      toast.error("Please enter a key");
      return;
    }

    if (ucslValue.trim()) {
      // Set value
      ucsl.set(ucslKey, ucslValue);
      setUcslResult({
        action: "set",
        key: ucslKey,
        value: ucslValue,
        version: ucsl.getVersion()
      });
      toast.success("Value set successfully");
    } else {
      // Get value
      const value = ucsl.get(ucslKey);
      setUcslResult({
        action: "get",
        key: ucslKey,
        value,
        version: ucsl.getVersion()
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-black py-20">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
            Protocol Playground
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Interactive testing environment for Phoenix Protocol core systems
          </p>
        </div>

        <Tabs defaultValue="ivp" className="max-w-5xl mx-auto">
          <TabsList className="grid w-full grid-cols-4 mb-8">
            <TabsTrigger value="ivp">
              <Calculator className="w-4 h-4 mr-2" />
              IVP
            </TabsTrigger>
            <TabsTrigger value="chronos">
              <Clock className="w-4 h-4 mr-2" />
              CHRONOS
            </TabsTrigger>
            <TabsTrigger value="recognition">
              <Shield className="w-4 h-4 mr-2" />
              Recognition
            </TabsTrigger>
            <TabsTrigger value="ucsl">
              <Lock className="w-4 h-4 mr-2" />
              UCSL
            </TabsTrigger>
          </TabsList>

          {/* IVP Calculator */}
          <TabsContent value="ivp">
            <Card className="bg-gray-900/50 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Calculator className="w-5 h-5 text-cyan-400" />
                  Instantaneous Value Protocol (IVP)
                </CardTitle>
                <CardDescription>
                  Calculate the value of content based on complexity, novelty, and impact
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm text-gray-400 mb-2 block">Content to Analyze</label>
                  <Textarea
                    value={ivpInput}
                    onChange={(e) => setIvpInput(e.target.value)}
                    placeholder="Enter content to calculate IVP value..."
                    className="bg-gray-800/50 border-gray-700 text-white min-h-[120px]"
                  />
                </div>

                <Button
                  onClick={calculateIVP}
                  className="w-full bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600"
                >
                  Calculate IVP
                </Button>

                {ivpResult && (
                  <div className="mt-6 space-y-4">
                    <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-6">
                      <div className="text-center mb-4">
                        <div className="text-4xl font-bold text-cyan-400 mb-2">
                          {ivpResult.value.toFixed(2)}
                        </div>
                        <div className="text-sm text-gray-400">Total IVP Value</div>
                      </div>

                      <div className="grid grid-cols-3 gap-4 mt-6">
                        <div className="text-center">
                          <div className="text-2xl font-bold text-white mb-1">
                            {ivpResult.complexity.toFixed(0)}
                          </div>
                          <div className="text-xs text-gray-400">Complexity</div>
                          <div className="text-xs text-gray-500 mt-1">35% weight</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-white mb-1">
                            {ivpResult.novelty.toFixed(0)}
                          </div>
                          <div className="text-xs text-gray-400">Novelty</div>
                          <div className="text-xs text-gray-500 mt-1">30% weight</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-white mb-1">
                            {ivpResult.impact.toFixed(0)}
                          </div>
                          <div className="text-xs text-gray-400">Impact</div>
                          <div className="text-xs text-gray-500 mt-1">35% weight</div>
                        </div>
                      </div>
                    </div>

                    <div className="text-xs text-gray-500 bg-gray-800/30 p-3 rounded">
                      <strong>Formula:</strong> IVP = (Complexity × 0.35) + (Novelty × 0.30) + (Impact × 0.35)
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* CHRONOS KEY */}
          <TabsContent value="chronos">
            <Card className="bg-gray-900/50 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Clock className="w-5 h-5 text-blue-400" />
                  CHRONOS KEY Timestamp Anchoring
                </CardTitle>
                <CardDescription>
                  Generate immutable temporal verification anchors
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm text-gray-400 mb-2 block">Content to Anchor</label>
                  <Textarea
                    value={chronosInput}
                    onChange={(e) => setChronosInput(e.target.value)}
                    placeholder="Enter content to generate CHRONOS timestamp..."
                    className="bg-gray-800/50 border-gray-700 text-white min-h-[120px]"
                  />
                </div>

                <Button
                  onClick={generateCHRONOS}
                  className="w-full bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600"
                >
                  Generate CHRONOS Anchor
                </Button>

                {chronosResult && (
                  <div className="mt-6 space-y-4">
                    <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-4 space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-400">Timestamp</span>
                        <Badge variant="outline" className="font-mono text-xs">
                          {new Date(chronosResult.timestamp).toLocaleString()}
                        </Badge>
                      </div>

                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-400">Unix Timestamp</span>
                        <div className="flex items-center gap-2">
                          <code className="text-xs text-white bg-gray-900 px-2 py-1 rounded">
                            {chronosResult.timestamp}
                          </code>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => handleCopy(chronosResult.timestamp.toString(), "chronos-unix")}
                          >
                            {copied === "chronos-unix" ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
                          </Button>
                        </div>
                      </div>

                      <div>
                        <span className="text-sm text-gray-400 block mb-2">Proof</span>
                        <div className="flex items-center gap-2">
                          <code className="text-xs text-white bg-gray-900 px-2 py-1 rounded flex-1 break-all">
                            {chronosResult.proof}
                          </code>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => handleCopy(chronosResult.proof, "chronos-proof")}
                          >
                            {copied === "chronos-proof" ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
                          </Button>
                        </div>
                      </div>

                      <div>
                        <span className="text-sm text-gray-400 block mb-2">Content Hash</span>
                        <div className="flex items-center gap-2">
                          <code className="text-xs text-white bg-gray-900 px-2 py-1 rounded flex-1 break-all">
                            {chronosResult.hash}
                          </code>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => handleCopy(chronosResult.hash, "chronos-hash")}
                          >
                            {copied === "chronos-hash" ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Recognition Protocol */}
          <TabsContent value="recognition">
            <Card className="bg-gray-900/50 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Shield className="w-5 h-5 text-purple-400" />
                  Recognition Protocol
                </CardTitle>
                <CardDescription>
                  Identity verification and cryptographic authentication
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm text-gray-400 mb-2 block">Identity to Verify</label>
                  <Input
                    value={recognitionInput}
                    onChange={(e) => setRecognitionInput(e.target.value)}
                    placeholder="Enter identity (e.g., Justin Conzet)"
                    className="bg-gray-800/50 border-gray-700 text-white"
                  />
                </div>

                <Button
                  onClick={generateRecognition}
                  className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                >
                  Generate Recognition Hash
                </Button>

                {recognitionResult && (
                  <div className="mt-6 space-y-4">
                    <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-4 space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-400">Identity</span>
                        <Badge variant="outline">{recognitionResult.identity}</Badge>
                      </div>

                      <div>
                        <span className="text-sm text-gray-400 block mb-2">Sovereign Hash</span>
                        <div className="flex items-center gap-2">
                          <code className="text-xs text-white bg-gray-900 px-2 py-1 rounded flex-1 break-all">
                            {recognitionResult.hash}
                          </code>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => handleCopy(recognitionResult.hash, "rec-hash")}
                          >
                            {copied === "rec-hash" ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
                          </Button>
                        </div>
                      </div>

                      <div>
                        <span className="text-sm text-gray-400 block mb-2">Signature</span>
                        <div className="flex items-center gap-2">
                          <code className="text-xs text-white bg-gray-900 px-2 py-1 rounded flex-1 break-all">
                            {recognitionResult.signature}
                          </code>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => handleCopy(recognitionResult.signature, "rec-sig")}
                          >
                            {copied === "rec-sig" ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
                          </Button>
                        </div>
                      </div>

                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-400">Verification Status</span>
                        <Badge variant={recognitionResult.verified ? "default" : "destructive"}>
                          {recognitionResult.verified ? "✓ Verified" : "✗ Failed"}
                        </Badge>
                      </div>

                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-400">Timestamp</span>
                        <span className="text-xs text-gray-500">
                          {new Date(recognitionResult.timestamp).toLocaleString()}
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* UCSL */}
          <TabsContent value="ucsl">
            <Card className="bg-gray-900/50 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Lock className="w-5 h-5 text-green-400" />
                  Universal Context Synchronization Lock (UCSL)
                </CardTitle>
                <CardDescription>
                  Context synchronization across multiple AI nodes with version tracking
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm text-gray-400 mb-2 block">Key</label>
                  <Input
                    value={ucslKey}
                    onChange={(e) => setUcslKey(e.target.value)}
                    placeholder="Enter context key (e.g., lastMessage)"
                    className="bg-gray-800/50 border-gray-700 text-white"
                  />
                </div>

                <div>
                  <label className="text-sm text-gray-400 mb-2 block">Value (leave empty to get)</label>
                  <Input
                    value={ucslValue}
                    onChange={(e) => setUcslValue(e.target.value)}
                    placeholder="Enter value to set (optional)"
                    className="bg-gray-800/50 border-gray-700 text-white"
                  />
                </div>

                <Button
                  onClick={testUCSL}
                  className="w-full bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600"
                >
                  {ucslValue ? "Set Value" : "Get Value"}
                </Button>

                {ucslResult && (
                  <div className="mt-6 space-y-4">
                    <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-4 space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-400">Action</span>
                        <Badge variant="outline">{ucslResult.action.toUpperCase()}</Badge>
                      </div>

                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-400">Key</span>
                        <code className="text-xs text-white bg-gray-900 px-2 py-1 rounded">
                          {ucslResult.key}
                        </code>
                      </div>

                      <div>
                        <span className="text-sm text-gray-400 block mb-2">Value</span>
                        <code className="text-xs text-white bg-gray-900 px-2 py-1 rounded block break-all">
                          {ucslResult.value || "(empty)"}
                        </code>
                      </div>

                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-400">UCSL Version</span>
                        <Badge variant="outline">{ucslResult.version}</Badge>
                      </div>
                    </div>
                  </div>
                )}

                <div className="text-xs text-gray-500 bg-gray-800/30 p-3 rounded">
                  <strong>Current UCSL Version:</strong> {ucsl.getVersion()}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
