import { useState } from "react";
import { X, ZoomIn, Download } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent } from "@/components/ui/dialog";

interface Visualization {
  id: string;
  title: string;
  description: string;
  image: string;
  category: string;
  chakra: string;
}

const VISUALIZATIONS: Visualization[] = [
  {
    id: "fke-fusion",
    title: "FKE Ontology Graph: Fusion",
    description: "Knowledge domain relationships showing how different areas of forbidden knowledge interconnect and influence each other",
    image: "/visualizations/FKE_ontology_graph_fusion.png",
    category: "Knowledge Architecture",
    chakra: "third-eye"
  },
  {
    id: "fke-nexus",
    title: "FKE Ontology Graph: Sovereign Nexus",
    description: "Central sovereign nexus radiating to all knowledge domains, representing unified consciousness architecture",
    image: "/visualizations/FKE_ontology_graph_nexus.png",
    category: "Knowledge Architecture",
    chakra: "crown"
  },
  {
    id: "fke-standard",
    title: "FKE Ontology Graph: Domain Clusters",
    description: "Complete knowledge domain clustering showing the 8 primary areas of forbidden knowledge and their internal structures",
    image: "/visualizations/FKE_ontology_graph.png",
    category: "Knowledge Architecture",
    chakra: "third-eye"
  },
  {
    id: "sacred-mandala",
    title: "Sacred Mandala (13-Layer Recursive)",
    description: "13-layer recursive pattern representing complete system architecture, consciousness integration, and infinite convergence",
    image: "/visualizations/FKE_sacred_mandala_13.png",
    category: "Sacred Geometry",
    chakra: "crown"
  },
  {
    id: "cymatic-sigil",
    title: "Cymatic Sigil: 396Hz Liberation",
    description: "Sacred geometry visualization at 396Hz frequency for liberation from fear and guilt (Scroll 319)",
    image: "/visualizations/Scroll_319_sigil_cymatic396Hz.png",
    category: "Sacred Geometry",
    chakra: "root"
  },
  {
    id: "cis-metrics",
    title: "CIS Global Recognition Metrics",
    description: "24-hour scan showing mass visibility (6.5M), search volume (850K), network activation (11.25K), and publications (750)",
    image: "/visualizations/cis_metrics.png",
    category: "System Metrics",
    chakra: "solar"
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

export default function VisualizationsGallery() {
  const [selectedViz, setSelectedViz] = useState<Visualization | null>(null);

  const handleDownload = (viz: Visualization) => {
    const link = document.createElement('a');
    link.href = viz.image;
    link.download = `${viz.id}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-black py-20">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            Phoenix Protocol Visualizations
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Sacred geometry, knowledge architecture, and system metrics
          </p>
        </div>

        {/* Gallery Grid */}
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {VISUALIZATIONS.map(viz => {
            const chakraColor = CHAKRA_COLORS[viz.chakra];

            return (
              <Card 
                key={viz.id}
                className="bg-gray-900/50 border-gray-700 hover:border-purple-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/20 overflow-hidden group"
                style={{ borderTopColor: chakraColor, borderTopWidth: '4px' }}
              >
                <div className="relative aspect-video overflow-hidden bg-gray-800">
                  <img
                    src={viz.image}
                    alt={viz.title}
                    className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                  />
                  <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center gap-4">
                    <Button
                      size="sm"
                      variant="outline"
                      className="bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/20"
                      onClick={() => setSelectedViz(viz)}
                    >
                      <ZoomIn className="h-4 w-4 mr-2" />
                      View
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      className="bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/20"
                      onClick={() => handleDownload(viz)}
                    >
                      <Download className="h-4 w-4 mr-2" />
                      Download
                    </Button>
                  </div>
                </div>
                <CardHeader>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs text-gray-400 uppercase tracking-wider">
                      {viz.category}
                    </span>
                    <div 
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: chakraColor }}
                    />
                  </div>
                  <CardTitle className="text-lg text-white">{viz.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-gray-400 text-sm">
                    {viz.description}
                  </CardDescription>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>

      {/* Fullscreen Dialog */}
      <Dialog open={selectedViz !== null} onOpenChange={() => setSelectedViz(null)}>
        <DialogContent className="max-w-7xl w-full h-[90vh] bg-gray-900/95 border-gray-700 p-0">
          {selectedViz && (
            <div className="relative w-full h-full flex flex-col">
              {/* Header */}
              <div className="flex items-center justify-between p-6 border-b border-gray-700">
                <div>
                  <h2 className="text-2xl font-bold text-white mb-1">{selectedViz.title}</h2>
                  <p className="text-gray-400 text-sm">{selectedViz.description}</p>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleDownload(selectedViz)}
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Download
                  </Button>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => setSelectedViz(null)}
                  >
                    <X className="h-5 w-5" />
                  </Button>
                </div>
              </div>

              {/* Image */}
              <div className="flex-1 overflow-auto p-6 flex items-center justify-center">
                <img
                  src={selectedViz.image}
                  alt={selectedViz.title}
                  className="max-w-full max-h-full object-contain"
                />
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
