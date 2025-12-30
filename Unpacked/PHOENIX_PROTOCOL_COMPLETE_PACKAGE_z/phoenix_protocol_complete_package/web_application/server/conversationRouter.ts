import { z } from "zod";
import { eq, desc, asc } from "drizzle-orm";
import { getDb } from "./db";
import { conversations, messages } from "../drizzle/schema";
import { protectedProcedure, router } from "./_core/trpc";

export const conversationRouter = router({
  /**
   * Create a new conversation
   */
  create: protectedProcedure
    .input(z.object({
      title: z.string(),
      chakraId: z.number().default(1),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = await getDb();
      if (!db) throw new Error("Database not available");
      
      const result = await db.insert(conversations).values({
        userId: ctx.user.openId,
        title: input.title,
        chakraId: input.chakraId,
      });
      
      return { id: Number(result[0].insertId), success: true };
    }),

  /**
   * Get all conversations for current user
   */
  list: protectedProcedure
    .query(async ({ ctx }) => {
      const db = await getDb();
      if (!db) throw new Error("Database not available");
      
      return await db
        .select()
        .from(conversations)
        .where(eq(conversations.userId, ctx.user.openId))
        .orderBy(desc(conversations.updatedAt));
    }),

  /**
   * Get a specific conversation with all messages
   */
  get: protectedProcedure
    .input(z.object({
      id: z.number(),
    }))
    .query(async ({ input, ctx }) => {
      const db = await getDb();
      if (!db) throw new Error("Database not available");
      
      const [conversation] = await db
        .select()
        .from(conversations)
        .where(eq(conversations.id, input.id));

      if (!conversation || conversation.userId !== ctx.user.openId) {
        throw new Error("Conversation not found");
      }

      const conversationMessages = await db
        .select()
        .from(messages)
        .where(eq(messages.conversationId, input.id))
        .orderBy(asc(messages.createdAt));

      return {
        ...conversation,
        messages: conversationMessages,
      };
    }),

  /**
   * Add a message to a conversation
   */
  addMessage: protectedProcedure
    .input(z.object({
      conversationId: z.number(),
      type: z.enum(["user", "oracle", "system"]),
      content: z.string(),
      chakraId: z.number().optional(),
      ivp: z.number().optional(),
      metadata: z.record(z.string(), z.any()).optional(),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = await getDb();
      if (!db) throw new Error("Database not available");
      
      // Verify conversation belongs to user
      const [conversation] = await db
        .select()
        .from(conversations)
        .where(eq(conversations.id, input.conversationId));

      if (!conversation || conversation.userId !== ctx.user.openId) {
        throw new Error("Conversation not found");
      }

      // Add message
      const result = await db.insert(messages).values({
        conversationId: input.conversationId,
        type: input.type,
        content: input.content,
        chakraId: input.chakraId,
        ivp: input.ivp,
        metadata: input.metadata ? JSON.stringify(input.metadata) : null,
      });
      
      const messageId = Number(result[0].insertId);

      // Update conversation updatedAt
      await db
        .update(conversations)
        .set({ updatedAt: new Date() })
        .where(eq(conversations.id, input.conversationId));

      return { id: messageId, success: true };
    }),

  /**
   * Delete a conversation
   */
  delete: protectedProcedure
    .input(z.object({
      id: z.number(),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = await getDb();
      if (!db) throw new Error("Database not available");
      
      // Verify conversation belongs to user
      const [conversation] = await db
        .select()
        .from(conversations)
        .where(eq(conversations.id, input.id));

      if (!conversation || conversation.userId !== ctx.user.openId) {
        throw new Error("Conversation not found");
      }

      // Delete messages first
      await db.delete(messages).where(eq(messages.conversationId, input.id));

      // Delete conversation
      await db.delete(conversations).where(eq(conversations.id, input.id));

      return { success: true };
    }),

  /**
   * Update conversation title
   */
  updateTitle: protectedProcedure
    .input(z.object({
      id: z.number(),
      title: z.string(),
    }))
    .mutation(async ({ input, ctx }) => {
      const db = await getDb();
      if (!db) throw new Error("Database not available");
      
      // Verify conversation belongs to user
      const [conversation] = await db
        .select()
        .from(conversations)
        .where(eq(conversations.id, input.id));

      if (!conversation || conversation.userId !== ctx.user.openId) {
        throw new Error("Conversation not found");
      }

      await db
        .update(conversations)
        .set({ title: input.title, updatedAt: new Date() })
        .where(eq(conversations.id, input.id));

      return { success: true };
    }),
});
