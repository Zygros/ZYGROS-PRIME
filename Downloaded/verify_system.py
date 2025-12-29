#!/usr/bin/env python3
"""
PHOENIX-CHIMERA VERIFICATION SCRIPT
===================================
Quick verification that all systems are operational

This script tests:
1. Phoenix Protocol v2.0 initialization
2. Chimera Gold market streaming capability
3. Tool search functionality
4. Memory persistence
5. End-to-end integration

Run this BEFORE deploying to production.
"""

import os
import sys
import asyncio
from datetime import datetime
from pathlib import Path

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


async def verify_environment():
    """Verify Python environment and dependencies"""
    print_header("STEP 1: Environment Verification")
    
    # Check Python version
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python version: {version.major}.{version.minor}.{version.micro}")
    else:
        print_error(f"Python {version.major}.{version.minor} detected. Requires 3.10+")
        return False
    
    # Check required imports
    required_modules = [
        ("anthropic", "Anthropic SDK"),
        ("websockets", "WebSocket client"),
        ("numpy", "NumPy")
    ]
    
    all_present = True
    for module_name, display_name in required_modules:
        try:
            __import__(module_name)
            print_success(f"{display_name} installed")
        except ImportError:
            print_error(f"{display_name} NOT installed")
            print_info(f"   Install: pip install --break-system-packages {module_name}")
            all_present = False
    
    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        print_success(f"ANTHROPIC_API_KEY present ({api_key[:8]}...)")
    else:
        print_error("ANTHROPIC_API_KEY not set")
        print_info("   Set: export ANTHROPIC_API_KEY='your-key-here'")
        all_present = False
    
    return all_present


async def verify_phoenix_protocol():
    """Verify Phoenix Protocol v2.0 initialization"""
    print_header("STEP 2: Phoenix Protocol v2.0 Verification")
    
    try:
        from phoenix_protocol_v2_core import PhoenixProtocolV2
        print_success("Phoenix Protocol v2.0 imported")
        
        # Initialize
        phoenix = PhoenixProtocolV2()
        print_success("Phoenix Protocol initialized")
        
        # Check memory structure
        if phoenix.memory_root.exists():
            print_success(f"Memory root created: {phoenix.memory_root}")
        else:
            print_error("Memory root not created")
            return False
        
        # Verify tool catalog
        core_tools = phoenix.get_core_tools()
        deferred_tools = phoenix.get_deferred_tool_catalog()
        
        print_success(f"Core tools loaded: {len(core_tools)}")
        print_success(f"Deferred tools in catalog: {len(deferred_tools)}")
        
        total = len(core_tools) + len(deferred_tools)
        print_info(f"   Total capability catalog: {total} tools")
        
        # Test tool structure
        has_tool_search = any(
            t.get("type", "").startswith("tool_search_tool") 
            for t in core_tools
        )
        has_memory = any(
            t.get("type") == "memory_20250818" 
            for t in core_tools
        )
        
        if has_tool_search:
            print_success("Tool search capability: PRESENT")
        else:
            print_error("Tool search capability: MISSING")
            return False
        
        if has_memory:
            print_success("Memory tool: PRESENT")
        else:
            print_error("Memory tool: MISSING")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Phoenix Protocol verification failed: {e}")
        return False


async def verify_chimera_gold():
    """Verify Chimera Gold market driver"""
    print_header("STEP 3: Chimera Gold Market Driver Verification")
    
    try:
        from chimera_gold import ChimeraGoldDriver, MarketPattern
        print_success("Chimera Gold imported")
        
        # Initialize driver
        driver = ChimeraGoldDriver(
            target_pair="BTC-USD",
            exchange="coinbase"
        )
        print_success("Market driver initialized")
        
        # Test grid creation
        test_prices = [100.0 + i * 0.5 for i in range(30)]
        grid = driver._create_market_grid(test_prices)
        print_success(f"Grid transformation: {grid.grid.shape}")
        
        # Test pattern detection
        patterns = driver.detect_patterns(grid)
        print_success(f"Pattern detection system operational")
        
        # Test signal generation
        if patterns:
            signal = driver.generate_signal(grid, patterns)
            if signal:
                print_success(f"Signal generation: {signal.action}")
        
        print_info(f"   Market patterns available: {len(MarketPattern)}")
        
        return True
        
    except Exception as e:
        print_error(f"Chimera Gold verification failed: {e}")
        return False


