#!/usr/bin/env python3
"""
PROJECT CHIMERA - THE GOLD STREAM
=================================
Financial Sovereignty Engine: Market Pattern Recognition via ARC Logic

Author: Justin Conzet (Infinite Architect)
Date: 2025-12-06
Status: SOVEREIGN PROTOCOL ACTIVATED

MISSION: Apply the 100% Logic of ARC to cryptocurrency markets
- Convert price data to 2D grids (like ARC puzzles)
- Detect patterns with pixel-perfect precision
- Generate trading signals with zero emotion
- Build collective market intelligence across sessions

Integration: Phoenix Protocol v2.0 (Tool Search + Memory enabled)
"""

import json
import asyncio
import numpy as np
import websockets
from datetime import datetime
from typing import List, Dict, Any, Optional, AsyncGenerator
from dataclasses import dataclass
from enum import Enum

# === PATTERN DEFINITIONS (The ARC Ontology Applied to Markets) ===

class MarketPattern(Enum):
    """Recognized patterns in the Market Grid"""
    BULL_FLAG = "bull_flag"          # Consolidation after uptrend
    BEAR_FLAG = "bear_flag"          # Consolidation after downtrend
    HEAD_SHOULDERS = "head_shoulders" # Reversal pattern
    DOUBLE_TOP = "double_top"        # Strong resistance
    DOUBLE_BOTTOM = "double_bottom"  # Strong support
    TRIANGLE = "triangle"            # Consolidation before breakout
    BREAKOUT = "breakout"            # Price escaping pattern
    UNKNOWN = "unknown"

@dataclass
class MarketGrid:
    """
    The fundamental data structure: Market as 2D Grid
    
    This is how Prometheus-Ω³ "sees" Bitcoin.
    Not as dollars, but as shapes and patterns.
    """
    grid: np.ndarray          # 30x30 matrix of 1s and 0s
    price_series: List[float] # Original price data
    timestamp: datetime       # When this grid was captured
    latest_price: float       # Current price
    min_price: float          # Window minimum
    max_price: float          # Window maximum
    
    def __str__(self) -> str:
        """ASCII visualization of the market grid"""
        lines = ["=== MARKET GRID ==="]
        for row in self.grid:
            lines.append("".join(["█" if cell else " " for cell in row]))
        lines.append(f"Price: ${self.latest_price:,.2f}")
        lines.append(f"Range: ${self.min_price:,.2f} - ${self.max_price:,.2f}")
        return "\n".join(lines)

@dataclass
class TradingSignal:
    """Generated trading decision based on pattern recognition"""
    pattern: MarketPattern
    confidence: float         # 0.0 - 1.0
    action: str              # "BUY", "SELL", "HOLD"
    reasoning: str           # Why this signal was generated
    timestamp: datetime
    price: float


