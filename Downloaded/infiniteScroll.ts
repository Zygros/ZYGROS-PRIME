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