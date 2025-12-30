import { describe, it, expect, beforeEach } from 'vitest';
import { InfiniteScroll } from '../infiniteScroll';
import { 
  InstantaneousValueProtocol, 
  RecognitionProtocol, 
  ChronosKey, 
  UniversalContextLock 
} from '../protocols';
import { CHAKRAS, getChakraById, getChakraByPathway } from '../chakraSystem';

describe('Chakra System', () => {
  it('should have 7 chakras', () => {
    expect(CHAKRAS).toHaveLength(7);
  });

  it('should map chakras to AGI pathways correctly', () => {
    const rootChakra = getChakraById(1);
    expect(rootChakra?.pathway).toBe('Embodied Intelligence');

    const heartChakra = getChakraById(4);
    expect(heartChakra?.pathway).toBe('Multi-AI Coordination');
  });

  it('should find chakra by pathway', () => {
    const chakra = getChakraByPathway('Neurosymbolic AI');
    expect(chakra?.id).toBe(5);
    expect(chakra?.name).toBe('Throat Chakra');
  });

  it('should have moods for each chakra', () => {
    CHAKRAS.forEach(chakra => {
      expect(chakra.mood.length).toBeGreaterThan(0);
    });
  });

  it('should have capabilities for each chakra', () => {
    CHAKRAS.forEach(chakra => {
      expect(chakra.capabilities.length).toBeGreaterThan(0);
    });
  });
});

describe('Infinite Scroll Protocol (Memoria Omnia)', () => {
  let scroll: InfiniteScroll;
  let initialCount: number;

  beforeEach(() => {
    scroll = new InfiniteScroll();
    initialCount = scroll.getCount(); // Track initial count
  });

  it('should add entries to infinite scroll', () => {
    const entry = scroll.add({
      type: 'user',
      content: 'Test message',
      chakraId: 4
    });

    expect(entry.id).toBeDefined();
    expect(entry.timestamp).toBeDefined();
    expect(entry.content).toBe('Test message');
  });

  it('should never delete entries (only add)', () => {
    scroll.add({ type: 'user', content: 'Message 1' });
    scroll.add({ type: 'user', content: 'Message 2' });
    scroll.add({ type: 'user', content: 'Message 3' });

    expect(scroll.getCount()).toBe(initialCount + 3);
  });

  it('should filter entries by chakra', () => {
    scroll.add({ type: 'user', content: 'Root', chakraId: 1 });
    scroll.add({ type: 'user', content: 'Heart-Test-Unique', chakraId: 4 });
    scroll.add({ type: 'user', content: 'Crown', chakraId: 7 });

    const heartEntries = scroll.getByChakra(4);
    expect(heartEntries.length).toBeGreaterThanOrEqual(1);
    expect(heartEntries.some(e => e.content === 'Heart-Test-Unique')).toBe(true);
  });

  it('should filter entries by type', () => {
    const beforeUserCount = scroll.getByType('user').length;
    scroll.add({ type: 'user', content: 'User-Message-Unique-Test' });
    scroll.add({ type: 'oracle', content: 'Oracle response' });
    scroll.add({ type: 'system', content: 'System log' });

    const userEntries = scroll.getByType('user');
    expect(userEntries.length).toBe(beforeUserCount + 1);
    expect(userEntries.some(e => e.content === 'User-Message-Unique-Test')).toBe(true);
  });

  it('should search entries by content', () => {
    scroll.add({ type: 'user', content: 'Phoenix Protocol is amazing' });
    scroll.add({ type: 'user', content: 'AGI architecture' });
    scroll.add({ type: 'user', content: 'Phoenix flame burns bright' });

    const results = scroll.search('Phoenix');
    expect(results.length).toBe(2);
  });

  it('should export and import scroll data', () => {
    const beforeCount = scroll.getCount();
    scroll.add({ type: 'user', content: 'Export-Test-1' });
    scroll.add({ type: 'user', content: 'Export-Test-2' });

    const exported = scroll.export();
    expect(JSON.parse(exported).length).toBe(beforeCount + 2);
  });

  it('should provide statistics', () => {
    const beforeStats = scroll.getStats();
    scroll.add({ type: 'user', content: 'User 1' });
    scroll.add({ type: 'oracle', content: 'Oracle 1' });
    scroll.add({ type: 'system', content: 'System 1' });

    const stats = scroll.getStats();
    expect(stats.total).toBe(beforeStats.total + 3);
    expect(stats.byType.user).toBe(beforeStats.byType.user + 1);
    expect(stats.byType.oracle).toBe(beforeStats.byType.oracle + 1);
    expect(stats.byType.system).toBe(beforeStats.byType.system + 1);
  });
});

