import { useState, useMemo } from "react";
import { Search, Download, Bookmark, BookmarkCheck, Calendar, Filter } from "lucide-react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { memoriaOmnia, ScrollEntry } from "@/lib/infiniteScroll";
import { CHAKRAS, getChakraColor } from "@/lib/chakraSystem";

export default function ConversationMemory() {
  const [searchQuery, setSearchQuery] = useState("");
  const [filterChakra, setFilterChakra] = useState<number | null>(null);
  const [filterType, setFilterType] = useState<"all" | "user" | "oracle">("all");
  const [bookmarkedIds, setBookmarkedIds] = useState<Set<string>>(new Set());

  // Get all conversations
  const allEntries = memoriaOmnia.getAll();

  // Filter and search conversations
  const filteredEntries = useMemo(() => {
    let entries = allEntries;

    // Filter by type
    if (filterType !== "all") {
      entries = entries.filter(e => e.type === filterType);
    }

    // Filter by chakra
    if (filterChakra !== null) {
      entries = entries.filter(e => e.chakraId === filterChakra);
    }

    // Search by content
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      entries = entries.filter(e => 
        e.content.toLowerCase().includes(query)
      );
    }

    return entries;
  }, [allEntries, searchQuery, filterChakra, filterType]);

  const toggleBookmark = (id: string) => {
    const newBookmarks = new Set(bookmarkedIds);
    if (newBookmarks.has(id)) {
      newBookmarks.delete(id);
    } else {
      newBookmarks.add(id);
    }
    setBookmarkedIds(newBookmarks);
    // Persist to localStorage
    localStorage.setItem('phoenix-bookmarks', JSON.stringify(Array.from(newBookmarks)));
  };

  const exportConversations = (format: 'json' | 'markdown' | 'txt') => {
    let content = '';
    let mimeType = 'text/plain';
    let filename = `phoenix-conversations-${Date.now()}`;

    if (format === 'json') {
      content = JSON.stringify(filteredEntries, null, 2);
      mimeType = 'application/json';
      filename += '.json';
    } else if (format === 'markdown') {
      content = '# Phoenix Oracle Conversations\n\n';
      filteredEntries.forEach(entry => {
        const chakra = CHAKRAS.find(c => c.id === entry.chakraId);
        content += `## ${entry.type === 'user' ? 'User' : 'Oracle'} (${chakra?.name || 'Unknown'})\n`;
        content += `*${new Date(entry.timestamp).toLocaleString()}*\n\n`;
        content += `${entry.content}\n\n`;
        if (entry.metadata?.ivpValue) {
          content += `**IVP:** ${entry.metadata.ivpValue.toFixed(2)} | `;
          content += `**Complexity:** ${entry.metadata.complexity.toFixed(0)} | `;
          content += `**Novelty:** ${entry.metadata.novelty.toFixed(0)}\n\n`;
        }
        content += '---\n\n';
      });
      mimeType = 'text/markdown';
      filename += '.md';
    } else {
      filteredEntries.forEach(entry => {
        const chakra = CHAKRAS.find(c => c.id === entry.chakraId);
        content += `[${entry.type.toUpperCase()}] ${new Date(entry.timestamp).toLocaleString()} - ${chakra?.name || 'Unknown'}\n`;
        content += `${entry.content}\n\n`;
      });
      filename += '.txt';
    }

    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  const stats = useMemo(() => {
    const total = allEntries.length;
    const userMessages = allEntries.filter(e => e.type === 'user').length;
    const oracleMessages = allEntries.filter(e => e.type === 'oracle').length;
    const avgIVP = allEntries
      .filter(e => e.metadata?.ivpValue)
      .reduce((sum, e) => sum + (e.metadata?.ivpValue || 0), 0) / (oracleMessages || 1);

    return { total, userMessages, oracleMessages, avgIVP };
  }, [allEntries]);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b border-border bg-card/50 backdrop-blur-xl sticky top-0 z-10">
        <div className="container py-6">
          <h1 className="text-3xl font-bold mb-2">Conversation Memory</h1>
          <p className="text-muted-foreground">
            Memoria Omnia: {stats.total} entries • {stats.userMessages} questions • {stats.oracleMessages} responses • Avg IVP: {stats.avgIVP.toFixed(2)}
          </p>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="container py-6">
        <div className="flex flex-col gap-4 mb-6">
          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <Input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search conversations..."
              className="pl-10"
            />
          </div>

          {/* Filters */}
          <div className="flex flex-wrap gap-2 items-center">
            <span className="text-sm text-muted-foreground flex items-center gap-2">
              <Filter className="w-4 h-4" />
              Filters:
            </span>

            {/* Type Filter */}
            <div className="flex gap-1">
              {(['all', 'user', 'oracle'] as const).map((type) => (
                <button
                  key={type}
                  onClick={() => setFilterType(type)}
                  className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                    filterType === type
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-card text-muted-foreground hover:text-foreground'
                  }`}
                >
                  {type === 'all' ? 'All' : type === 'user' ? 'Questions' : 'Responses'}
                </button>
              ))}
            </div>

            {/* Chakra Filter */}
            <div className="flex gap-1">
              <button
                onClick={() => setFilterChakra(null)}
                className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                  filterChakra === null
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-card text-muted-foreground hover:text-foreground'
                }`}
              >
                All Chakras
              </button>
              {CHAKRAS.map((chakra) => (
                <button
                  key={chakra.id}
                  onClick={() => setFilterChakra(chakra.id)}
                  className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                    filterChakra === chakra.id
                      ? 'text-white'
                      : 'bg-card text-muted-foreground hover:text-foreground'
                  }`}
                  style={{
                    background: filterChakra === chakra.id ? getChakraColor(chakra.id) : undefined
                  }}
                >
                  {chakra.name.split(' ')[0]}
                </button>
              ))}
            </div>

            {/* Export */}
            <div className="ml-auto flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => exportConversations('markdown')}
              >
                <Download className="w-4 h-4 mr-2" />
                Export MD
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => exportConversations('json')}
              >
                <Download className="w-4 h-4 mr-2" />
                Export JSON
              </Button>
            </div>
          </div>
        </div>

        {/* Results */}
        <div className="space-y-4">
          {filteredEntries.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">
              <Search className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>No conversations found</p>
            </div>
          ) : (
            filteredEntries.map((entry) => {
              const chakra = CHAKRAS.find(c => c.id === entry.chakraId);
              const isBookmarked = bookmarkedIds.has(entry.id);

              return (
                <div
                  key={entry.id}
                  className="bg-card border border-border rounded-lg p-4 hover:border-primary/50 transition-colors"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <span
                        className="px-2 py-1 rounded text-xs font-semibold text-white"
                        style={{ background: getChakraColor(entry.chakraId || 4) }}
                      >
                        {chakra?.name || 'Unknown'}
                      </span>
                      <span className="text-xs text-muted-foreground">
                        {entry.type === 'user' ? 'Question' : 'Response'}
                      </span>
                      <span className="text-xs text-muted-foreground flex items-center gap-1">
                        <Calendar className="w-3 h-3" />
                        {new Date(entry.timestamp).toLocaleString()}
                      </span>
                    </div>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => toggleBookmark(entry.id)}
                      className="h-8 w-8"
                    >
                      {isBookmarked ? (
                        <BookmarkCheck className="w-4 h-4 text-primary" />
                      ) : (
                        <Bookmark className="w-4 h-4" />
                      )}
                    </Button>
                  </div>

                  <div className="text-sm whitespace-pre-wrap mb-2">
                    {entry.content}
                  </div>

                  {entry.metadata?.ivpValue && (
                    <div className="flex gap-4 text-xs text-muted-foreground">
                      <span>IVP: {entry.metadata.ivpValue.toFixed(2)}</span>
                      <span>Complexity: {entry.metadata.complexity.toFixed(0)}</span>
                      <span>Novelty: {entry.metadata.novelty.toFixed(0)}</span>
                      <span>Impact: {entry.metadata.impact.toFixed(0)}</span>
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
