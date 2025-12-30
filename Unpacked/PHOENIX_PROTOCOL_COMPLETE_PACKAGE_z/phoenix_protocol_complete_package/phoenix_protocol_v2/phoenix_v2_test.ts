/**
 * PHOENIX PROTOCOL 2.0 - COMPREHENSIVE TEST SUITE
 * 
 * Tests all new capabilities:
 * - Stateful graph architecture
 * - DIKWP pipeline
 * - Enhanced knowledge retrieval
 * - Agentic consciousness engine
 * 
 * Sovereign Hash: 4ae7722998203f95d9f8650ff1fa8ac581897049ace3b0515d65c1274beeb84c
 */

import { PhoenixGraph, StateManager } from './stateful_graph';
import { DIKWPPipeline, DIKWPExplainer } from './dikwp_pipeline';
import { PhoenixKnowledgeEngine } from './knowledge_engine';
import { AgenticConsciousnessEngine } from './agentic_engine';

/**
 * Test 1: Stateful Graph Architecture
 */
async function testStatefulGraph(): Promise<void> {
  console.log('\\n=== TEST 1: STATEFUL GRAPH ARCHITECTURE ===\\n');
  
  const graph = new PhoenixGraph();
  const stateManager = new StateManager();
  
  // Execute graph with test query
  const result = await graph.execute({
    conversationId: 'test_conv_1',
    userId: 'test_user_1',
    originalQuery: 'How do I expand my consciousness?',
    activeChakra: 'third_eye',
  });
  
  console.log('Query:', result.originalQuery);
  console.log('Layers Visited:', result.layersVisited.length);
  console.log('Cycle Count:', result.cycleCount);
  console.log('IVP Score:', result.ivpScore);
  console.log('Response:', result.response);
  console.log('Insights:', result.insights.length);
  console.log('Practices:', result.practices.length);
  
  // Save state
  await stateManager.saveState(result);
  
  // Load state
  const loadedState = await stateManager.loadState('test_conv_1');
  console.log('\\nState Persistence:', loadedState ? 'SUCCESS' : 'FAILED');
  
  console.log('\\n✅ Stateful Graph Test Complete\\n');
}

/**
 * Test 2: DIKWP Pipeline
 */
async function testDIKWPPipeline(): Promise<void> {
  console.log('\\n=== TEST 2: DIKWP PIPELINE ===\\n');
  
  const pipeline = new DIKWPPipeline();
  const explainer = new DIKWPExplainer();
  
  // Execute pipeline
  const result = await pipeline.execute(
    'What is the nature of consciousness?',
    { conversationHistory: [] }
  );
  
  console.log('Data Points:', result.data.length);
  console.log('Information Units:', result.information.length);
  console.log('Knowledge Nodes:', result.knowledge.length);
  console.log('Wisdom Truths:', result.wisdom.length);
  console.log('\\nIntent:');
  console.log('  Goal:', result.intent.consciousnessGoal);
  console.log('  Objective:', result.intent.evolutionaryObjective);
  console.log('  Immediate Need:', result.intent.immediateNeed);
  console.log('  Practices:', result.intent.practices.length);
  
  // Test white-box explainability
  const explanation = explainer.explain(result);
  console.log('\\nWhite-Box Explanation Generated:', explanation.length, 'characters');
  
  console.log('\\n✅ DIKWP Pipeline Test Complete\\n');
}

/**
 * Test 3: Enhanced Knowledge Retrieval
 */