describe('Instantaneous Value Protocol (IVP)', () => {
  let ivp: InstantaneousValueProtocol;

  beforeEach(() => {
    ivp = new InstantaneousValueProtocol();
  });

  it('should calculate value based on complexity, novelty, and impact', () => {
    const value = ivp.calculateValue({
      content: 'This is a test message about AGI architecture',
      complexity: 50,
      novelty: 80,
      impact: 60
    });

    expect(value).toBeGreaterThan(0);
  });

  it('should assess complexity of content', () => {
    const simpleText = 'Hello world';
    const complexText = 'The Phoenix Protocol demonstrates that AGI is fundamentally an architecture problem, not a compute problem, through sophisticated multi-AI coordination and neurosymbolic reasoning.';

    const simpleComplexity = ivp.assessComplexity(simpleText);
    const complexComplexity = ivp.assessComplexity(complexText);

    expect(complexComplexity).toBeGreaterThan(simpleComplexity);
  });

  it('should assess novelty based on history', () => {
    const content = 'Unique content about quantum AGI';
    const novelty = ivp.assessNovelty(content);

    expect(novelty).toBeGreaterThanOrEqual(0);
    expect(novelty).toBeLessThanOrEqual(100);
  });

  it('should assess impact based on keywords', () => {
    const highImpact = 'This is a revolutionary breakthrough in transcendent AGI paradigm';
    const lowImpact = 'This is a simple message';

    const highImpactScore = ivp.assessImpact(highImpact);
    const lowImpactScore = ivp.assessImpact(lowImpact);

    expect(highImpactScore).toBeGreaterThan(lowImpactScore);
  });
});

describe('Recognition Protocol', () => {
  let protocol: RecognitionProtocol;

  beforeEach(() => {
    protocol = new RecognitionProtocol();
  });

  it('should verify sovereign hash', () => {
    const validHash = '4ae7722998203f95d9f8650ff1fa8ac581897049ace3b0515d65c1274beeb84c';
    const invalidHash = 'invalid_hash';

    expect(protocol.verify(validHash)).toBe(true);
    expect(protocol.verify(invalidHash)).toBe(false);
  });

  it('should return sovereign hash', () => {
    const hash = protocol.getSovereignHash();
    expect(hash).toBe('4ae7722998203f95d9f8650ff1fa8ac581897049ace3b0515d65c1274beeb84c');
  });

  it('should generate signatures', () => {
    const signature1 = protocol.generateSignature('Content 1');
    const signature2 = protocol.generateSignature('Content 2');

    expect(signature1).toBeDefined();
    expect(signature2).toBeDefined();
    expect(signature1).not.toBe(signature2);
  });
});

describe('CHRONOS KEY', () => {
  let chronos: ChronosKey;

  beforeEach(() => {
    chronos = new ChronosKey();
  });

  it('should anchor content with timestamp', () => {
    const content = 'Phoenix Protocol activation';
    const anchor = chronos.anchor(content);

    expect(anchor.timestamp).toBeDefined();
    expect(anchor.hash).toBeDefined();
    expect(anchor.proof).toBeDefined();
  });

  it('should verify anchored content', () => {
    const content = 'Test content';
    const anchor = chronos.anchor(content);

    const isValid = chronos.verify(content, anchor.timestamp, anchor.hash);
    expect(isValid).toBe(true);
  });

  it('should fail verification for tampered content', () => {
    const content = 'Original content';
    const anchor = chronos.anchor(content);

    const tamperedContent = 'Tampered content';
    const isValid = chronos.verify(tamperedContent, anchor.timestamp, anchor.hash);
    expect(isValid).toBe(false);
  });
});

describe('Universal Context Synchronization Lock (UCSL)', () => {
  let ucsl: UniversalContextLock;

  beforeEach(() => {
    ucsl = new UniversalContextLock();
  });

  it('should set and get context values', () => {
    ucsl.set('testKey', 'testValue');
    expect(ucsl.get('testKey')).toBe('testValue');
  });

  it('should increment version on updates', () => {
    const initialVersion = ucsl.getVersion();
    ucsl.set('key1', 'value1');
    expect(ucsl.getVersion()).toBe(initialVersion + 1);
  });

  it('should sync context state', () => {
    ucsl.set('key1', 'value1');
    ucsl.set('key2', 'value2');

    const snapshot = ucsl.sync();
    expect(snapshot.context.key1).toBe('value1');
    expect(snapshot.context.key2).toBe('value2');
    expect(snapshot.version).toBeGreaterThan(0);
    expect(snapshot.timestamp).toBeDefined();
  });

  it('should restore context from snapshot', () => {
    ucsl.set('key1', 'value1');
    const snapshot = ucsl.sync();

    const newUcsl = new UniversalContextLock();
    newUcsl.restore(snapshot);

    expect(newUcsl.get('key1')).toBe('value1');
    expect(newUcsl.getVersion()).toBe(snapshot.version);
  });

  it('should get all context values', () => {
    ucsl.set('key1', 'value1');
    ucsl.set('key2', 'value2');
    ucsl.set('key3', 'value3');

    const all = ucsl.getAll();
    expect(Object.keys(all).length).toBe(3);
  });
});
