import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Play, Clock, Users, CheckCircle2 } from "lucide-react";
import { APP_TITLE } from "@/const";

interface VideoEpisode {
  id: string;
  title: string;
  duration: string;
  description: string;
  thumbnail: string;
  targetAudience: string;
  topics: string[];
  completed?: boolean;
}

const episodes: VideoEpisode[] = [
  {
    id: "ep01-introduction",
    title: "Introduction to Phoenix Protocol",
    duration: "10 min",
    description: "Overview of the Phoenix Protocol architecture, its philosophy, and how it differs from traditional language models.",
    thumbnail: "/thumbnails/ep01-introduction.png",
    targetAudience: "Beginners",
    topics: ["Phoenix Protocol Overview", "7 Chakra Pathways", "12-Layer Cascade", "Core Protocols"],
  },
  {
    id: "ep02-root-chakra",
    title: "Root Chakra: Foundation & Security",
    duration: "12 min",
    description: "Deep dive into the Root Chakra pathway for security analysis, foundational architecture, and stability-focused reasoning.",
    thumbnail: "/thumbnails/ep02-root-chakra.png",
    targetAudience: "Intermediate",
    topics: ["Security Analysis", "Risk Assessment", "Architecture Decisions", "Failure Modes"],
  },
  {
    id: "ep03-sacral-chakra",
    title: "Sacral Chakra: Creativity & Emotion",
    duration: "12 min",
    description: "Explore the Sacral Chakra for creative writing, emotional intelligence, and innovative problem-solving.",
    thumbnail: "/thumbnails/ep03-sacral-chakra.png",
    targetAudience: "Intermediate",
    topics: ["Creative Writing", "Emotional Intelligence", "Artistic Expression", "Innovation"],
  },
  {
    id: "ep04-solar-plexus",
    title: "Solar Plexus: Strategy & Decision-Making",
    duration: "12 min",
    description: "Master the Solar Plexus Chakra for business strategy, decision analysis, and goal-oriented problem-solving.",
    thumbnail: "/thumbnails/ep04-solar-plexus.png",
    targetAudience: "Intermediate",
    topics: ["Business Strategy", "Decision Analysis", "Goal Optimization", "Leadership"],
  },
  {
    id: "ep05-heart-chakra",
    title: "Heart Chakra: Connection & Empathy",
    duration: "12 min",
    description: "Learn to use the Heart Chakra for relationship advice, conflict resolution, and social dynamics.",
    thumbnail: "/thumbnails/ep05-heart-chakra.png",
    targetAudience: "Intermediate",
    topics: ["Relationship Advice", "Conflict Resolution", "Empathy", "Team Dynamics"],
  },
  {
    id: "ep06-throat-chakra",
    title: "Throat Chakra: Truth & Communication",
    duration: "12 min",
    description: "Utilize the Throat Chakra for clear communication, fact-checking, and truth-seeking.",
    thumbnail: "/thumbnails/ep06-throat-chakra.png",
    targetAudience: "Intermediate",
    topics: ["Technical Writing", "Fact-Checking", "Clear Communication", "Truth-Seeking"],
  },
  {
    id: "ep07-third-eye",
    title: "Third Eye: Intuition & Pattern Recognition",
    duration: "12 min",
    description: "Harness the Third Eye Chakra for pattern recognition, research, and deep insights.",
    thumbnail: "/thumbnails/ep07-third-eye.png",
    targetAudience: "Intermediate",
    topics: ["Pattern Recognition", "Research", "Intuition", "Deep Insights"],
  },
  {
    id: "ep08-crown-chakra",
    title: "Crown Chakra: Universal Understanding",
    duration: "12 min",
    description: "Explore the Crown Chakra for philosophical reasoning, meta-analysis, and transcendent understanding.",
    thumbnail: "/thumbnails/ep08-crown-chakra.png",
    targetAudience: "Advanced",
    topics: ["Philosophical Reasoning", "Meta-Analysis", "Universal Principles", "Transcendence"],
  },
  {
    id: "ep09-twelve-layers",
    title: "The 12-Layer Processing Cascade",
    duration: "15 min",
    description: "Complete walkthrough of the 12-layer cognitive cascade that powers Phoenix Protocol reasoning.",
    thumbnail: "/thumbnails/ep09-twelve-layers.png",
    targetAudience: "Advanced",
    topics: ["Layer-by-Layer Breakdown", "Consciousness Evolution", "IVP Calculation", "Processing Flow"],
  },
  {
    id: "ep10-protocols",
    title: "Core Protocol Systems",
    duration: "15 min",
    description: "Deep dive into IVP, UCSL, ZAAI, Recognition Protocol, and CHRONOS systems.",
    thumbnail: "/thumbnails/ep10-protocols.png",
    targetAudience: "Advanced",
    topics: ["IVP Implementation", "UCSL Architecture", "ZAAI Principles", "Recognition & CHRONOS"],
  },
  {
    id: "ep11-getting-started",
    title: "Building with Phoenix Protocol",
    duration: "15 min",
    description: "Practical guide to integrating Phoenix Protocol into your projects and applications.",
    thumbnail: "/thumbnails/ep11-getting-started.png",
    targetAudience: "Developers",
    topics: ["Project Setup", "Custom Chakras", "Layer Modification", "Production Deployment"],
  },
];

