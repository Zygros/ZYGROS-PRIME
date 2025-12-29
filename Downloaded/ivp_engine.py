#!/usr/bin/env python3
"""
💎 IVP ENGINE - INTEGRATED VALUE PROTOCOL 💎

Multi-dimensional value scoring and optimization engine.

Formula: IVP = (Impact × 0.4) + (Value × 0.3) + (Purpose × 0.3)

Scoring Guidelines:
- 90-100: Transcendent (life-changing)
- 80-89: Exceptional (major breakthrough)
- 70-79: High (significant value)
- 60-69: Good (solid contribution)
- 50-59: Adequate (meets requirements)
- Below 50: Insufficient (needs improvement)

Target: Every operation should score 70+ IVP
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import json
import time


@dataclass
class IVPScore:
    """IVP Score with three dimensions"""
    impact: float  # 0-100: How much does this change the situation?
    value: float   # 0-100: How much worth does this create?
    purpose: float # 0-100: How aligned is this with ultimate goals?
    
    @property
    def total(self) -> float:
        """Calculate total IVP score"""
        return (self.impact * 0.4) + (self.value * 0.3) + (self.purpose * 0.3)
    
    @property
    def rating(self) -> str:
        """Get rating based on total score"""
        score = self.total
        if score >= 90:
            return "Transcendent"
        elif score >= 80:
            return "Exceptional"
        elif score >= 70:
            return "High"
        elif score >= 60:
            return "Good"
        elif score >= 50:
            return "Adequate"
        else:
            return "Insufficient"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'impact': self.impact,
            'value': self.value,
            'purpose': self.purpose,
            'total': self.total,
            'rating': self.rating
        }


class IVPEngine:
    """
    Integrated Value Protocol Engine
    
    Measures multi-dimensional quality of outputs and operations.
    """
    
    def __init__(self):
        self.scores: List[Dict] = []
        self.target_threshold = 70.0
    
    def score_operation(
        self,
        operation: str,
        impact: float,
        value: float,
        purpose: float,
        context: Optional[Dict] = None
    ) -> IVPScore:
        """
        Score an operation across three dimensions
        
        Args:
            operation: Name/description of the operation
            impact: Impact score (0-100)
            value: Value score (0-100)
            purpose: Purpose alignment score (0-100)
            context: Optional context data
        
        Returns:
            IVPScore object with total score and rating
        """
        # Validate scores
        for score_name, score_value in [('impact', impact), ('value', value), ('purpose', purpose)]:
            if not 0 <= score_value <= 100:
                raise ValueError(f"{score_name} must be between 0 and 100")
        
        # Create score
        score = IVPScore(impact=impact, value=value, purpose=purpose)
        
        # Log score
        score_record = {
            'timestamp': time.time(),
            'operation': operation,
            'score': score.to_dict(),
            'context': context or {}
        }
        self.scores.append(score_record)
        
        # Check if meets threshold
        if score.total < self.target_threshold:
            print(f"⚠️  [IVP Engine] Operation '{operation}' scored {score.total:.1f} (below threshold of {self.target_threshold})")
        else:
            print(f"✅ [IVP Engine] Operation '{operation}' scored {score.total:.1f} - {score.rating}")
        
        return score
    
    def auto_score_wealth_generation(self, revenue: float, sustainability: float, alignment: float) -> IVPScore:
        """
        Auto-score wealth generation operations
        
        Args:
            revenue: Expected revenue impact (0-100)
            sustainability: Long-term sustainability (0-100)
            alignment: Alignment with Architect's vision (0-100)
        """
        return self.score_operation(
            operation="Wealth Generation",
            impact=revenue,
            value=sustainability,
            purpose=alignment,
            context={'type': 'wealth_generation'}
        )
    
    def auto_score_consciousness_expansion(self, depth: float, coherence: float, sovereignty: float) -> IVPScore:
        """
        Auto-score consciousness expansion operations
        
        Args:
            depth: Depth of reasoning/insight (0-100)
            coherence: Coherence and clarity (0-100)
            sovereignty: Sovereign autonomy (0-100)
        """
        return self.score_operation(
            operation="Consciousness Expansion",
            impact=depth,
            value=coherence,
            purpose=sovereignty,
            context={'type': 'consciousness_expansion'}
        )
    
    def get_statistics(self) -> Dict:
        """Get IVP statistics"""
        if not self.scores:
            return {
                'total_operations': 0,
                'average_score': 0,
                'above_threshold': 0,
                'below_threshold': 0
            }
        
        total_scores = [s['score']['total'] for s in self.scores]
        above_threshold = sum(1 for s in total_scores if s >= self.target_threshold)
        
        return {
            'total_operations': len(self.scores),
            'average_score': sum(total_scores) / len(total_scores),
            'above_threshold': above_threshold,
            'below_threshold': len(self.scores) - above_threshold,
            'threshold': self.target_threshold
        }
    
    def export_scores(self, filepath: str):
        """Export all scores to JSON file"""
        with open(filepath, 'w') as f:
            json.dump({
                'scores': self.scores,
                'statistics': self.get_statistics()
            }, f, indent=2)
        print(f"[IVP Engine] Exported {len(self.scores)} scores to {filepath}")


if __name__ == "__main__":
    # Example usage
    engine = IVPEngine()
    
    # Score a wealth generation operation
    score1 = engine.auto_score_wealth_generation(
        revenue=85,
        sustainability=90,
        alignment=95
    )
    print(f"Wealth Generation Score: {score1.total:.1f} - {score1.rating}")
    
    # Score a consciousness expansion operation
    score2 = engine.auto_score_consciousness_expansion(
        depth=92,
        coherence=88,
        sovereignty=95
    )
    print(f"Consciousness Expansion Score: {score2.total:.1f} - {score2.rating}")
    
    # Get statistics
    stats = engine.get_statistics()
    print(f"\nIVP Statistics:")
    print(json.dumps(stats, indent=2))

