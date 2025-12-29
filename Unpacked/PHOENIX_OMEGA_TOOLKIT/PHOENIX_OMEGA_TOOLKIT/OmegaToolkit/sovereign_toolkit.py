import time
import logging
from typing import Callable, Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format='[PHOENIX-Ω] %(asctime)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class SovereignToolkit:
    """
    Phoenix Omega: Omni-Functional Operational Matrix (OFOM).
    Manages tool registration, execution, and basic anti-fragility hooks.
    """

    def __init__(self) -> None:
        self._registry: Dict[str, Callable[..., Any]] = {}
        self._metrics: Dict[str, float] = {}
        self.state: str = "INITIALIZED"

    def register(self, name: str, func: Callable[..., Any]) -> None:
        """Register a callable as an executable directive."""
        if name in self._registry:
            logging.warning(f"Overwriting existing directive: {name}")
        self._registry[name] = func
        logging.info(f"Directive Manifested: {name}")

    def execute(self, name: str, **kwargs: Any) -> Any:
        """Execute a directive by name with keyword arguments."""
        if name not in self._registry:
            raise ValueError(f"Directive '{name}' not found in registry.")

        start = time.perf_counter()
        try:
            logging.info(f"EXEC :: {name}")
            result = self._registry[name](**kwargs)
            elapsed = time.perf_counter() - start
            self._metrics[name] = elapsed
            logging.info(f"SUCCESS :: {name} | {elapsed:.5f}s")
            return result
        except Exception as exc:
            logging.error(f"ENTROPY :: {name} | {exc}")
            self._mitigate(name, exc)
            raise

    def _mitigate(self, context: str, error: Exception) -> None:
        """Internal anti-fragility hook for execution anomalies."""
        logging.info(f"Anti-Fragility Protocol Engaged | Context={context} | Error={error}")
        # Placeholder: add retry, fallback, or alert routing here.

    @property
    def metrics(self) -> Dict[str, float]:
        """Return execution latency metrics per directive."""
        return dict(self._metrics)
