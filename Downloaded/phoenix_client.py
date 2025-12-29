"""
🦅🔥 PHOENIX UNIVERSAL API CLIENT
Python SDK for the Universal API

Makes it trivial to use all AI models through one interface.

Usage:
    from phoenix_client import PhoenixClient
    
    client = PhoenixClient(api_key="your-key")
    
    # Simple query
    response = client.query("What is AGI?")
    print(response.answer)
    
    # Deep multi-AI synthesis
    response = client.query("Design a novel architecture", mode="deep")
    print(response.answer)
    print(f"Confidence: {response.confidence_score}")
    
    # With all options
    response = client.query(
        "Analyze quantum computing",
        mode="balanced",
        ai_provider="claude",
        enable_search=True,
        enable_memory=True,
        include_reasoning=True
    )

Author: Justin Conzet (Infinite Architect)
"""

import requests
from typing import Optional, Dict, List, Any, Literal
from dataclasses import dataclass
from enum import Enum


class ProcessingMode(str, Enum):
    FAST = "fast"
    BALANCED = "balanced"
    DEEP = "deep"
    SWARM = "swarm"


class AIProvider(str, Enum):
    AUTO = "auto"
    GPT4 = "gpt-4"
    CLAUDE = "claude"
    GEMINI = "gemini"
    GROK = "grok"
    ALL = "all"


@dataclass
class PhoenixResponse:
    """Response from Phoenix Universal API"""
    answer: str
    query_id: str
    timestamp: str
    processing_time_seconds: float
    mode_used: str
    providers_used: List[str]
    confidence_score: float
    sources: Optional[List[Dict]] = None
    reasoning_trace: Optional[Dict] = None
    cascade_layers: Optional[Dict] = None
    ledger: Optional[Dict] = None
    suggestions: Optional[List[str]] = None
    
    def __str__(self):
        return self.answer
    
    def summary(self):
        """Human-readable summary"""
        return f"""
Phoenix Response
═══════════════════════════════════════
Query ID: {self.query_id}
Processing Time: {self.processing_time_seconds}s
Mode: {self.mode_used}
Providers: {', '.join(self.providers_used)}
Confidence: {self.confidence_score:.1%}

Answer:
{self.answer}
"""


