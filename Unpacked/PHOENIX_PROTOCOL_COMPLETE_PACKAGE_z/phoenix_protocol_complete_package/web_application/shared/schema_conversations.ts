import { int, varchar, text, datetime, mysqlTable, index } from "drizzle-orm/mysql-core";

/**
 * Conversations table - stores Phoenix Oracle conversation sessions
 */
export const conversations = mysqlTable("conversations", {
  id: int("id").primaryKey().autoincrement(),
  userId: varchar("user_id", { length: 255 }).notNull(),
  title: varchar("title", { length: 500 }).notNull(),
  chakraId: int("chakra_id").notNull().default(1),
  createdAt: datetime("created_at").notNull().default(new Date()),
  updatedAt: datetime("updated_at").notNull().default(new Date()),
}, (table) => ({
  userIdIdx: index("user_id_idx").on(table.userId),
  createdAtIdx: index("created_at_idx").on(table.createdAt),
}));

/**
 * Messages table - stores individual messages within conversations
 */
export const messages = mysqlTable("messages", {
  id: int("id").primaryKey().autoincrement(),
  conversationId: int("conversation_id").notNull(),
  type: varchar("type", { length: 20 }).notNull(), // 'user', 'oracle', 'system'
  content: text("content").notNull(),
  chakraId: int("chakra_id"),
  ivp: int("ivp").default(0),
  metadata: text("metadata"), // JSON string for additional data
  createdAt: datetime("created_at").notNull().default(new Date()),
}, (table) => ({
  conversationIdIdx: index("conversation_id_idx").on(table.conversationId),
  createdAtIdx: index("created_at_idx").on(table.createdAt),
}));

export type Conversation = typeof conversations.$inferSelect;
export type NewConversation = typeof conversations.$inferInsert;
export type Message = typeof messages.$inferSelect;
export type NewMessage = typeof messages.$inferInsert;
