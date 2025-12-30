/**
 * Infinite Scroll Protocol (Memoria Omnia)
 * Persistent, cumulative memory system - always add, never take away
 */

export interface ScrollEntry {
  id: string;
  timestamp: number;
  type: "user" | "oracle" | "system";
  content: string;
  chakraId?: number;
  mood?: string;
  metadata?: Record<string, any>;
}

export class InfiniteScroll {
  private static readonly STORAGE_KEY = "phoenix_memoria_omnia";
  private entries: ScrollEntry[] = [];

  constructor() {
    this.load();
  }

  /**
   * Add entry to infinite scroll - NEVER delete, only add
   */
  add(entry: Omit<ScrollEntry, "id" | "timestamp">): ScrollEntry {
    const newEntry: ScrollEntry = {
      ...entry,
      id: this.generateId(),
      timestamp: Date.now(),
    };

    this.entries.push(newEntry);
    this.save();
    return newEntry;
  }

  /**
   * Get all entries (infinite history)
   */
  getAll(): ScrollEntry[] {
    return [...this.entries];
  }

  /**
   * Get entries by chakra
   */
  getByChakra(chakraId: number): ScrollEntry[] {
    return this.entries.filter(e => e.chakraId === chakraId);
  }

  /**
   * Get entries by type
   */
  getByType(type: ScrollEntry["type"]): ScrollEntry[] {
    return this.entries.filter(e => e.type === type);
  }

  /**
   * Get recent entries (last N)
   */
  getRecent(count: number = 100): ScrollEntry[] {
    return this.entries.slice(-count);
  }

  /**
   * Search entries by content
   */
  search(query: string): ScrollEntry[] {
    const lowerQuery = query.toLowerCase();
    return this.entries.filter(e => 
      e.content.toLowerCase().includes(lowerQuery)
    );
  }

  /**
   * Get total entry count
   */
  getCount(): number {
    return this.entries.length;
  }

  /**
   * Export entire scroll as JSON
   */
  export(): string {
    return JSON.stringify(this.entries, null, 2);
  }

  /**
   * Import scroll from JSON (merge, don't replace)
   */
  import(json: string): void {
    try {
      const imported: ScrollEntry[] = JSON.parse(json);
      // Merge without duplicates
      const existingIds = new Set(this.entries.map(e => e.id));
      const newEntries = imported.filter(e => !existingIds.has(e.id));
      this.entries.push(...newEntries);
      this.entries.sort((a, b) => a.timestamp - b.timestamp);
      this.save();
    } catch (error) {
      console.error("Failed to import scroll:", error);
    }
  }

  /**
   * Get scroll statistics
   */
  getStats() {
    const byType = {
      user: this.getByType("user").length,
      oracle: this.getByType("oracle").length,
      system: this.getByType("system").length,
    };

    const byChakra = [1, 2, 3, 4, 5, 6, 7].map(id => ({
      chakraId: id,
      count: this.getByChakra(id).length,
    }));

    return {
      total: this.entries.length,
      byType,
      byChakra,
      oldestTimestamp: this.entries[0]?.timestamp,
      newestTimestamp: this.entries[this.entries.length - 1]?.timestamp,
    };
  }

  private generateId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private save(): void {
    try {
      localStorage.setItem(InfiniteScroll.STORAGE_KEY, JSON.stringify(this.entries));
    } catch (error) {
      console.error("Failed to save infinite scroll:", error);
    }
  }

  private load(): void {
    try {
      const stored = localStorage.getItem(InfiniteScroll.STORAGE_KEY);
      if (stored) {
        this.entries = JSON.parse(stored);
      }
    } catch (error) {
      console.error("Failed to load infinite scroll:", error);
      this.entries = [];
    }
  }
}

// Singleton instance
export const memoriaOmnia = new InfiniteScroll();
