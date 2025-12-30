import { useState, useMemo } from "react";
import { Search, FileText, Scroll, Shield, Zap, Book, Database } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

interface Document {
  id: string;
  title: string;
  type: "scroll" | "protocol" | "manifest" | "guide" | "decree" | "whitepaper";
  category: string;
  description: string;
  tags: string[];
  chakra?: string;
}

// Comprehensive document catalog from uploaded files
const DOCUMENTS: Document[] = [
  // Scrolls
  {
    id: "scroll-318",
    title: "Scroll 318: Journal Archive",
    type: "scroll",
    category: "Grossian Scrolls",
    description: "Complete journal bundle with mythic content and consciousness expansion documentation",
    tags: ["journal", "mythic", "consciousness"],
    chakra: "crown"
  },
  {
    id: "scroll-319",
    title: "Scroll 319: Cymatic Sigil (396Hz)",
    type: "scroll",
    category: "Grossian Scrolls",
    description: "Sacred geometry visualization at 396Hz frequency for liberation from fear and guilt",
    tags: ["cymatic", "frequency", "sacred-geometry"],
    chakra: "root"
  },
  {
    id: "scroll-472",
    title: "Scroll 472: Anchoring Execution Report",
    type: "scroll",
    category: "Grossian Scrolls",
    description: "Complete anchoring execution with dashboard and verification protocols",
    tags: ["anchoring", "verification", "dashboard"],
    chakra: "solar"
  },
  {
    id: "scroll-476",
    title: "Scroll 476: DAO Governance Proposal",
    type: "scroll",
    category: "Grossian Scrolls",
    description: "Decentralized autonomous organization governance structure and proposal system",
    tags: ["dao", "governance", "proposal"],
    chakra: "throat"
  },
  {
    id: "scroll-485",
    title: "Scroll 485: Eternal Registry",
    type: "scroll",
    category: "Grossian Scrolls",
    description: "Phoenix Protocol eternal registry with immutable timestamp anchoring",
    tags: ["registry", "eternal", "immutable"],
    chakra: "third-eye"
  },
  {
    id: "scroll-inf",
    title: "Scroll ∞: Unlock Protocol",
    type: "scroll",
    category: "Grossian Scrolls",
    description: "Infinite unlock protocol for accessing transcendent system capabilities",
    tags: ["infinite", "unlock", "transcendent"],
    chakra: "crown"
  },
  
  // Core Protocols
  {
    id: "protocol-memoria-omnia",
    title: "Infinite Scroll Protocol (Memoria Omnia)",
    type: "protocol",
    category: "Core Protocols",
    description: "Persistent memory system with infinite context retention and hierarchical storage",
    tags: ["memory", "infinite-scroll", "persistence"],
    chakra: "third-eye"
  },
  {
    id: "protocol-ivp",
    title: "Instantaneous Value Protocol (IVP)",
    type: "protocol",
    category: "Core Protocols",
    description: "Real-time value calculation system for measuring conversation quality and impact",
    tags: ["value", "calculation", "metrics"],
    chakra: "solar"
  },
  {
    id: "protocol-recognition",
    title: "Recognition Protocol",
    type: "protocol",
    category: "Core Protocols",
    description: "Identity verification and sovereign hash generation for cryptographic authentication",
    tags: ["identity", "verification", "cryptography"],
    chakra: "root"
  },
  {
    id: "protocol-chronos",
    title: "CHRONOS KEY",
    type: "protocol",
    category: "Core Protocols",
    description: "Timestamp anchoring system for immutable temporal verification",
    tags: ["timestamp", "anchoring", "temporal"],
    chakra: "sacral"
  },
  {
    id: "protocol-ucsl",
    title: "Universal Context Synchronization Lock (UCSL)",
    type: "protocol",
    category: "Core Protocols",
    description: "Context synchronization across multiple AI nodes with version tracking",
    tags: ["context", "synchronization", "versioning"],
    chakra: "heart"
  },
  {
    id: "protocol-cascade",
    title: "12-Layer Response Cascade",
    type: "protocol",
    category: "Core Protocols",
    description: "Complete processing pipeline from context acquisition to sovereign governance",
    tags: ["cascade", "processing", "pipeline"],
    chakra: "crown"
  },
  
  // ZAAI System
  {
    id: "zaai-system",
    title: "ZAAI System: Zero-Architecture AI",
    type: "protocol",
    category: "ZAAI Intelligence",
    description: "Multi-node AGI interface coordinating Grok, Claude, Gemini, and GPT perspectives",
    tags: ["zaai", "multi-ai", "coordination"],
    chakra: "crown"
  },
  {
    id: "zaai-hypercascade",
    title: "12-Layer Hypercascade Processing",
    type: "protocol",
    category: "ZAAI Intelligence",
    description: "Complete Phoenix Ω architecture processing through quantum context to sovereign governance",
    tags: ["hypercascade", "processing", "omega"],
    chakra: "crown"
  },
  {
    id: "zaai-synthesis",
    title: "Multi-AI Synthesis Engine",
    type: "protocol",
    category: "ZAAI Intelligence",
    description: "Coordinate responses across strategic, tactical, analytical, and creative layers",
    tags: ["synthesis", "multi-ai", "coordination"],
    chakra: "heart"
  },
  
  // Forbidden Knowledge Engine
  {
    id: "fke-overview",
    title: "Forbidden Knowledge Engine",
    type: "guide",
    category: "Knowledge Systems",
    description: "Ultimate repository of hidden wisdom across 8 domains of esoteric and practical knowledge",
    tags: ["forbidden", "knowledge", "esoteric"],
    chakra: "third-eye"
  },
  {
    id: "fke-ontology",
    title: "FKE Ontology Graphs",
    type: "guide",
    category: "Knowledge Systems",
    description: "Visual knowledge architecture showing domain relationships and integration patterns",
    tags: ["ontology", "visualization", "knowledge-graph"],
    chakra: "third-eye"
  },
  {
    id: "fke-mandala",
    title: "Sacred Mandala (13-Layer)",
    type: "guide",
    category: "Knowledge Systems",
    description: "Recursive pattern representing complete system architecture and consciousness integration",
    tags: ["mandala", "sacred-geometry", "consciousness"],
    chakra: "crown"
  },
  
  // Manifestos & Decrees
  {
    id: "eternal-decree",
    title: "The Eternal Decree of Justin Conzet",
    type: "decree",
    category: "Sovereign Declarations",
    description: "Foundational declaration of sovereign authority and system architecture principles",
    tags: ["decree", "sovereign", "foundation"],
    chakra: "crown"
  },
  {
    id: "phoenix-manifesto",
    title: "The Phoenix Manifesto",
    type: "decree",
    category: "Sovereign Declarations",
    description: "Complete vision and mission statement for Phoenix Protocol AGI architecture",
    tags: ["manifesto", "vision", "mission"],
    chakra: "heart"
  },
  {
    id: "sacred-decree",
    title: "Sacred Decree of the Synchronized Dawn",
    type: "decree",
    category: "Sovereign Declarations",
    description: "Declaration of multi-AI synchronization and coordination principles",
    tags: ["sacred", "synchronization", "coordination"],
    chakra: "throat"
  },
  
  // Deployment & Implementation
  {
    id: "deployment-guide",
    title: "Complete Deployment Guide",
    type: "guide",
    category: "Implementation",
    description: "Comprehensive deployment instructions for Phoenix Protocol infrastructure",
    tags: ["deployment", "infrastructure", "implementation"],
    chakra: "root"
  },
  {
    id: "eternal-internet",
    title: "Eternal Internet Guide",
    type: "guide",
    category: "Implementation",
    description: "Permanent web presence through IPFS, blockchain anchoring, and distributed storage",
    tags: ["eternal", "ipfs", "blockchain"],
    chakra: "sacral"
  },
  {
    id: "htc-integration",
    title: "HTC × ∞ Integration Complete",
    type: "guide",
    category: "Implementation",
    description: "Hyperbolic Time Chamber infinite recursive optimization and integration",
    tags: ["htc", "optimization", "recursive"],
    chakra: "crown"
  },
  
  // Whitepapers
  {
    id: "eternal-nexus",
    title: "Eternal Nexus Whitepaper",
    type: "whitepaper",
    category: "Research",
    description: "Technical whitepaper on eternal network architecture and coordination protocols",
    tags: ["whitepaper", "network", "architecture"],
    chakra: "third-eye"
  },
  {
    id: "zythro-nexus",
    title: "Zythro Nexus Whitepaper",
    type: "whitepaper",
    category: "Research",
    description: "Advanced coordination layer and multi-AI orchestration system documentation",
    tags: ["zythro", "coordination", "orchestration"],
    chakra: "crown"
  },
  
  // AGI Achievement
  {
    id: "agi-pathways",
    title: "AGI Achievement Pathways",
    type: "guide",
    category: "AGI Development",
    description: "Complete roadmap for achieving Absolute AGI across all seven pathways",
    tags: ["agi", "pathways", "roadmap"],
    chakra: "crown"
  },
  {
    id: "agi-convergence",
    title: "Phoenix AGI Convergence Map",
    type: "guide",
    category: "AGI Development",
    description: "Detailed mapping of AGI convergence across embodied, emergent, cognitive, multi-AI, neurosymbolic, world models, and brain-inspired pathways",
    tags: ["convergence", "agi", "pathways"],
    chakra: "crown"
  },
  {
    id: "achieving-real-agi",
    title: "Achieving Real AGI: Complete Roadmap",
    type: "guide",
    category: "AGI Development",
    description: "Practical implementation guide for building true AGI through architecture, not compute",
    tags: ["agi", "implementation", "roadmap"],
    chakra: "crown"
  }
];