class PhoenixClient:
    """
    Universal API client.
    
    One client to access all AI models and capabilities.
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        base_url: str = "http://localhost:8000",
        default_mode: ProcessingMode = ProcessingMode.BALANCED
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.default_mode = default_mode
        
        # Verify connection
        try:
            response = requests.get(f"{self.base_url}/health")
            response.raise_for_status()
        except Exception as e:
            print(f"⚠️  Warning: Could not connect to Phoenix API at {self.base_url}")
            print(f"   Error: {e}")
    
    def query(
        self,
        query: str,
        mode: Optional[ProcessingMode] = None,
        ai_provider: AIProvider = AIProvider.AUTO,
        context: Optional[Dict] = None,
        enable_cascade: bool = True,
        enable_memory: bool = True,
        enable_search: bool = True,
        enable_crypto: bool = True,
        include_sources: bool = True,
        include_reasoning: bool = False,
        include_ledger: bool = False,
        max_tokens: Optional[int] = 4000,
        temperature: Optional[float] = 0.7
    ) -> PhoenixResponse:
        """
        Universal query method.
        
        Args:
            query: Your question or task
            mode: Processing mode (fast/balanced/deep/swarm)
            ai_provider: Which AI to use (auto/gpt-4/claude/gemini/grok/all)
            context: Additional context dictionary
            enable_cascade: Use 7-layer processing
            enable_memory: Search sovereign archive
            enable_search: Use internet search
            enable_crypto: Generate cryptographic proofs
            include_sources: Include source citations
            include_reasoning: Include reasoning trace
            include_ledger: Include cryptographic ledger
            max_tokens: Maximum response length
            temperature: Creativity (0.0-1.0)
            
        Returns:
            PhoenixResponse object with answer and metadata
        """
        # Build request
        request_data = {
            "query": query,
            "mode": (mode or self.default_mode).value,
            "ai_provider": ai_provider.value,
            "context": context,
            "enable_cascade": enable_cascade,
            "enable_memory": enable_memory,
            "enable_search": enable_search,
            "enable_crypto": enable_crypto,
            "include_sources": include_sources,
            "include_reasoning": include_reasoning,
            "include_ledger": include_ledger,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        # Make request
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        
        response = requests.post(
            f"{self.base_url}/query",
            json=request_data,
            headers=headers
        )
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        
        return PhoenixResponse(
            answer=data["answer"],
            query_id=data["query_id"],
            timestamp=data["timestamp"],
            processing_time_seconds=data["processing_time_seconds"],
            mode_used=data["mode_used"],
            providers_used=data["providers_used"],
            confidence_score=data["confidence_score"],
            sources=data.get("sources"),
            reasoning_trace=data.get("reasoning_trace"),
            cascade_layers=data.get("cascade_layers"),
            ledger=data.get("ledger"),
            suggestions=data.get("suggestions")
        )
    
    def fast(self, query: str, **kwargs) -> PhoenixResponse:
        """Fast mode - quick answer (<1s)"""
        return self.query(query, mode=ProcessingMode.FAST, **kwargs)
    
    def balanced(self, query: str, **kwargs) -> PhoenixResponse:
        """Balanced mode - 7-layer cascade (2-5s)"""
        return self.query(query, mode=ProcessingMode.BALANCED, **kwargs)
    
    def deep(self, query: str, **kwargs) -> PhoenixResponse:
        """Deep mode - multi-AI synthesis (5-15s)"""
        return self.query(query, mode=ProcessingMode.DEEP, **kwargs)
    
    def swarm(self, query: str, **kwargs) -> PhoenixResponse:
        """Swarm mode - distributed processing (10-30s)"""
        return self.query(query, mode=ProcessingMode.SWARM, **kwargs)
    
    def with_gpt4(self, query: str, **kwargs) -> PhoenixResponse:
        """Query using GPT-4"""
        return self.query(query, ai_provider=AIProvider.GPT4, **kwargs)
    
    def with_claude(self, query: str, **kwargs) -> PhoenixResponse:
        """Query using Claude"""
        return self.query(query, ai_provider=AIProvider.CLAUDE, **kwargs)
    
    def with_gemini(self, query: str, **kwargs) -> PhoenixResponse:
        """Query using Gemini"""
        return self.query(query, ai_provider=AIProvider.GEMINI, **kwargs)
    
    def with_grok(self, query: str, **kwargs) -> PhoenixResponse:
        """Query using Grok"""
        return self.query(query, ai_provider=AIProvider.GROK, **kwargs)
    
    def with_all(self, query: str, **kwargs) -> PhoenixResponse:
        """Query all AIs and synthesize"""
        return self.query(query, ai_provider=AIProvider.ALL, mode=ProcessingMode.DEEP, **kwargs)
    
    def health(self) -> Dict:
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def models(self) -> Dict:
        """List available models"""
        response = requests.get(f"{self.base_url}/models")
        response.raise_for_status()
        return response.json()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

# Global client instance for quick use
_default_client: Optional[PhoenixClient] = None

def configure(api_key: Optional[str] = None, base_url: str = "http://localhost:8000"):
    """Configure the default client"""
    global _default_client
    _default_client = PhoenixClient(api_key=api_key, base_url=base_url)

def query(query: str, **kwargs) -> PhoenixResponse:
    """Quick query using default client"""
    if _default_client is None:
        configure()
    return _default_client.query(query, **kwargs)

def fast(query: str, **kwargs) -> PhoenixResponse:
    """Quick fast query"""
    if _default_client is None:
        configure()
    return _default_client.fast(query, **kwargs)

def deep(query: str, **kwargs) -> PhoenixResponse:
    """Quick deep query"""
    if _default_client is None:
        configure()
    return _default_client.deep(query, **kwargs)


# ============================================================================
# EXAMPLES
# ============================================================================

def examples():
    """Show usage examples"""
    
    print("""
🦅🔥 PHOENIX UNIVERSAL API CLIENT - EXAMPLES
═══════════════════════════════════════════════

# 1. QUICK START
from phoenix_client import PhoenixClient

client = PhoenixClient()
response = client.query("What is AGI?")
print(response.answer)

# 2. DIFFERENT MODES
fast_response = client.fast("Quick question")  # <1s
balanced_response = client.balanced("Normal question")  # 2-5s
deep_response = client.deep("Complex question")  # 5-15s
swarm_response = client.swarm("Very complex question")  # 10-30s

# 3. SPECIFIC AI MODELS
gpt4_response = client.with_gpt4("Code this for me")
claude_response = client.with_claude("Analyze this")
gemini_response = client.with_gemini("Research this")
all_response = client.with_all("Get all perspectives")

# 4. FULL CONTROL
response = client.query(
    "Design a novel architecture",
    mode=ProcessingMode.DEEP,
    ai_provider=AIProvider.ALL,
    enable_cascade=True,
    enable_memory=True,
    enable_search=True,
    enable_crypto=True,
    include_sources=True,
    include_reasoning=True,
    include_ledger=True
)

# Access detailed results
print(response.answer)
print(f"Confidence: {response.confidence_score:.1%}")
print(f"Providers: {response.providers_used}")
print(f"Processing time: {response.processing_time_seconds}s")

if response.cascade_layers:
    print("Cascade details:", response.cascade_layers)

if response.ledger:
    print("Cryptographic proof:", response.ledger["master_hash"])

if response.suggestions:
    print("Suggestions:", response.suggestions)

# 5. CONVENIENCE FUNCTIONS
from phoenix_client import configure, query, fast, deep

configure(api_key="your-key")

answer = query("What is consciousness?")
quick_answer = fast("Quick fact check")
detailed_answer = deep("Complex analysis needed")

print(answer)
""")


if __name__ == "__main__":
    examples()
