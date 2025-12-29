import os
from phoenix_registry_standard.capability_registry import CapabilityRegistry, TaskProfile, RiskProfile

def test_registry_basic():
    cfg_path = os.path.join(os.path.dirname(__file__), "..", "phoenix_registry_standard", "model_profiles.yaml")
    registry = CapabilityRegistry()
    registry.load_from_yaml(cfg_path)
    task = TaskProfile(description="Test", needs_reasoning=True)
    model = registry.choose_best(task)
    assert model is not None