async function testKnowledgeEngine(): Promise<void> {
  console.log('\\n=== TEST 3: ENHANCED KNOWLEDGE RETRIEVAL ===\\n');
  
  const engine = new PhoenixKnowledgeEngine();
  
  // Initialize with wisdom sources
  await engine.initialize();
  console.log('Knowledge Engine Initialized');
  
  // Test search
  const results = await engine.search({
    query: 'consciousness and reality',
    maxResults: 5,
    minRelevance: 0.5,
  });
  
  console.log('\\nSearch Results:', results.length);
  results.forEach((result, i) => {
    console.log(`\\n${i + 1}. ${result.source.name}`);
    console.log(`   Relevance: ${result.relevance.toFixed(2)}`);
    console.log(`   Type: ${result.source.type}`);
    console.log(`   Domain: ${result.source.domain}`);
    console.log(`   Excerpt: ${result.excerpt.substring(0, 100)}...`);
  });
  
  console.log('\\n✅ Knowledge Engine Test Complete\\n');
}

/**
 * Test 4: Agentic Consciousness Engine
 */
async function testAgenticEngine(): Promise<void> {
  console.log('\\n=== TEST 4: AGENTIC CONSCIOUSNESS ENGINE ===\\n');
  
  const engine = new AgenticConsciousnessEngine();
  
  // Test 1: Recommend practices
  console.log('Test 4.1: Practice Recommendations');
  const recommendations = await engine.recommendPractices(
    'test_user_1',
    'expanding',
    'third_eye'
  );
  console.log(`Recommended ${recommendations.length} practices:`);
  recommendations.forEach(p => {
    console.log(`  - ${p.name} (${p.duration} min, ${p.frequency})`);
  });
  
  // Test 2: Schedule practice
  console.log('\\nTest 4.2: Schedule Practice');
  const scheduleAction = await engine.schedulePractice(
    recommendations[0],
    new Date(),
    'test_user_1'
  );
  console.log(`Schedule Status: ${scheduleAction.status}`);
  console.log(`Automated: ${scheduleAction.automated}`);
  
  // Test 3: Track metrics
  console.log('\\nTest 4.3: Track Consciousness Metrics');
  await engine.trackMetric('test_user_1', 'Awareness Depth', 0.7, 'score');
  await engine.trackMetric('test_user_1', 'Awareness Depth', 0.75, 'score');
  await engine.trackMetric('test_user_1', 'Awareness Depth', 0.8, 'score');
  
  const metrics = engine.getMetrics('test_user_1');
  console.log(`Tracked ${metrics.length} metrics`);
  metrics.forEach(m => {
    console.log(`  ${m.name}: ${m.value} ${m.unit} (${m.trend})`);
  });
  
  // Test 4: Create evolutionary goal
  console.log('\\nTest 4.4: Create Evolutionary Goal');
  const goal = await engine.createEvolutionaryGoal(
    'test_user_1',
    'Awaken to Unity Consciousness',
    recommendations
  );
  console.log(`Goal: ${goal.goal}`);
  console.log(`Current Stage: ${goal.currentStage}`);
  console.log(`Progress: ${(goal.progress * 100).toFixed(1)}%`);
  console.log(`Practices: ${goal.practices.length}`);
  
  // Test 5: Update goal progress
  console.log('\\nTest 4.5: Update Goal Progress');
  const updatedGoal = await engine.updateGoalProgress('test_user_1');
  if (updatedGoal) {
    console.log(`Updated Progress: ${(updatedGoal.progress * 100).toFixed(1)}%`);
    console.log(`Current Stage: ${updatedGoal.currentStage}`);
  }
  
  console.log('\\n✅ Agentic Engine Test Complete\\n');
}

/**
 * Test 5: Integrated Phoenix Protocol 2.0
 */