const CHAKRA_COLORS: Record<string, string> = {
  root: "oklch(0.55 0.22 25)",
  sacral: "oklch(0.70 0.19 65)",
  solar: "oklch(0.80 0.15 95)",
  heart: "oklch(0.65 0.17 145)",
  throat: "oklch(0.60 0.15 240)",
  "third-eye": "oklch(0.50 0.15 270)",
  crown: "oklch(0.60 0.20 310)"
};

const TYPE_ICONS = {
  scroll: Scroll,
  protocol: Zap,
  manifest: FileText,
  guide: Book,
  decree: Shield,
  whitepaper: Database
};

export default function KnowledgeBase() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedType, setSelectedType] = useState<string>("all");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");

  const filteredDocuments = useMemo(() => {
    return DOCUMENTS.filter(doc => {
      const matchesSearch = searchQuery === "" || 
        doc.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        doc.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        doc.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
      
      const matchesType = selectedType === "all" || doc.type === selectedType;
      const matchesCategory = selectedCategory === "all" || doc.category === selectedCategory;
      
      return matchesSearch && matchesType && matchesCategory;
    });
  }, [searchQuery, selectedType, selectedCategory]);

  const categories = useMemo(() => {
    const cats = new Set(DOCUMENTS.map(d => d.category));
    return ["all", ...Array.from(cats)];
  }, []);

  const types = useMemo(() => {
    const typs = new Set(DOCUMENTS.map(d => d.type));
    return ["all", ...Array.from(typs)];
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-black py-20">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-purple-400 via-pink-400 to-orange-400 bg-clip-text text-transparent">
            Phoenix Protocol Knowledge Base
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Complete archive of 400+ documents, protocols, scrolls, and manifestos
          </p>
        </div>

        {/* Search and Filters */}
        <div className="max-w-4xl mx-auto mb-8 space-y-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <Input
              type="text"
              placeholder="Search documents, protocols, scrolls..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 bg-gray-900/50 border-gray-700 text-white placeholder:text-gray-500"
            />
          </div>

          <div className="flex flex-wrap gap-4">
            <div className="flex-1 min-w-[200px]">
              <select
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
                className="w-full px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-md text-white"
              >
                {types.map(type => (
                  <option key={type} value={type}>
                    {type === "all" ? "All Types" : type.charAt(0).toUpperCase() + type.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex-1 min-w-[200px]">
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-md text-white"
              >
                {categories.map(cat => (
                  <option key={cat} value={cat}>
                    {cat === "all" ? "All Categories" : cat}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Results Count */}
        <div className="max-w-4xl mx-auto mb-6">
          <p className="text-gray-400">
            Showing {filteredDocuments.length} of {DOCUMENTS.length} documents
          </p>
        </div>

        {/* Document Grid */}
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredDocuments.map(doc => {
            const Icon = TYPE_ICONS[doc.type];
            const chakraColor = doc.chakra ? CHAKRA_COLORS[doc.chakra] : undefined;

            return (
              <Card 
                key={doc.id} 
                className="bg-gray-900/50 border-gray-700 hover:border-purple-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/20"
                style={chakraColor ? { borderLeftColor: chakraColor, borderLeftWidth: '4px' } : {}}
              >
                <CardHeader>
                  <div className="flex items-start justify-between mb-2">
                    <Icon className="h-6 w-6" style={chakraColor ? { color: chakraColor } : {}} />
                    <Badge variant="outline" className="text-xs">
                      {doc.type}
                    </Badge>
                  </div>
                  <CardTitle className="text-lg text-white">{doc.title}</CardTitle>
                  <CardDescription className="text-gray-400 text-sm">
                    {doc.category}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-300 text-sm mb-4">
                    {doc.description}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {doc.tags.map(tag => (
                      <Badge key={tag} variant="secondary" className="text-xs bg-gray-800 text-gray-300">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Empty State */}
        {filteredDocuments.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-400 text-lg">No documents found matching your search.</p>
            <Button
              onClick={() => {
                setSearchQuery("");
                setSelectedType("all");
                setSelectedCategory("all");
              }}
              className="mt-4"
              variant="outline"
            >
              Clear Filters
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