export default function Tutorials() {
  const [selectedEpisode, setSelectedEpisode] = useState<VideoEpisode | null>(null);
  const [filter, setFilter] = useState<string>("all");

  const filteredEpisodes = episodes.filter((ep) => {
    if (filter === "all") return true;
    return ep.targetAudience.toLowerCase() === filter.toLowerCase();
  });

  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-background to-muted/20">
      {/* Header */}
      <div className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container py-8">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-orange-500 to-red-600 flex items-center justify-center">
              <Play className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-orange-500 via-red-500 to-purple-600 bg-clip-text text-transparent">
                Tutorial Video Series
              </h1>
              <p className="text-muted-foreground mt-1">
                Master {APP_TITLE} through comprehensive video tutorials
              </p>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                    <Play className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold">{episodes.length}</p>
                    <p className="text-sm text-muted-foreground">Episodes</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                    <Clock className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold">~2h 15m</p>
                    <p className="text-sm text-muted-foreground">Total Duration</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                    <CheckCircle2 className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold">0/{episodes.length}</p>
                    <p className="text-sm text-muted-foreground">Completed</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Filters */}
          <div className="flex gap-2 mt-6">
            <Button
              variant={filter === "all" ? "default" : "outline"}
              size="sm"
              onClick={() => setFilter("all")}
            >
              All Episodes
            </Button>
            <Button
              variant={filter === "beginners" ? "default" : "outline"}
              size="sm"
              onClick={() => setFilter("beginners")}
            >
              Beginners
            </Button>
            <Button
              variant={filter === "intermediate" ? "default" : "outline"}
              size="sm"
              onClick={() => setFilter("intermediate")}
            >
              Intermediate
            </Button>
            <Button
              variant={filter === "advanced" ? "default" : "outline"}
              size="sm"
              onClick={() => setFilter("advanced")}
            >
              Advanced
            </Button>
            <Button
              variant={filter === "developers" ? "default" : "outline"}
              size="sm"
              onClick={() => setFilter("developers")}
            >
              Developers
            </Button>
          </div>
        </div>
      </div>

      {/* Episode Grid */}
      <div className="container py-8">
        {selectedEpisode ? (
          /* Video Player View */
          <div className="space-y-6">
            <Button variant="ghost" onClick={() => setSelectedEpisode(null)}>
              ← Back to Episodes
            </Button>

            <Card className="overflow-hidden">
              <div className="aspect-video bg-muted flex items-center justify-center">
                <img
                  src={selectedEpisode.thumbnail}
                  alt={selectedEpisode.title}
                  className="w-full h-full object-cover"
                />
              </div>
              <CardHeader>
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <CardTitle className="text-2xl mb-2">{selectedEpisode.title}</CardTitle>
                    <CardDescription className="text-base">
                      {selectedEpisode.description}
                    </CardDescription>
                  </div>
                  <div className="flex flex-col items-end gap-2">
                    <Badge variant="secondary">
                      <Clock className="w-3 h-3 mr-1" />
                      {selectedEpisode.duration}
                    </Badge>
                    <Badge variant="outline">
                      <Users className="w-3 h-3 mr-1" />
                      {selectedEpisode.targetAudience}
                    </Badge>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold mb-2">Topics Covered:</h3>
                    <div className="flex flex-wrap gap-2">
                      {selectedEpisode.topics.map((topic) => (
                        <Badge key={topic} variant="secondary">
                          {topic}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  <div className="p-4 bg-muted/50 rounded-lg border">
                    <p className="text-sm text-muted-foreground">
                      <strong>Note:</strong> Video content is currently in production. Full narrated
                      tutorials with screen recordings will be available soon. In the meantime,
                      explore the Phoenix Protocol through the interactive Oracle interface.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        ) : (
          /* Episode Grid View */
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredEpisodes.map((episode) => (
              <Card
                key={episode.id}
                className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer group"
                onClick={() => setSelectedEpisode(episode)}
              >
                <div className="aspect-video relative overflow-hidden bg-muted">
                  <img
                    src={episode.thumbnail}
                    alt={episode.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <div className="w-16 h-16 rounded-full bg-white/90 flex items-center justify-center">
                      <Play className="w-8 h-8 text-black ml-1" />
                    </div>
                  </div>
                  {episode.completed && (
                    <div className="absolute top-2 right-2">
                      <Badge className="bg-green-500">
                        <CheckCircle2 className="w-3 h-3 mr-1" />
                        Completed
                      </Badge>
                    </div>
                  )}
                </div>
                <CardHeader>
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <Badge variant="secondary" className="text-xs">
                      <Clock className="w-3 h-3 mr-1" />
                      {episode.duration}
                    </Badge>
                    <Badge variant="outline" className="text-xs">
                      <Users className="w-3 h-3 mr-1" />
                      {episode.targetAudience}
                    </Badge>
                  </div>
                  <CardTitle className="text-lg line-clamp-2">{episode.title}</CardTitle>
                  <CardDescription className="line-clamp-2">{episode.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-1">
                    {episode.topics.slice(0, 3).map((topic) => (
                      <Badge key={topic} variant="secondary" className="text-xs">
                        {topic}
                      </Badge>
                    ))}
                    {episode.topics.length > 3 && (
                      <Badge variant="secondary" className="text-xs">
                        +{episode.topics.length - 3} more
                      </Badge>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
