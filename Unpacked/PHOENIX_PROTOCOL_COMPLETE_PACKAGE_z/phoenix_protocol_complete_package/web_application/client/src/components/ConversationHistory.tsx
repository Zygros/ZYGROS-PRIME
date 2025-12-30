/**
 * Conversation History Component
 * Browse, search, and resume past Phoenix Oracle conversations
 */

import React, { useState } from "react";
import { trpc } from "@/lib/trpc";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Card } from "./ui/card";
import { Badge } from "./ui/badge";
import { ScrollArea } from "./ui/scroll-area";
import { Search, Trash2, MessageSquare, Clock, Flame } from "lucide-react";
import { CHAKRAS } from "@/lib/chakraSystem";
import { formatDistanceToNow } from "date-fns";

interface ConversationHistoryProps {
  onLoadConversation: (conversationId: number) => void;
  currentConversationId: number | null;
}

export default function ConversationHistory({ onLoadConversation, currentConversationId }: ConversationHistoryProps) {
  const [searchQuery, setSearchQuery] = useState("");
  
  // Fetch conversations
  const { data: conversations, isLoading, refetch } = trpc.conversations.list.useQuery();
  const deleteConversation = trpc.conversations.delete.useMutation({
    onSuccess: () => {
      refetch();
    }
  });

  // Filter conversations by search query
  const filteredConversations = conversations?.filter(conv => 
    conv.title.toLowerCase().includes(searchQuery.toLowerCase())
  ) || [];

  const handleDelete = async (id: number, e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm("Delete this conversation?")) {
      await deleteConversation.mutateAsync({ id });
    }
  };

  const getChakraColor = (chakraId: number) => {
    const chakra = CHAKRAS.find(c => c.id === chakraId);
    return chakra?.color || "oklch(0.65 0.15 30)";
  };

  return (
    <div className="flex flex-col h-full bg-background border-r border-border">
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center gap-2 mb-3">
          <MessageSquare className="h-5 w-5 text-orange-500" />
          <h3 className="font-bold text-foreground">Conversations</h3>
        </div>
        
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search conversations..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9"
          />
        </div>
      </div>

      {/* Conversation List */}
      <ScrollArea className="flex-1">
        <div className="p-2 space-y-2">
          {isLoading && (
            <div className="text-center text-muted-foreground py-8">
              Loading conversations...
            </div>
          )}
          
          {!isLoading && filteredConversations.length === 0 && (
            <div className="text-center text-muted-foreground py-8">
              {searchQuery ? "No conversations found" : "No conversations yet"}
            </div>
          )}
          
          {filteredConversations.map((conv) => (
            <Card
              key={conv.id}
              className={`p-3 cursor-pointer hover:bg-accent transition-colors ${
                currentConversationId === conv.id ? 'bg-orange-500/10 border-orange-500/30' : ''
              }`}
              onClick={() => onLoadConversation(conv.id)}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <Flame 
                      className="h-3 w-3 flex-shrink-0" 
                      style={{ color: getChakraColor(conv.chakraId) }}
                    />
                    <h4 className="text-sm font-medium truncate">
                      {conv.title}
                    </h4>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <Clock className="h-3 w-3" />
                    <span>
                      {formatDistanceToNow(new Date(conv.updatedAt), { addSuffix: true })}
                    </span>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-6 w-6 flex-shrink-0"
                  onClick={(e) => handleDelete(conv.id, e)}
                >
                  <Trash2 className="h-3 w-3" />
                </Button>
              </div>
              
              {/* Chakra Badge */}
              <Badge 
                variant="outline" 
                className="mt-2 text-xs"
                style={{ 
                  borderColor: getChakraColor(conv.chakraId),
                  color: getChakraColor(conv.chakraId)
                }}
              >
                {CHAKRAS.find(c => c.id === conv.chakraId)?.name || 'Unknown'}
              </Badge>
            </Card>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}