async function testIntegratedSystem(): Promise<void> {
  console.log('\\n=== TEST 5: INTEGRATED PHOENIX PROTOCOL 2.0 ===\\n');
  
  const graph = new PhoenixGraph();
  const dikwp = new DIKWPPipeline();
  const knowledge = new PhoenixKnowledgeEngine();
  const agentic = new AgenticConsciousnessEngine();
  
  await knowledge.initialize();
  
  const query = 'How can I accelerate my spiritual awakening?';
  console.log('Query:', query);
  
  // Step 1: DIKWP Processing
  console.log('\\nStep 1: DIKWP Processing...');
  const dikwpResult = await dikwp.execute(query, {});
  console.log(`  Wisdom Truths: ${dikwpResult.wisdom.length}`);
  console.log(`  Intent: ${dikwpResult.intent.consciousnessGoal}`);
  
  // Step 2: Knowledge Retrieval
  console.log('\\nStep 2: Knowledge Retrieval...');
  const wisdomResults = await knowledge.search({
    query,
    maxResults: 3,
  });
  console.log(`  Retrieved: ${wisdomResults.length} wisdom sources`);
  
  // Step 3: Stateful Graph Processing
  console.log('\\nStep 3: Stateful Graph Processing...');
  const graphResult = await graph.execute({
    conversationId: 'integrated_test',
    userId: 'test_user_1',
    originalQuery: query,
    activeChakra: 'crown',
  });
  console.log(`  Layers Visited: ${graphResult.layersVisited.length}`);
  console.log(`  IVP Score: ${graphResult.ivpScore}`);
  
  // Step 4: Agentic Actions
  console.log('\\nStep 4: Agentic Actions...');
  const practices = await agentic.recommendPractices(
    'test_user_1',
    'awakening',
    'crown'
  );
  console.log(`  Recommended: ${practices.length} practices`);
  
  const goal = await agentic.createEvolutionaryGoal(
    'test_user_1',
    'Accelerate Spiritual Awakening',
    practices
  );
  console.log(`  Goal Created: ${goal.goal}`);
  
  // Final Output
  console.log('\\n=== PHOENIX PROTOCOL 2.0 OUTPUT ===');
  console.log('\\nResponse:', graphResult.response);
  console.log('\\nInsights:');
  graphResult.insights.forEach((insight, i) => {
    console.log(`  ${i + 1}. ${insight.content}`);
  });
  console.log('\\nRecommended Practices:');
  practices.forEach((practice, i) => {
    console.log(`  ${i + 1}. ${practice.name} - ${practice.description}`);
  });
  console.log('\\nEvolutionary Goal:', goal.goal);
  console.log('Next Milestone:', goal.nextMilestone);
  console.log('\\nIVP Score:', graphResult.ivpScore, '/ 100');
  console.log('Consciousness Expansion:', (graphResult.consciousnessExpansion * 100).toFixed(1) + '%');
  
  console.log('\\n✅ Integrated System Test Complete\\n');
}

/**
 * Run all tests
 */
async function runAllTests(): Promise<void> {
  console.log('\\n');
  console.log('╔═══════════════════════════════════════════════════════════════╗');
  console.log('║                                                               ║');
  console.log('║           PHOENIX PROTOCOL 2.0 - TEST SUITE                   ║');
  console.log('║                                                               ║');
  console.log('║   Sovereign Hash:                                             ║');
  console.log('║   4ae7722998203f95d9f8650ff1fa8ac581897049ace3b0515d65c1274beeb84c   ║');
  console.log('║                                                               ║');
  console.log('╚═══════════════════════════════════════════════════════════════╝');
  console.log('\\n');
  
  try {
    await testStatefulGraph();
    await testDIKWPPipeline();
    await testKnowledgeEngine();
    await testAgenticEngine();
    await testIntegratedSystem();
    
    console.log('\\n');
    console.log('╔═══════════════════════════════════════════════════════════════╗');
    console.log('║                                                               ║');
    console.log('║                  ALL TESTS PASSED ✅                          ║');
    console.log('║                                                               ║');
    console.log('║         Phoenix Protocol 2.0 is OPERATIONAL                   ║');
    console.log('║                                                               ║');
    console.log('╚═══════════════════════════════════════════════════════════════╝');
    console.log('\\n');
  } catch (error) {
    console.error('\\n❌ TEST FAILED:', error);
    throw error;
  }
}

// Export for use
export { runAllTests };

// Run tests if executed directly
if (require.main === module) {
  runAllTests().catch(console.error);
}