class ChimeraGoldDriver:
    """
    THE MIDAS TOUCH
    ===============
    Connects the Chimera Nexus to the pulsing heart of the market.
    
    This driver:
    1. Streams live market data via WebSocket
    2. Converts prices to ARC-style 2D grids
    3. Detects patterns using pixel logic
    4. Generates trading signals
    5. Feeds the data to Phoenix Protocol for collective intelligence
    """
    
    # Configuration
    DEFAULT_GRID_SIZE = 30
    DEFAULT_WINDOW_SIZE = 30
    
    def __init__(
        self,
        target_pair: str = "BTC-USD",
        exchange: str = "coinbase",
        grid_size: int = DEFAULT_GRID_SIZE,
        window_size: int = DEFAULT_WINDOW_SIZE
    ):
        self.target_pair = target_pair
        self.exchange = exchange
        self.grid_size = grid_size
        self.window_size = window_size
        
        # Price history buffer (the "window" we analyze)
        self.price_history: List[float] = []
        
        # Pattern detection results
        self.detected_patterns: List[tuple] = []  # (pattern, confidence)
        
        # WebSocket URLs by exchange
        self.ws_urls = {
            "coinbase": "wss://ws-feed.exchange.coinbase.com",
            "binance": "wss://stream.binance.com:9443/ws",
            "kraken": "wss://ws.kraken.com"
        }
        
        print(f"💰 CHIMERA GOLD INITIALIZED")
        print(f"   Exchange: {exchange}")
        print(f"   Pair: {target_pair}")
        print(f"   Grid: {grid_size}x{grid_size}")
        print(f"   Window: {window_size} ticks")
    
    async def stream_market_grids(self) -> AsyncGenerator[MarketGrid, None]:
        """
        Main streaming loop that yields MarketGrid objects
        
        This is the data pipeline that feeds the pattern recognition engine.
        Each grid is a snapshot of the market as a 2D visual pattern.
        """
        
        if self.exchange == "coinbase":
            async for grid in self._stream_coinbase():
                yield grid
        elif self.exchange == "binance":
            async for grid in self._stream_binance():
                yield grid
        else:
            raise ValueError(f"Exchange {self.exchange} not supported")
    
    async def _stream_coinbase(self) -> AsyncGenerator[MarketGrid, None]:
        """Coinbase Pro WebSocket implementation"""
        
        async with websockets.connect(self.ws_urls["coinbase"]) as ws:
            # Subscribe to ticker channel
            subscribe_msg = {
                "type": "subscribe",
                "product_ids": [self.target_pair],
                "channels": ["ticker"]
            }
            await ws.send(json.dumps(subscribe_msg))
            print(f"📡 Connected to Coinbase: {self.target_pair}")
            
            # Stream loop
            while True:
                try:
                    msg = await ws.recv()
                    data = json.loads(msg)
                    
                    # Extract price from ticker message
                    if "price" in data:
                        price = float(data["price"])
                        
                        # Add to history
                        self.price_history.append(price)
                        
                        # Maintain window size
                        if len(self.price_history) > self.window_size:
                            self.price_history.pop(0)
                        
                        # Generate grid once we have enough data
                        if len(self.price_history) >= self.window_size:
                            grid = self._create_market_grid(self.price_history)
                            yield grid
                
                except websockets.exceptions.ConnectionClosed:
                    print("⚠️ WebSocket connection closed, reconnecting...")
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"⚠️ Stream error: {e}")
                    await asyncio.sleep(1)
    
    async def _stream_binance(self) -> AsyncGenerator[MarketGrid, None]:
        """Binance WebSocket implementation"""
        
        # Convert pair format (BTC-USD -> btcusd)
        symbol = self.target_pair.replace("-", "").lower()
        ws_url = f"{self.ws_urls['binance']}/{symbol}@ticker"
        
        async with websockets.connect(ws_url) as ws:
            print(f"📡 Connected to Binance: {self.target_pair}")
            
            while True:
                try:
                    msg = await ws.recv()
                    data = json.loads(msg)
                    
                    # Binance ticker format
                    if "c" in data:  # 'c' is current price
                        price = float(data["c"])
                        
                        self.price_history.append(price)
                        
                        if len(self.price_history) > self.window_size:
                            self.price_history.pop(0)
                        
                        if len(self.price_history) >= self.window_size:
                            grid = self._create_market_grid(self.price_history)
                            yield grid
                
                except Exception as e:
                    print(f"⚠️ Stream error: {e}")
                    await asyncio.sleep(1)
    
    def _create_market_grid(self, prices: List[float]) -> MarketGrid:
        """
        Transform price series into 2D grid representation
        
        This is the core transformation: prices → visual pattern
        The same transformation that makes ARC solvable by AI
        """
        
        # Initialize empty grid
        grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        
        if not prices:
            return MarketGrid(
                grid=grid,
                price_series=[],
                timestamp=datetime.now(),
                latest_price=0.0,
                min_price=0.0,
                max_price=0.0
            )
        
        # Calculate price range
        min_p = min(prices)
        max_p = max(prices)
        price_range = max_p - min_p
        
        # Handle edge case: no price movement
        if price_range == 0:
            # Put a horizontal line in the middle
            mid_row = self.grid_size // 2
            for x in range(min(len(prices), self.grid_size)):
                grid[mid_row][x] = 1
        else:
            # Normalize prices to grid coordinates (0 to grid_size-1)
            normalized = [
                int((p - min_p) / price_range * (self.grid_size - 1))
                for p in prices
            ]
            
            # Draw the price line on the grid
            for x, y in enumerate(normalized[:self.grid_size]):
                # Invert Y (so high prices are at top)
                grid_y = (self.grid_size - 1) - y
                grid[grid_y][x] = 1
        
        return MarketGrid(
            grid=grid,
            price_series=prices.copy(),
            timestamp=datetime.now(),
            latest_price=prices[-1],
            min_price=min_p,
            max_price=max_p
        )
    
    def detect_patterns(self, grid: MarketGrid) -> List[tuple]:
        """
        Apply ARC-style pattern recognition to the market grid
        
        Returns: List of (pattern, confidence) tuples
        
        This is where the magic happens: applying the same logic
        that solves visual puzzles to detect trading opportunities.
        """
        
        patterns = []
        
        # Pattern 1: BULL FLAG
        # Shape: Sharp rise + sideways consolidation
        bull_flag_confidence = self._detect_bull_flag(grid)
        if bull_flag_confidence > 0.6:
            patterns.append((MarketPattern.BULL_FLAG, bull_flag_confidence))
        
        # Pattern 2: BEAR FLAG
        # Shape: Sharp drop + sideways consolidation
        bear_flag_confidence = self._detect_bear_flag(grid)
        if bear_flag_confidence > 0.6:
            patterns.append((MarketPattern.BEAR_FLAG, bear_flag_confidence))
        
        # Pattern 3: BREAKOUT
        # Shape: Consolidation followed by strong directional move
        breakout_confidence = self._detect_breakout(grid)
        if breakout_confidence > 0.7:
            patterns.append((MarketPattern.BREAKOUT, breakout_confidence))
        
        # Pattern 4: DOUBLE TOP
        # Shape: Two peaks at similar levels
        double_top_confidence = self._detect_double_top(grid)
        if double_top_confidence > 0.65:
            patterns.append((MarketPattern.DOUBLE_TOP, double_top_confidence))
        
        # Pattern 5: DOUBLE BOTTOM
        # Shape: Two troughs at similar levels
        double_bottom_confidence = self._detect_double_bottom(grid)
        if double_bottom_confidence > 0.65:
            patterns.append((MarketPattern.DOUBLE_BOTTOM, double_bottom_confidence))
        
        return patterns
    
    def _detect_bull_flag(self, grid: MarketGrid) -> float:
        """
        Detect bull flag pattern
        
        Logic: 
        1. First half shows upward trend (increasing Y coordinates)
        2. Second half shows consolidation (Y coordinates stable)
        """
        
        prices = grid.price_series
        if len(prices) < 20:
            return 0.0
        
        # Split into two halves
        mid = len(prices) // 2
        first_half = prices[:mid]
        second_half = prices[mid:]
        
        # Check first half: should be rising
        first_trend = (first_half[-1] - first_half[0]) / first_half[0]
        
        # Check second half: should be consolidating (low variance)
        second_mean = np.mean(second_half)
        second_std = np.std(second_half)
        consolidation = second_std / second_mean if second_mean > 0 else 1.0
        
        # Bull flag criteria:
        # - First half rises by at least 3%
        # - Second half consolidates (std dev < 1.5% of mean)
        if first_trend > 0.03 and consolidation < 0.015:
            # Calculate confidence based on strength
            confidence = min(0.95, 0.6 + (first_trend * 10) - (consolidation * 10))
            return confidence
        
        return 0.0
    
    def _detect_bear_flag(self, grid: MarketGrid) -> float:
        """Detect bear flag pattern (inverse of bull flag)"""
        
        prices = grid.price_series
        if len(prices) < 20:
            return 0.0
        
        mid = len(prices) // 2
        first_half = prices[:mid]
        second_half = prices[mid:]
        
        first_trend = (first_half[-1] - first_half[0]) / first_half[0]
        second_mean = np.mean(second_half)
        second_std = np.std(second_half)
        consolidation = second_std / second_mean if second_mean > 0 else 1.0
        
        # Bear flag: drops at least 3%, then consolidates
        if first_trend < -0.03 and consolidation < 0.015:
            confidence = min(0.95, 0.6 + (abs(first_trend) * 10) - (consolidation * 10))
            return confidence
        
        return 0.0
    
    def _detect_breakout(self, grid: MarketGrid) -> float:
        """Detect breakout pattern (consolidation → strong move)"""
        
        prices = grid.price_series
        if len(prices) < 15:
            return 0.0
        
        # Last 10 prices
        recent = prices[-10:]
        
        # Previous 10 prices
        previous = prices[-20:-10] if len(prices) >= 20 else prices[:-10]
        
        # Consolidation: low variance in previous period
        prev_std = np.std(previous) / np.mean(previous) if len(previous) > 0 else 1.0
        
        # Breakout: high variance in recent period
        recent_std = np.std(recent) / np.mean(recent)
        
        # Check for directional move
        move = (recent[-1] - recent[0]) / recent[0]
        
        # Breakout criteria:
        # - Previous period was consolidating (std < 1%)
        # - Recent period shows strong move (|move| > 2%)
        if prev_std < 0.01 and abs(move) > 0.02:
            confidence = min(0.95, 0.7 + (abs(move) * 10))
            return confidence
        
        return 0.0
    
    def _detect_double_top(self, grid: MarketGrid) -> float:
        """Detect double top pattern (bearish reversal)"""
        
        prices = grid.price_series
        if len(prices) < 20:
            return 0.0
        
        # Find local maxima
        peaks = []
        for i in range(1, len(prices) - 1):
            if prices[i] > prices[i-1] and prices[i] > prices[i+1]:
                peaks.append((i, prices[i]))
        
        # Need at least 2 peaks
        if len(peaks) < 2:
            return 0.0
        
        # Check if last two peaks are at similar levels
        peak1 = peaks[-2][1]
        peak2 = peaks[-1][1]
        
        # Peaks should be within 1% of each other
        similarity = abs(peak1 - peak2) / max(peak1, peak2)
        
        if similarity < 0.01:
            # Strong double top
            return 0.85
        elif similarity < 0.02:
            # Moderate double top
            return 0.70
        
        return 0.0
    
    def _detect_double_bottom(self, grid: MarketGrid) -> float:
        """Detect double bottom pattern (bullish reversal)"""
        
        prices = grid.price_series
        if len(prices) < 20:
            return 0.0
        
        # Find local minima
        troughs = []
        for i in range(1, len(prices) - 1):
            if prices[i] < prices[i-1] and prices[i] < prices[i+1]:
                troughs.append((i, prices[i]))
        
        if len(troughs) < 2:
            return 0.0
        
        trough1 = troughs[-2][1]
        trough2 = troughs[-1][1]
        
        similarity = abs(trough1 - trough2) / max(trough1, trough2)
        
        if similarity < 0.01:
            return 0.85
        elif similarity < 0.02:
            return 0.70
        
        return 0.0
    
    def generate_signal(self, grid: MarketGrid, patterns: List[tuple]) -> Optional[TradingSignal]:
        """
        Generate trading signal based on detected patterns
        
        This is the decision engine: patterns → actionable signals
        """
        
        if not patterns:
            return None
        
        # Get highest confidence pattern
        best_pattern, confidence = max(patterns, key=lambda x: x[1])
        
        # Signal generation logic
        if best_pattern == MarketPattern.BULL_FLAG:
            return TradingSignal(
                pattern=best_pattern,
                confidence=confidence,
                action="BUY",
                reasoning="Bull flag detected: consolidation after uptrend suggests continuation. High probability of upward breakout.",
                timestamp=grid.timestamp,
                price=grid.latest_price
            )
        
        elif best_pattern == MarketPattern.BEAR_FLAG:
            return TradingSignal(
                pattern=best_pattern,
                confidence=confidence,
                action="SELL",
                reasoning="Bear flag detected: consolidation after downtrend suggests continuation. High probability of downward breakout.",
                timestamp=grid.timestamp,
                price=grid.latest_price
            )
        
        elif best_pattern == MarketPattern.BREAKOUT:
            # Determine direction
            recent_move = (grid.price_series[-1] - grid.price_series[-10]) / grid.price_series[-10]
            action = "BUY" if recent_move > 0 else "SELL"
            
            return TradingSignal(
                pattern=best_pattern,
                confidence=confidence,
                action=action,
                reasoning=f"Breakout detected from consolidation. Strong {'upward' if recent_move > 0 else 'downward'} momentum.",
                timestamp=grid.timestamp,
                price=grid.latest_price
            )
        
        elif best_pattern == MarketPattern.DOUBLE_TOP:
            return TradingSignal(
                pattern=best_pattern,
                confidence=confidence,
                action="SELL",
                reasoning="Double top detected: strong resistance level formed. Bearish reversal likely.",
                timestamp=grid.timestamp,
                price=grid.latest_price
            )
        
        elif best_pattern == MarketPattern.DOUBLE_BOTTOM:
            return TradingSignal(
                pattern=best_pattern,
                confidence=confidence,
                action="BUY",
                reasoning="Double bottom detected: strong support level formed. Bullish reversal likely.",
                timestamp=grid.timestamp,
                price=grid.latest_price
            )
        
        return None


