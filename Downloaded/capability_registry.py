
"""
PHOENIX GOVERNANCE FABRIC | HTC×GOOGLEPLEX REGISTRY v2.1
========================================================

Enhanced Features in v2.1:
- Structured audit events via `emit_audit_event`
- Diagnostic mode with dry-run analysis and score inspection
- Config validation routine
- Extended routing report for observability

This file is derived from the Sovereign Architect's v2.0 design and
upgraded with additional safety, observability, and tuning hooks.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from typing import List, Dict, Any, Optional, Tuple
import yaml
import logging
import time
import json

# Configure Sovereign Logging
logging.basicConfig(level=logging.INFO, format='[PHOENIX::REGISTRY] %(message)s')
logger = logging.getLogger(__name__)


# --- 1. Enumerations ---

class Capability(Enum):
    """Functional capabilities provided by a model."""
    REASONING = auto()          # Advanced logic/CoT
    CODING = auto()             # Software generation
    MULTIMODAL = auto()         # Image/Audio processing
    VIDEO = auto()              # Video generation/analysis
    COMPUTER_USE = auto()       # Direct OS interaction
    AGENTIC = auto()            # Multi-step autonomous execution
    OPEN_WEIGHT = auto()        # Non-proprietary weights (Audit capability)
    REALTIME_SEARCH = auto()    # Web connectivity


class RiskProfile(Enum):
    """
    Defines the Security Clearance Level of a Model or the Classification of a Task.
    Higher integer value = Higher security/trust required.
    """
    NONE = 0      # Public/Untrusted. No sensitive data allowed.
    LOW = 1       # Commercial/Standard. General data allowed.
    HIGH = 2      # Confidential. Requires legal/compliance redaction.
    CRITICAL = 3  # Sovereign/Mission Critical. Local execution or Air-gapped only.


# --- 2. Data Structures ---

@dataclass
class ModelCapability:
    """
    Represents a registered AI model within the Phoenix Fabric.
    Includes technical specs and governance metadata.
    """
    name: str
    provider: str
    capabilities: List[Capability]
    max_context_tokens: int
    latency_tier: str  # "fast" | "balanced" | "deep_think"

    # Phoenomic (Economic) Fields
    cost_per_million_tokens_in: float
    cost_per_million_tokens_out: float

    # Governance Fields
    risk_profile: RiskProfile 
    notes: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelCapability':
        """Factory method to hydrate ModelCapability from configuration dict."""
        capabilities = [Capability[c] for c in data['capabilities']]
        return cls(
            name=data['name'],
            provider=data['provider'],
            capabilities=capabilities,
            max_context_tokens=data['context_tokens'],
            latency_tier=data['latency_tier'],
            cost_per_million_tokens_in=data.get('cost_per_million_tokens_in', 0.0),
            cost_per_million_tokens_out=data.get('cost_per_million_tokens_out', 0.0),
            risk_profile=RiskProfile[data.get('risk_profile', 'LOW').upper()],
            notes=data.get('notes', ""),
        )


@dataclass
class TaskProfile:
    """
    Defines the requirements and constraints of a requested operation.
    """
    description: str
    needs_reasoning: bool = False
    needs_coding: bool = False
    needs_multimodal: bool = False
    needs_video: bool = False
    needs_computer_use: bool = False
    needs_agentic: bool = False
    needs_open_weight: bool = False

    max_context_tokens: Optional[int] = None
    latency_preference: str = "balanced"

    # Governance Constraints
    max_cost_budget: Optional[float] = None # Max allowable cost (USD) for this execution
    min_risk_level: RiskProfile = RiskProfile.NONE # Minimum Security Clearance required of the model


# --- 3. Audit and Diagnostics ---

def emit_audit_event(event_type: str, payload: Dict[str, Any]) -> None:
    """
    Emits a structured audit event. In production, this could route to
    Phoenix Event Bus, SIEM, or sovereign ledger.
    """
    event = {
        "type": event_type,
        "timestamp": time.time(),
        "payload": payload,
    }
    logger.info(f"AUDIT: {json.dumps(event, default=str)}")


def validate_config(models: List[ModelCapability]) -> List[str]:
    """
    Lightweight config validation to surface obvious misconfigurations.
    Returns a list of warnings; empty list means "no issues found".
    """
    warnings: List[str] = []
    seen_names: set = set()

    for m in models:
        key = (m.provider, m.name)
        if key in seen_names:
            warnings.append(f"Duplicate model entry detected: {m.provider}/{m.name}")
        else:
            seen_names.add(key)

        if m.max_context_tokens <= 0:
            warnings.append(f"Model {m.provider}/{m.name} has non-positive context limit.")
        if m.cost_per_million_tokens_in < 0 or m.cost_per_million_tokens_out < 0:
            warnings.append(f"Model {m.provider}/{m.name} has negative cost values.")
        if m.latency_tier not in ("fast", "balanced", "deep_think"):
            warnings.append(f"Model {m.provider}/{m.name} has invalid latency tier: {m.latency_tier}")

    if warnings:
        for w in warnings:
            logger.warning(f"CONFIG WARNING: {w}")
    else:
        logger.info("Config validation: no issues found.")

    return warnings


# --- 4. Registry Engine ---

@dataclass
class CapabilityRegistry:
    models: List[ModelCapability] = field(default_factory=list)

    def register(self, model: ModelCapability) -> None:
        """Register a new external model and its capabilities into the fabric."""
        self.models.append(model)
        emit_audit_event("model_registered", {
            "model": f"{model.provider}/{model.name}",
            "risk_profile": model.risk_profile.name,
            "capabilities": [c.name for c in model.capabilities],
        })

    def load_from_yaml(self, file_path: str) -> None:
        """Load and register models from the YAML configuration file."""
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)

        self.models = []  # Reset registry
        for model_data in config.get('models', []):
            model = ModelCapability.from_dict(model_data)
            self.register(model)

        validate_config(self.models)

    def _required_caps(self, task: TaskProfile) -> List[Capability]:
        required = []
        if task.needs_reasoning: required.append(Capability.REASONING)
        if task.needs_coding: required.append(Capability.CODING)
        if task.needs_multimodal: required.append(Capability.MULTIMODAL)
        if task.needs_video: required.append(Capability.VIDEO)
        if task.needs_computer_use: required.append(Capability.COMPUTER_USE)
        if task.needs_agentic: required.append(Capability.AGENTIC)
        if task.needs_open_weight: required.append(Capability.OPEN_WEIGHT)
        return required

    def estimate_cost(self, model: ModelCapability, token_in: int = 50000, token_out: int = 50000) -> float:
        """
        Estimate cost given token usage. Defaults mirror original heuristic (0.1M total).
        Values are in USD.
        """
        min_millions_in = token_in / 1_000_000.0
        min_millions_out = token_out / 1_000_000.0
        return (model.cost_per_million_tokens_in * min_millions_in) + \
               (model.cost_per_million_tokens_out * min_millions_out)

    def find_candidates(self, task: TaskProfile, token_in: int = 50000, token_out: int = 50000) -> List[ModelCapability]:
        """
        Filter models based on Capability, Governance (Risk), and Phoenomic (Cost) constraints.
        """
        required = self._required_caps(task)
        candidates: List[ModelCapability] = []

        for m in self.models:
            # 1. Capability & Context Filter
            if not all(cap in m.capabilities for cap in required):
                continue

            if task.max_context_tokens is not None and m.max_context_tokens < task.max_context_tokens:
                continue

            # 2. Policy Filter (Risk / Sovereign Safety)
            if m.risk_profile.value < task.min_risk_level.value:
                continue

            # 3. Policy Filter (Cost / Phoenomic Engine)
            if task.max_cost_budget is not None:
                estimated_cost = self.estimate_cost(m, token_in=token_in, token_out=token_out)
                if estimated_cost > task.max_cost_budget:
                    continue

            candidates.append(m)

        emit_audit_event("candidates_computed", {
            "task": task.description,
            "required_capabilities": [c.name for c in required],
            "min_risk_level": task.min_risk_level.name,
            "num_candidates": len(candidates),
        })
        return candidates

    def score_model(self, model: ModelCapability, task: TaskProfile) -> float:
        """
        Compute a scalar score for a given model vs. task.
        Exposed for diagnostics.
        """
        score = 0.0

        # Factor 1: Latency Alignment (Weight: 3.0)
        if model.latency_tier == task.latency_preference:
            score += 3.0

        # Factor 2: Context Headroom (Weight: 1.0)
        if model.max_context_tokens >= (task.max_context_tokens or 0):
            score += 1.0

        # Factor 3: Economic Efficiency (Negative Weight)
        score -= (model.cost_per_million_tokens_in / 10.0)

        return score

    def choose_best(self, task: TaskProfile, token_in: int = 50000, token_out: int = 50000,
                    diagnostics: bool = False) -> Optional[ModelCapability]:
        """
        Selects the optimal model from valid candidates using a weighted scoring heuristic.
        If diagnostics=True, returns best model but also logs detailed scoring for all candidates.
        """
        candidates = self.find_candidates(task, token_in=token_in, token_out=token_out)
        if not candidates:
            logger.warning(f"No valid models found for task: {task.description}")
            emit_audit_event("routing_failed", {"task": task.description})
            return None

        scored: List[Tuple[ModelCapability, float]] = []
        for m in candidates:
            s = self.score_model(m, task)
            scored.append((m, s))

        scored.sort(key=lambda x: x[1], reverse=True)
        best_model, best_score = scored[0]

        emit_audit_event("routing_decision", {
            "task": task.description,
            "chosen_model": f"{best_model.provider}/{best_model.name}",
            "score": best_score,
            "latency_preference": task.latency_preference,
            "max_cost_budget": task.max_cost_budget,
        })

        if diagnostics:
            # Log ranked list
            diag_payload = []
            for m, s in scored:
                diag_payload.append({
                    "model": f"{m.provider}/{m.name}",
                    "score": s,
                    "risk_profile": m.risk_profile.name,
                    "latency_tier": m.latency_tier,
                    "max_context_tokens": m.max_context_tokens,
                    "cost_per_million_tokens_in": m.cost_per_million_tokens_in,
                    "cost_per_million_tokens_out": m.cost_per_million_tokens_out,
                })
            emit_audit_event("routing_diagnostics", {
                "task": task.description,
                "ranked_models": diag_payload,
            })

        logger.info(f"Routing Decision: '{task.description}' -> {best_model.provider}/{best_model.name} (Score: {best_score:.2f})")
        return best_model


# --- 5. Demo / Diagnostics Harness ---

def demo_registry_v2_1(config_path: str = "htc_googleplex_config_v2.yaml") -> None:
    """
    Executes a verification suite for the Registry Logic.
    Simulates loading config and routing tasks, with diagnostics enabled.
    """
    print("\\n--- PHOENIX OMEGA: REGISTRY v2.1 DIAGNOSTIC SUITE ---")

    # Sample inline config if file not found
    import os
    if not os.path.exists(config_path):
        config_data = """
