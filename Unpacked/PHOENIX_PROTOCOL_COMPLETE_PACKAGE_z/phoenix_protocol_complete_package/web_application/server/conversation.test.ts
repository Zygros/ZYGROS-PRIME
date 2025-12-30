import { describe, expect, it, beforeEach } from "vitest";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

type AuthenticatedUser = NonNullable<TrpcContext["user"]>;

function createTestContext(): { ctx: TrpcContext } {
  const user: AuthenticatedUser = {
    id: 1,
    openId: "test-user-123",
    email: "test@phoenix.protocol",
    name: "Test User",
    loginMethod: "manus",
    role: "user",
    createdAt: new Date(),
    updatedAt: new Date(),
    lastSignedIn: new Date(),
  };

  const ctx: TrpcContext = {
    user,
    req: {
      protocol: "https",
      headers: {},
    } as TrpcContext["req"],
    res: {
      clearCookie: () => {},
    } as TrpcContext["res"],
  };

  return { ctx };
}

describe("Conversation Persistence System", () => {
  let caller: ReturnType<typeof appRouter.createCaller>;
  let testConversationId: number;

  beforeEach(() => {
    const { ctx } = createTestContext();
    caller = appRouter.createCaller(ctx);
  });

  describe("conversations.create", () => {
    it("should create a new conversation", async () => {
      const result = await caller.conversations.create({
        title: "Test Conversation About AGI",
        chakraId: 4,
      });

      expect(result).toHaveProperty("id");
      expect(result).toHaveProperty("success", true);
      expect(typeof result.id).toBe("number");
      
      testConversationId = result.id;
    });

    it("should create conversation with default chakra", async () => {
      const result = await caller.conversations.create({
        title: "Default Chakra Test",
        chakraId: 1,
      });

      expect(result).toHaveProperty("id");
      expect(result.success).toBe(true);
    });
  });

  describe("conversations.list", () => {
    it("should list user conversations", async () => {
      // Create a test conversation first
      const created = await caller.conversations.create({
        title: "List Test Conversation",
        chakraId: 3,
      });

      const conversations = await caller.conversations.list();

      expect(Array.isArray(conversations)).toBe(true);
      expect(conversations.length).toBeGreaterThan(0);
      
      const found = conversations.find(c => c.id === created.id);
      expect(found).toBeDefined();
      expect(found?.title).toBe("List Test Conversation");
      expect(found?.chakraId).toBe(3);
    });

    it("should return conversations in descending order by updatedAt", async () => {
      const conversations = await caller.conversations.list();
      
      if (conversations.length > 1) {
        for (let i = 0; i < conversations.length - 1; i++) {
          const current = new Date(conversations[i]!.updatedAt).getTime();
          const next = new Date(conversations[i + 1]!.updatedAt).getTime();
          expect(current).toBeGreaterThanOrEqual(next);
        }
      }
    });
  });

  describe("conversations.addMessage", () => {
    it("should add user message to conversation", async () => {
      // Create conversation
      const conv = await caller.conversations.create({
        title: "Message Test",
        chakraId: 4,
      });

      // Add user message
      const result = await caller.conversations.addMessage({
        conversationId: conv.id,
        type: "user",
        content: "What is the Phoenix Protocol?",
        chakraId: 4,
        ivp: 0,
      });

      expect(result).toHaveProperty("id");
      expect(result).toHaveProperty("success", true);
    });

    it("should add oracle message with IVP and metadata", async () => {
      // Create conversation
      const conv = await caller.conversations.create({
        title: "Oracle Response Test",
        chakraId: 4,
      });

      // Add oracle message
      const result = await caller.conversations.addMessage({
        conversationId: conv.id,
        type: "oracle",
        content: "The Phoenix Protocol is a comprehensive AGI architecture...",
        chakraId: 4,
        ivp: 85,
        metadata: {
          ivp: 85.5,
          layers: 12,
          processingTime: 2500,
        },
      });

      expect(result).toHaveProperty("id");
      expect(result.success).toBe(true);
    });

    it("should reject message for non-existent conversation", async () => {
      await expect(
        caller.conversations.addMessage({
          conversationId: 999999,
          type: "user",
          content: "This should fail",
          ivp: 0,
        })
      ).rejects.toThrow("Conversation not found");
    });
  });

  describe("conversations.get", () => {
    it("should retrieve conversation with all messages", async () => {
      // Create conversation
      const conv = await caller.conversations.create({
        title: "Full Conversation Test",
        chakraId: 5,
      });

      // Add messages
      await caller.conversations.addMessage({
        conversationId: conv.id,
        type: "user",
        content: "First message",
        ivp: 0,
      });

      await caller.conversations.addMessage({
        conversationId: conv.id,
        type: "oracle",
        content: "First response",
        ivp: 75,
      });

      await caller.conversations.addMessage({
        conversationId: conv.id,
        type: "user",
        content: "Second message",
        ivp: 0,
      });

      // Retrieve conversation
      const result = await caller.conversations.get({ id: conv.id });

      expect(result).toHaveProperty("id", conv.id);
      expect(result).toHaveProperty("title", "Full Conversation Test");
      expect(result).toHaveProperty("messages");
      expect(Array.isArray(result.messages)).toBe(true);
      expect(result.messages.length).toBe(3);
      
      // Check message order (should be chronological)
      expect(result.messages[0]?.content).toBe("First message");
      expect(result.messages[1]?.content).toBe("First response");
      expect(result.messages[2]?.content).toBe("Second message");
    });

    it("should reject request for non-existent conversation", async () => {
      await expect(
        caller.conversations.get({ id: 999999 })
      ).rejects.toThrow("Conversation not found");
    });
  });

  describe("conversations.updateTitle", () => {
    it("should update conversation title", async () => {
      // Create conversation
      const conv = await caller.conversations.create({
        title: "Original Title",
        chakraId: 2,
      });

      // Update title
      const result = await caller.conversations.updateTitle({
        id: conv.id,
        title: "Updated Title",
      });

      expect(result.success).toBe(true);

      // Verify update
      const updated = await caller.conversations.get({ id: conv.id });
      expect(updated.title).toBe("Updated Title");
    });
  });

  describe("conversations.delete", () => {
    it("should delete conversation and all messages", async () => {
      // Create conversation with messages
      const conv = await caller.conversations.create({
        title: "To Be Deleted",
        chakraId: 1,
      });

      await caller.conversations.addMessage({
        conversationId: conv.id,
        type: "user",
        content: "Test message",
        ivp: 0,
      });

      // Delete conversation
      const result = await caller.conversations.delete({ id: conv.id });
      expect(result.success).toBe(true);

      // Verify deletion
      await expect(
        caller.conversations.get({ id: conv.id })
      ).rejects.toThrow("Conversation not found");
    });
  });

  describe("Conversation Flow Integration", () => {
    it("should handle complete conversation lifecycle", async () => {
      // 1. Create conversation
      const conv = await caller.conversations.create({
        title: "Complete Lifecycle Test",
        chakraId: 4,
      });
      expect(conv.id).toBeDefined();

      // 2. Add user message
      const userMsg = await caller.conversations.addMessage({
        conversationId: conv.id,
        type: "user",
        content: "Explain the 12-layer cascade",
        chakraId: 4,
        ivp: 0,
      });
      expect(userMsg.success).toBe(true);

      // 3. Add oracle response
      const oracleMsg = await caller.conversations.addMessage({
        conversationId: conv.id,
        type: "oracle",
        content: "The 12-layer cascade is...",
        chakraId: 4,
        ivp: 92,
        metadata: {
          ivp: 92.3,
          layers: 12,
          coherence: 95,
        },
      });
      expect(oracleMsg.success).toBe(true);

      // 4. Retrieve full conversation
      const fullConv = await caller.conversations.get({ id: conv.id });
      expect(fullConv.messages.length).toBe(2);
      expect(fullConv.messages[0]?.type).toBe("user");
      expect(fullConv.messages[1]?.type).toBe("oracle");

      // 5. Update title
      await caller.conversations.updateTitle({
        id: conv.id,
        title: "12-Layer Cascade Discussion",
      });

      // 6. Verify in list
      const list = await caller.conversations.list();
      const found = list.find(c => c.id === conv.id);
      expect(found?.title).toBe("12-Layer Cascade Discussion");

      // 7. Delete conversation
      await caller.conversations.delete({ id: conv.id });
      
      // 8. Verify deletion
      await expect(
        caller.conversations.get({ id: conv.id })
      ).rejects.toThrow();
    });
  });

  describe("Multi-User Isolation", () => {
    it("should not allow access to other users' conversations", async () => {
      // Create conversation as test user
      const conv = await caller.conversations.create({
        title: "Private Conversation",
        chakraId: 3,
      });

      // Create different user context
      const otherUser: AuthenticatedUser = {
        id: 2,
        openId: "other-user-456",
        email: "other@phoenix.protocol",
        name: "Other User",
        loginMethod: "manus",
        role: "user",
        createdAt: new Date(),
        updatedAt: new Date(),
        lastSignedIn: new Date(),
      };

      const otherCtx: TrpcContext = {
        user: otherUser,
        req: { protocol: "https", headers: {} } as TrpcContext["req"],
        res: { clearCookie: () => {} } as TrpcContext["res"],
      };

      const otherCaller = appRouter.createCaller(otherCtx);

      // Try to access first user's conversation
      await expect(
        otherCaller.conversations.get({ id: conv.id })
      ).rejects.toThrow("Conversation not found");
    });
  });
});