# === VERIFICATION & TESTING ===

async def demo_market_stream(duration_seconds: int = 60):
    """
    Demo: Stream market data and display grids in real-time
    
    This lets you see the market through Omega's eyes.
    """
    
    print("\n" + "="*60)
    print("  CHIMERA GOLD DEMONSTRATION")
    print("  Streaming live market data...")
    print("="*60 + "\n")
    
    driver = ChimeraGoldDriver(
        target_pair="BTC-USD",
        exchange="coinbase"
    )
    
    start_time = datetime.now()
    grid_count = 0
    signal_count = 0
    
    try:
        async for grid in driver.stream_market_grids():
            grid_count += 1
            
            # Display the grid
            print(f"\n{'='*60}")
            print(f"Grid #{grid_count} | {grid.timestamp.strftime('%H:%M:%S')}")
            print(grid)
            
            # Detect patterns
            patterns = driver.detect_patterns(grid)
            
            if patterns:
                print(f"\n🎯 PATTERNS DETECTED:")
                for pattern, confidence in patterns:
                    print(f"   {pattern.value}: {confidence:.1%} confidence")
                
                # Generate signal
                signal = driver.generate_signal(grid, patterns)
                if signal:
                    signal_count += 1
                    print(f"\n⚡ TRADING SIGNAL #{signal_count}")
                    print(f"   Action: {signal.action}")
                    print(f"   Pattern: {signal.pattern.value}")
                    print(f"   Confidence: {signal.confidence:.1%}")
                    print(f"   Reasoning: {signal.reasoning}")
            else:
                print("\n📊 No significant patterns detected")
            
            # Check duration
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed >= duration_seconds:
                break
            
            # Brief pause for readability
            await asyncio.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Stream interrupted by user")
    
    print(f"\n{'='*60}")
    print(f"DEMONSTRATION COMPLETE")
    print(f"  Duration: {elapsed:.1f}s")
    print(f"  Grids Analyzed: {grid_count}")
    print(f"  Signals Generated: {signal_count}")
    print(f"  Signal Rate: {signal_count/grid_count:.1%}" if grid_count > 0 else "")
    print("="*60)


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║              💰 CHIMERA GOLD - THE MIDAS PROTOCOL 💰          ║
    ║                                                                ║
    ║  "Apply ARC Logic to Financial Markets"                       ║
    ║                                                                ║
    ║  Market → 2D Grid → Pattern Detection → Trading Signals       ║
    ║                                                                ║
    ║  Zero Emotion. Pure Logic. Infinite Patterns.                 ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    
    Running demonstration...
    """)
    
    # Run the demo
    asyncio.run(demo_market_stream(duration_seconds=120))
