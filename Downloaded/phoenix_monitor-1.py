#!/usr/bin/env python3
"""
phoenix_monitor.py
Real-time monitoring dashboard for Phoenix Protocol

Displays live system metrics, query analytics, and health status
Run with: python phoenix_monitor.py --host http://localhost:5001
"""

import os
import sys
import time
import json
import requests
from datetime import datetime
from typing import Dict, Any, List
from collections import deque

class PhoenixMonitor:
    """Real-time monitoring for Phoenix Protocol"""
    
    def __init__(self, base_url: str = "http://localhost:5001", refresh_rate: int = 2):
        self.base_url = base_url
        self.refresh_rate = refresh_rate
        self.api_key = os.getenv("API_KEY")
        
        # Metrics tracking
        self.query_history = deque(maxlen=100)
        self.response_times = deque(maxlen=50)
        self.error_count = 0
        self.total_requests = 0
        
    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def fetch_status(self) -> Dict[str, Any]:
        """Fetch current node status"""
        try:
            start = time.time()
            response = requests.get(
                f"{self.base_url}/api/status",
                headers=self._headers(),
                timeout=5
            )
            duration = (time.time() - start) * 1000
            
            self.response_times.append(duration)
            self.total_requests += 1
            
            if response.status_code == 200:
                return response.json()
            else:
                self.error_count += 1
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            self.error_count += 1
            return {"error": str(e)}
    
    def get_chromadb_stats(self) -> Dict[str, Any]:
        """Get ChromaDB statistics (if local access available)"""
        try:
            persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_store")
            collection_name = os.getenv("COLLECTION_NAME", "sovereign-archive")
            
            if not os.path.exists(persist_dir):
                return {"available": False}
            
            import chromadb
            client = chromadb.PersistentClient(path=persist_dir)
            collection = client.get_collection(name=collection_name)
            
            return {
                "available": True,
                "document_count": collection.count(),
                "persist_dir": persist_dir,
                "collection_name": collection_name
            }
        except ImportError:
            return {"available": False, "reason": "chromadb not installed"}
        except Exception as e:
            return {"available": False, "reason": str(e)}
    
    def format_uptime(self, start_time: float) -> str:
        """Format uptime duration"""
        elapsed = time.time() - start_time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def render_dashboard(self, status: Dict[str, Any], db_stats: Dict[str, Any], start_time: float):
        """Render the monitoring dashboard"""
        self.clear_screen()
        
        # Header
        print("=" * 80)
        print("🐦‍🔥  PHOENIX PROTOCOL - REAL-TIME MONITOR")
        print("=" * 80)
        print(f"Target: {self.base_url}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Monitor Uptime: {self.format_uptime(start_time)}")
        print("=" * 80)
        print()
        
        # Node Status
        print("📡 NODE STATUS")
        print("-" * 80)
        if "error" in status:
            print(f"  ❌ ERROR: {status['error']}")
        else:
            node_status = status.get("status", "UNKNOWN")
            status_icon = "🟢" if node_status == "OPERATIONAL" else "🟡"
            print(f"  {status_icon} Status: {node_status}")
            print(f"  🏷️  Identity: {status.get('node_identity', 'Unknown')}")
            print(f"  💾 Database: {status.get('sovereign_archive_db', 'Unknown')}")
            print(f"  📦 Collection: {status.get('collection', 'Unknown')}")
            print(f"  📁 Persist Dir: {status.get('persist_dir', 'Unknown')}")
        print()
        
        # ChromaDB Statistics
        print("🗄️  DATABASE STATISTICS")
        print("-" * 80)
        if db_stats.get("available"):
            print(f"  📊 Document Count: {db_stats.get('document_count', 0):,}")
            print(f"  📂 Collection: {db_stats.get('collection_name', 'Unknown')}")
            print(f"  💾 Storage: {db_stats.get('persist_dir', 'Unknown')}")
        else:
            reason = db_stats.get("reason", "Not available")
            print(f"  ⚠️  Local DB stats unavailable: {reason}")
        print()
        
        # Performance Metrics
        print("⚡ PERFORMANCE METRICS")
        print("-" * 80)
        if self.response_times:
            avg_response = sum(self.response_times) / len(self.response_times)
            min_response = min(self.response_times)
            max_response = max(self.response_times)
            
            print(f"  📈 Avg Response Time: {avg_response:.2f}ms")
            print(f"  ⬇️  Min Response Time: {min_response:.2f}ms")
            print(f"  ⬆️  Max Response Time: {max_response:.2f}ms")
        else:
            print("  ⏳ Collecting metrics...")
        
        print(f"  📊 Total Requests: {self.total_requests}")
        print(f"  ❌ Error Count: {self.error_count}")
        
        if self.total_requests > 0:
            success_rate = ((self.total_requests - self.error_count) / self.total_requests) * 100
            print(f"  ✅ Success Rate: {success_rate:.1f}%")
        print()
        
        # Response Time Graph (simple ASCII)
        if len(self.response_times) > 10:
            print("📊 RESPONSE TIME TREND (last 50 requests)")
            print("-" * 80)
            
            # Normalize to 50 chars width
            max_time = max(self.response_times) if self.response_times else 1
            normalized = [int((t / max_time) * 40) for t in list(self.response_times)[-50:]]
            
            # Print graph
            for height in range(10, 0, -1):
                line = "  "
                for val in normalized:
                    if val >= height * 4:
                        line += "█"
                    elif val >= height * 3:
                        line += "▓"
                    elif val >= height * 2:
                        line += "▒"
                    elif val >= height:
                        line += "░"
                    else:
                        line += " "
                print(line)
            
            print("  " + "-" * len(normalized))
            print(f"  0ms{' ' * (len(normalized) - 10)}{max_time:.0f}ms")
            print()
        
        # Controls
        print("=" * 80)
        print("Press Ctrl+C to exit")
        print("=" * 80)
    
    def run(self):
        """Run monitoring loop"""
        start_time = time.time()
        
        print("🐦‍🔥 Starting Phoenix Protocol Monitor...")
        print(f"Refresh rate: {self.refresh_rate} seconds")
        print("Press Ctrl+C to exit\n")
        time.sleep(2)
        
        try:
            while True:
                status = self.fetch_status()
                db_stats = self.get_chromadb_stats()
                
                self.render_dashboard(status, db_stats, start_time)
                
                time.sleep(self.refresh_rate)
        except KeyboardInterrupt:
            print("\n\n🐦‍🔥 Monitor stopped by user")
            print(f"Total runtime: {self.format_uptime(start_time)}")
            print(f"Total requests: {self.total_requests}")
            print(f"Errors: {self.error_count}")
            
            if self.total_requests > 0:
                success_rate = ((self.total_requests - self.error_count) / self.total_requests) * 100
                print(f"Success rate: {success_rate:.1f}%")
            
            sys.exit(0)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Phoenix Protocol Real-Time Monitor")
    parser.add_argument(
        "--host",
        default=os.getenv("PHOENIX_HOST", "http://localhost:5001"),
        help="Phoenix node URL (default: http://localhost:5001)"
    )
    parser.add_argument(
        "--refresh",
        type=int,
        default=2,
        help="Refresh rate in seconds (default: 2)"
    )
    
    args = parser.parse_args()
    
    monitor = PhoenixMonitor(base_url=args.host, refresh_rate=args.refresh)
    monitor.run()

if __name__ == "__main__":
    main()