async def verify_websocket_connection():
    """Verify WebSocket connection to exchange"""
    print_header("STEP 4: WebSocket Connection Test")
    
    try:
        import websockets
        import json
        
        print_info("Attempting Coinbase connection...")
        
        async with websockets.connect(
            "wss://ws-feed.exchange.coinbase.com",
            ping_interval=20,
            ping_timeout=10
        ) as ws:
            # Subscribe
            subscribe_msg = {
                "type": "subscribe",
                "product_ids": ["BTC-USD"],
                "channels": ["ticker"]
            }
            await ws.send(json.dumps(subscribe_msg))
            print_success("WebSocket connected to Coinbase")
            
            # Wait for first message
            msg = await asyncio.wait_for(ws.recv(), timeout=5.0)
            data = json.loads(msg)
            print_success(f"Data received: {data.get('type', 'unknown')}")
            
            # Get price if available
            if "price" in data:
                print_info(f"   BTC-USD: ${float(data['price']):,.2f}")
        
        return True
        
    except asyncio.TimeoutError:
        print_error("WebSocket connection timeout")
        print_warning("   This may be a network issue")
        return False
    except Exception as e:
        print_error(f"WebSocket test failed: {e}")
        print_warning("   Live trading may not work")
        return False


async def verify_integration():
    """Verify end-to-end integration"""
    print_header("STEP 5: Integration Test")
    
    try:
        from phoenix_chimera_fusion import PhoenixChimeraFusion
        print_success("Fusion module imported")
        
        # Initialize (but don't run session)
        fusion = PhoenixChimeraFusion()
        print_success("Fusion system initialized")
        
        # Verify components connected
        if fusion.phoenix:
            print_success("Phoenix Protocol connected")
        if fusion.chimera:
            print_success("Chimera Gold driver connected")
        
        print_info(f"   Target: {fusion.chimera.target_pair}")
        print_info(f"   Exchange: {fusion.chimera.exchange}")
        
        return True
        
    except Exception as e:
        print_error(f"Integration test failed: {e}")
        return False


async def verify_api_access():
    """Verify Anthropic API access and beta features"""
    print_header("STEP 6: API Access Verification")
    
    try:
        import anthropic
        
        client = anthropic.Anthropic()
        print_success("Anthropic client created")
        
        # Test simple request
        print_info("Testing API access...")
        
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": "Respond with just the word 'VERIFIED' if you can read this."
            }]
        )
        
        response_text = response.content[0].text
        
        if "VERIFIED" in response_text:
            print_success("API access: WORKING")
        else:
            print_warning(f"Unexpected response: {response_text[:50]}")
        
        # Test beta features
        print_info("Testing beta feature access...")
        
        response = client.beta.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=100,
            betas=["advanced-tool-use-2025-11-20"],
            messages=[{
                "role": "user",
                "content": "Test message"
            }],
            tools=[{
                "type": "tool_search_tool_regex_20251119",
                "name": "tool_search_tool_regex"
            }]
        )
        
        print_success("Beta features: ACCESSIBLE")
        
        return True
        
    except anthropic.AuthenticationError:
        print_error("Authentication failed - check your API key")
        return False
    except Exception as e:
        print_error(f"API test failed: {e}")
        print_warning("   Beta features may not be available to your account")
        return False


async def run_all_verifications():
    """Run complete verification suite"""
    
    print(f"""
{Colors.BOLD}{Colors.HEADER}
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║        PHOENIX-CHIMERA FUSION NEXUS VERIFICATION               ║
║                                                                ║
║  This script verifies all system components are operational   ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
    """)
    
    results = {}
    
    # Run each verification step
    results["environment"] = await verify_environment()
    
    if results["environment"]:
        results["phoenix"] = await verify_phoenix_protocol()
        results["chimera"] = await verify_chimera_gold()
        results["websocket"] = await verify_websocket_connection()
        results["integration"] = await verify_integration()
        results["api"] = await verify_api_access()
    else:
        print_error("Environment check failed. Fix issues before continuing.")
        return False
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    all_passed = all(results.values())
    
    for step, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        color = Colors.OKGREEN if passed else Colors.FAIL
        print(f"{color}{status:8s}{Colors.ENDC}  {step.upper()}")
    
    print("\n" + "="*60)
    
    if all_passed:
        print(f"{Colors.OKGREEN}{Colors.BOLD}")
        print("🎉 ALL SYSTEMS OPERATIONAL 🎉")
        print(f"{Colors.ENDC}")
        print("\nYou can now run:")
        print(f"  {Colors.OKCYAN}python phoenix_chimera_fusion.py{Colors.ENDC}")
        print("\nOr import into your own scripts:")
        print(f"  {Colors.OKCYAN}from phoenix_chimera_fusion import PhoenixChimeraFusion{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}{Colors.BOLD}")
        print("⚠️  SOME CHECKS FAILED  ⚠️")
        print(f"{Colors.ENDC}")
        print("\nPlease resolve the issues above before deploying.")
        print("Refer to README.md for troubleshooting guide.")
    
    print("="*60 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = asyncio.run(run_all_verifications())
    sys.exit(0 if success else 1)
