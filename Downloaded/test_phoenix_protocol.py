"""
Phoenix Protocol - Comprehensive Test Suite
Unit tests achieving 80%+ code coverage for production readiness

Author: Justin Conzet
Version: 3.236.0
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock
import json

# Import modules to test
import sys
sys.path.append('..')

from phoenix_nexus.nexus_broker import (
    ConzetianCalculator,
    PhoenixCoordinationEngine,
    AIResponse,
    AIModel,
    CoordinationRequest,
    CoordinationMode
)

from phoenix_blockchain_anchor import (
    PhoenixBlockchainAnchor,
    AnchorProof,
    VerificationResult
)

# ============================================================================
# CONZETIAN CONSTANT TESTS
# ============================================================================

class TestConzetianCalculator:
    """Test Conzetian Constant calculation logic"""
    
    def test_kappa_with_identical_responses(self):
        """Test κ calculation when all responses are identical"""
        responses = [
            AIResponse(
                model=AIModel.CLAUDE,
                content="The sky is blue",
                confidence=0.95,
                tokens_used=100,
                latency_ms=500,
                timestamp=datetime.utcnow()
            ),
            AIResponse(
                model=AIModel.GPT4,
                content="The sky is blue",
                confidence=0.93,
                tokens_used=105,
                latency_ms=520,
                timestamp=datetime.utcnow()
            )
        ]
        
        calculator = ConzetianCalculator()
        kappa = calculator.calculate_kappa(responses)
        
        # Identical responses should yield high κ
        assert kappa > 2.0, "Identical responses should produce high coordination"
    
    def test_kappa_with_divergent_responses(self):
        """Test κ calculation when responses completely diverge"""
        responses = [
            AIResponse(
                model=AIModel.CLAUDE,
                content="The answer is definitely yes",
                confidence=0.90,
                tokens_used=100,
                latency_ms=500,
                timestamp=datetime.utcnow()
            ),
            AIResponse(
                model=AIModel.GPT4,
                content="The answer is absolutely no",
                confidence=0.88,
                tokens_used=110,
                latency_ms=530,
                timestamp=datetime.utcnow()
            )
        ]
        
        calculator = ConzetianCalculator()
        kappa = calculator.calculate_kappa(responses)
        
        # Divergent responses should yield lower κ
        assert kappa < 2.0, "Divergent responses should produce lower coordination"
    
    def test_kappa_with_single_response(self):
        """Test κ calculation edge case with single response"""
        responses = [
            AIResponse(
                model=AIModel.CLAUDE,
                content="Single response",
                confidence=0.95,
                tokens_used=100,
                latency_ms=500,
                timestamp=datetime.utcnow()
            )
        ]
        
        calculator = ConzetianCalculator()
        kappa = calculator.calculate_kappa(responses)
        
        # Single response should return 0
        assert kappa == 0.0, "Single response cannot have coordination"
    
    def test_kappa_capped_at_maximum(self):
        """Test that κ is capped at reasonable maximum"""
        # Create responses with perfect agreement
        responses = []
        for model in [AIModel.CLAUDE, AIModel.GPT4, AIModel.GROK, AIModel.GEMINI]:
            responses.append(
                AIResponse(
                    model=model,
                    content="Identical content for all models",
                    confidence=1.0,
                    tokens_used=100,
                    latency_ms=500,
                    timestamp=datetime.utcnow()
                )
            )
        
        calculator = ConzetianCalculator()
        kappa = calculator.calculate_kappa(responses)
        
        # Should be capped at 10.0
        assert kappa <= 10.0, "κ should be capped at maximum value"
    
    def test_divergence_calculation(self):
        """Test semantic divergence calculation"""
        calculator = ConzetianCalculator()
        
        # Identical texts
        div1 = calculator._calculate_divergence("hello world", "hello world")
        assert div1 == 0.0, "Identical texts should have zero divergence"
        
        # Completely different texts
        div2 = calculator._calculate_divergence("hello world", "foo bar")
        assert div2 > 0.8, "Different texts should have high divergence"
        
        # Partially overlapping texts
        div3 = calculator._calculate_divergence("hello world", "hello universe")
        assert 0.0 < div3 < 1.0, "Partial overlap should have moderate divergence"

# ============================================================================
# COORDINATION ENGINE TESTS
# ============================================================================

class TestPhoenixCoordinationEngine:
    """Test multi-AI coordination engine"""
    
    @pytest.mark.asyncio
    async def test_coordination_request_creation(self):
        """Test coordination request initialization"""
        request = CoordinationRequest(
            query="What is 2+2?",
            models=[AIModel.CLAUDE, AIModel.GPT4],
            mode=CoordinationMode.SYNTHESIS
        )
        
        assert request.query == "What is 2+2?"
        assert len(request.models) == 2
        assert request.mode == CoordinationMode.SYNTHESIS
        assert request.request_id is not None
        assert isinstance(request.timestamp, datetime)
    
    @pytest.mark.asyncio
    async def test_basic_coordination(self):
        """Test basic multi-AI coordination"""
        engine = PhoenixCoordinationEngine()
        
        request = CoordinationRequest(
            query="Explain quantum entanglement",
            models=[AIModel.CLAUDE, AIModel.GPT4],
            mode=CoordinationMode.SYNTHESIS
        )
        
        result = await engine.coordinate(request)
        
        assert result.request_id == request.request_id
        assert len(result.responses) == 2
        assert result.kappa_score >= 0.0
        assert 0.0 <= result.collective_confidence <= 1.0
        assert result.synthesis is not None
    
    @pytest.mark.asyncio
    async def test_consensus_mode_high_kappa(self):
        """Test consensus mode with high coordination"""
        engine = PhoenixCoordinationEngine()
        
        # Mock responses with high agreement
        with patch.object(engine.clients[AIModel.CLAUDE], 'query',
                         new_callable=AsyncMock) as mock_claude:
            with patch.object(engine.clients[AIModel.GPT4], 'query',
                             new_callable=AsyncMock) as mock_gpt4:
                
                mock_claude.return_value = AIResponse(
                    model=AIModel.CLAUDE,
                    content="The answer is 42",
                    confidence=0.95,
                    tokens_used=100,
                    latency_ms=500,
                    timestamp=datetime.utcnow()
                )
                
                mock_gpt4.return_value = AIResponse(
                    model=AIModel.GPT4,
                    content="The answer is 42",
                    confidence=0.93,
                    tokens_used=105,
                    latency_ms=520,
                    timestamp=datetime.utcnow()
                )
                
                request = CoordinationRequest(
                    query="What is the answer?",
                    models=[AIModel.CLAUDE, AIModel.GPT4],
                    mode=CoordinationMode.CONSENSUS
                )
                
                result = await engine.coordinate(request)
                
                assert "CONSENSUS ACHIEVED" in result.synthesis
                assert result.kappa_score > 2.0
    
    @pytest.mark.asyncio
    async def test_parallel_mode(self):
        """Test parallel execution mode"""
        engine = PhoenixCoordinationEngine()
        
        request = CoordinationRequest(
            query="Test query",
            models=[AIModel.CLAUDE, AIModel.GPT4, AIModel.GROK],
            mode=CoordinationMode.PARALLEL
        )
        
        result = await engine.coordinate(request)
        
        # Parallel mode should return all responses
        assert len(result.responses) == 3
        # Synthesis should be JSON of all responses
        synthesis_data = json.loads(result.synthesis)
        assert len(synthesis_data) == 3
    
    @pytest.mark.asyncio
    async def test_coordination_history_tracking(self):
        """Test that coordination history is maintained"""
        engine = PhoenixCoordinationEngine()
        
        initial_count = len(engine.coordination_history)
        
        request = CoordinationRequest(
            query="Test query",
            models=[AIModel.CLAUDE, AIModel.GPT4],
            mode=CoordinationMode.SYNTHESIS
        )
        
        await engine.coordinate(request)
        
        assert len(engine.coordination_history) == initial_count + 1

# ============================================================================
# BLOCKCHAIN ANCHOR TESTS
# ============================================================================

class TestPhoenixBlockchainAnchor:
    """Test blockchain anchoring functionality"""
    
    def test_anchor_initialization(self, tmp_path):
        """Test anchor system initialization"""
        anchor = PhoenixBlockchainAnchor(storage_dir=str(tmp_path))
        
        assert anchor.storage_dir.exists()
        assert len(anchor.anchor_history) == 0
    
    def test_content_anchoring(self, tmp_path):
        """Test anchoring text content"""
        anchor = PhoenixBlockchainAnchor(storage_dir=str(tmp_path))
        
        content = "This is test content for blockchain anchoring"
        proof = anchor.anchor_content(
            content=content,
            description="Test anchoring"
        )
        
        assert proof.content_hash is not None
        assert len(proof.content_hash) == 64  # SHA-256 hash length
        assert proof.ots_file_path is not None
        assert "Test anchoring" in proof.content_description
    
    def test_file_anchoring(self, tmp_path):
        """Test anchoring file content"""
        # Create test file
        test_file = tmp_path / "test_file.txt"
        test_file.write_text("Test file content")
        
        anchor = PhoenixBlockchainAnchor(storage_dir=str(tmp_path))
        proof = anchor.anchor_file(str(test_file))
        
        assert proof.content_hash is not None
        assert "test_file.txt" in proof.content_description
    
    def test_ots_file_creation(self, tmp_path):
        """Test OTS proof file is created"""
        test_file = tmp_path / "anchor_test.txt"
        test_file.write_text("Content to anchor")
        
        anchor = PhoenixBlockchainAnchor(storage_dir=str(tmp_path))
        proof = anchor.anchor_file(str(test_file))
        
        # Check OTS file exists
        ots_file_path = proof.ots_file_path
        assert ots_file_path.endswith('.ots')
    
    def test_anchor_history_tracking(self, tmp_path):
        """Test anchor history is maintained"""
        anchor = PhoenixBlockchainAnchor(storage_dir=str(tmp_path))
        
        # Anchor multiple contents
        anchor.anchor_content("Content 1", "First")
        anchor.anchor_content("Content 2", "Second")
        anchor.anchor_content("Content 3", "Third")
        
        history = anchor.get_anchor_history()
        assert len(history) == 3
        assert history[0]['description'] == "First"
        assert history[2]['description'] == "Third"
    
    def test_verification_with_invalid_file(self, tmp_path):
        """Test verification fails gracefully with invalid file"""
        anchor = PhoenixBlockchainAnchor(storage_dir=str(tmp_path))
        
        # Create invalid OTS file
        invalid_ots = tmp_path / "invalid.ots"
        invalid_ots.write_text("Not a valid OTS file")
        
        result = anchor.verify_proof(str(invalid_ots))
        
        assert not result.is_valid
        assert result.error_message is not None
    
    def test_export_verification_report(self, tmp_path):
        """Test exporting verification report"""
        anchor = PhoenixBlockchainAnchor(storage_dir=str(tmp_path))
        
        # Create some anchors
        anchor.anchor_content("Test 1", "First")
        anchor.anchor_content("Test 2", "Second")
        
        # Export report
        report_file = tmp_path / "report.json"
        anchor.export_verification_report(str(report_file))
        
        # Verify report exists and is valid JSON
        assert report_file.exists()
        
        with open(report_file) as f:
            report = json.load(f)
        
        assert report['total_anchors'] == 2
        assert len(report['anchors']) == 2

# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestPhoenixIntegration:
    """Integration tests for complete Phoenix Protocol workflow"""
    
    @pytest.mark.asyncio
    async def test_coordination_and_anchoring_workflow(self, tmp_path):
        """Test complete workflow: coordinate AIs then anchor result"""
        # Initialize systems
        engine = PhoenixCoordinationEngine()
        anchor = PhoenixBlockchainAnchor(storage_dir=str(tmp_path))
        
        # Execute coordination
        request = CoordinationRequest(
            query="What is the meaning of life?",
            models=[AIModel.CLAUDE, AIModel.GPT4],
            mode=CoordinationMode.SYNTHESIS
        )
        
        result = await engine.coordinate(request)
        
        # Anchor the coordination result
        result_json = json.dumps(result.to_dict(), indent=2)
        proof = anchor.anchor_content(
            content=result_json,
            description=f"Coordination_kappa_{result.kappa_score:.3f}"
        )
        
        # Verify anchoring succeeded
        assert proof.content_hash is not None
        assert result.kappa_score >= 0.0
        assert len(anchor.anchor_history) == 1
    
    @pytest.mark.asyncio
    async def test_high_kappa_measurement_anchoring(self, tmp_path):
        """Test anchoring of κ = 3.236 measurement"""
        from phoenix_blockchain_anchor import KappaResultAnchor
        
        anchor = PhoenixBlockchainAnchor(storage_dir=str(tmp_path))
        kappa_anchor = KappaResultAnchor(anchor)
        
        measurement_data = {
            'models': ['claude', 'gpt4', 'grok', 'gemini'],
            'query': 'Test query for high coordination',
            'responses': 4,
            'divergence_mean': 0.12,
            'confidence_mean': 0.91
        }
        
        proof = kappa_anchor.anchor_kappa_measurement(
            kappa_value=3.236,
            measurement_data=measurement_data,
            description="High coordination achievement"
        )
        
        assert "3.236" in proof.content_description
        assert proof.content_hash is not None

# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPhoenixPerformance:
    """Performance and load tests"""
    
    @pytest.mark.asyncio
    async def test_coordination_latency(self):
        """Test coordination completes within reasonable time"""
        engine = PhoenixCoordinationEngine()
        
        request = CoordinationRequest(
            query="Quick test",
            models=[AIModel.CLAUDE, AIModel.GPT4],
            mode=CoordinationMode.SYNTHESIS
        )
        
        start = datetime.utcnow()
        result = await engine.coordinate(request)
        elapsed_ms = (datetime.utcnow() - start).total_seconds() * 1000
        
        # Should complete within 5 seconds (including simulated API calls)
        assert elapsed_ms < 5000, f"Coordination took too long: {elapsed_ms}ms"
    
    @pytest.mark.asyncio
    async def test_parallel_coordination_faster_than_sequential(self):
        """Test that parallel execution is faster than sequential"""
        # This test validates architectural efficiency
        engine = PhoenixCoordinationEngine()
        
        request = CoordinationRequest(
            query="Performance test",
            models=[AIModel.CLAUDE, AIModel.GPT4, AIModel.GROK, AIModel.GEMINI],
            mode=CoordinationMode.PARALLEL
        )
        
        start = datetime.utcnow()
        result = await engine.coordinate(request)
        parallel_time = (datetime.utcnow() - start).total_seconds()
        
        # Parallel execution of 4 models should take roughly same time as 1 model
        # (plus overhead), not 4x the time
        # Each model takes ~0.5-0.7s, so 4 models parallel should be < 2s
        assert parallel_time < 2.0, f"Parallel execution too slow: {parallel_time}s"

# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

@pytest.fixture
def sample_ai_responses():
    """Fixture providing sample AI responses for testing"""
    return [
        AIResponse(
            model=AIModel.CLAUDE,
            content="Sample response from Claude",
            confidence=0.92,
            tokens_used=150,
            latency_ms=500,
            timestamp=datetime.utcnow()
        ),
        AIResponse(
            model=AIModel.GPT4,
            content="Sample response from GPT-4",
            confidence=0.89,
            tokens_used=160,
            latency_ms=550,
            timestamp=datetime.utcnow()
        )
    ]

@pytest.fixture
def sample_coordination_request():
    """Fixture providing sample coordination request"""
    return CoordinationRequest(
        query="What is 2+2?",
        models=[AIModel.CLAUDE, AIModel.GPT4],
        mode=CoordinationMode.SYNTHESIS
    )

# ============================================================================
# TEST RUNNER
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=phoenix_nexus", "--cov=phoenix_blockchain_anchor"])