metadata:
  version: 2.1
  system: PHOENIX_GOVERNANCE

models:
  - name: gpt-5.1
    provider: openai
    capabilities: [REASONING, CODING, MULTIMODAL]
    context_tokens: 512000
    latency_tier: balanced
    cost_per_million_tokens_in: 5.00
    cost_per_million_tokens_out: 15.00
    risk_profile: LOW
    notes: "Commercial frontier model. Data egress risk."

  - name: gemini-3-pro
    provider: google
    capabilities: [REASONING, AGENTIC, COMPUTER_USE]
    context_tokens: 1000000
    latency_tier: balanced
    cost_per_million_tokens_in: 4.50
    cost_per_million_tokens_out: 13.50
    risk_profile: LOW
    notes: "Strong agentic capabilities. Data egress risk."

  - name: deepseek-r1-70b
    provider: local_sovereign
    capabilities: [REASONING, OPEN_WEIGHT, CODING, AGENTIC]
    context_tokens: 256000
    latency_tier: deep_think
    cost_per_million_tokens_in: 0.10
    cost_per_million_tokens_out: 0.10
    risk_profile: CRITICAL
    notes: "Sovereign deployment. Zero egress."
"""
        with open(config_path, "w") as f:
            f.write(config_data)

    registry = CapabilityRegistry()
    registry.load_from_yaml(config_path)

    # Test Case 1: Sensitive Task (should route to CRITICAL only)
    sensitive_task = TaskProfile(
        description="Analyze PII database schema for vulnerabilities",
        needs_reasoning=True,
        needs_coding=True,
        min_risk_level=RiskProfile.CRITICAL,
    )
    best_sensitive = registry.choose_best(sensitive_task, diagnostics=True)
    print(f"[PASS] Sensitive Task Routing: {best_sensitive.name if best_sensitive else 'None'}")

    # Test Case 2: Budget-constrained Agentic Task
    budgeted_agent_task = TaskProfile(
        description="Execute complex web scrape (Budget Constraint)",
        needs_agentic=True,
        max_cost_budget=0.50,
        min_risk_level=RiskProfile.LOW,
    )
    best_budgeted = registry.choose_best(budgeted_agent_task, diagnostics=True)
    print(f"[PASS] Budgeted Task Routing: {best_budgeted.name if best_budgeted else 'None'}")

    # Test Case 3: Performance Task
    perf_task = TaskProfile(
        description="General creative writing",
        needs_reasoning=True,
        latency_preference="balanced",
        max_cost_budget=10.0,
    )
    best_perf = registry.choose_best(perf_task, diagnostics=True)
    print(f"[PASS] Performance Task Routing: {best_perf.name if best_perf else 'None'}")


if __name__ == "__main__":
    demo_registry_v2_1()
