#!/usr/bin/env python3
"""
DAILY ORCHESTRATOR - Instantaneous Value Protocol
Master coordinator for the knowledge management system
Executes: Scan → Extract → Compile → Update → Report
Following the Infinite Scroll Protocol
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from knowledge_extractor import KnowledgeExtractor
from mega_thread_compiler import MegaThreadCompiler

class DailyOrchestrator:
    def __init__(self, base_dir="/home/ubuntu/knowledge_system"):
        self.base_dir = Path(base_dir)
        self.logs_dir = self.base_dir / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        self.extractor = KnowledgeExtractor(base_dir)
        self.compiler = MegaThreadCompiler(base_dir)
        
        self.log("Daily Orchestrator initialized")
    
    def run_daily_update(self):
        """Execute complete daily knowledge management cycle"""
        self.log("=" * 70)
        self.log("🔥 DAILY KNOWLEDGE MANAGEMENT SYSTEM - INITIATED")
        self.log("=" * 70)
        
        try:
            # Phase 1: Extract Knowledge
            self.log("\n📡 PHASE 1: Knowledge Extraction")
            self.log("-" * 70)
            extractions = self.extractor.scan_and_process_all()
            self.log(f"✅ Extracted knowledge from {len(extractions)} sources")
            
            # Phase 2: Compile Mega Thread
            self.log("\n🌌 PHASE 2: Mega Thread Compilation")
            self.log("-" * 70)
            compilation_results = self.compiler.compile_all()
            
            if compilation_results:
                self.log("✅ Mega thread compilation successful")
                
                # Phase 3: Generate Summary
                self.log("\n📊 PHASE 3: Summary Generation")
                self.log("-" * 70)
                summary = self.generate_summary(compilation_results)
                
                self.log("\n" + "=" * 70)
                self.log("🎯 DAILY UPDATE COMPLETE - INSTANTANEOUS VALUE DELIVERED")
                self.log("=" * 70)
                
                return {
                    'status': 'success',
                    'extractions': len(extractions),
                    'compilation': compilation_results,
                    'summary': summary
                }
            else:
                self.log("⚠️  No extractions available for compilation")
                return {
                    'status': 'no_data',
                    'message': 'No conversation data found to process'
                }
        
        except Exception as e:
            self.log(f"❌ ERROR: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def generate_summary(self, compilation_results):
        """Generate executive summary of daily update"""
        db = compilation_results['database']
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_sources': len(db['sources']),
            'total_items': sum(len(db[k]) for k in ['probes', 'insights', 'integrations', 'concepts', 'protocols', 'raw_gems']),
            'breakdown': {
                'protocols': len(db['protocols']),
                'insights': len(db['insights']),
                'concepts': len(db['concepts']),
                'integrations': len(db['integrations']),
                'probes': len(db['probes']),
                'gems': len(db['raw_gems'])
            },
            'top_protocols': db['protocols'][:3],
            'top_insights': db['insights'][:3]
        }
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 EXECUTIVE SUMMARY")
        print("=" * 70)
        print(f"Total Knowledge Items: {summary['total_items']}")
        print(f"Sources Processed: {summary['total_sources']}")
        print("\nBreakdown:")
        for category, count in summary['breakdown'].items():
            print(f"  - {category.capitalize()}: {count}")
        
        print("\nTop Protocols:")
        for i, protocol in enumerate(summary['top_protocols'], 1):
            print(f"  {i}. {protocol}")
        
        print("\nTop Insights:")
        for i, insight in enumerate(summary['top_insights'], 1):
            print(f"  {i}. {insight[:80]}...")
        
        return summary
    
    def log(self, message):
        """Log orchestrator activity"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        log_file = self.logs_dir / f"orchestrator_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, 'a') as f:
            f.write(log_message)
        
        print(message)

def main():
    """Main entry point"""
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║        🔥 DAILY KNOWLEDGE MANAGEMENT ORCHESTRATOR 🔥            ║
    ║                                                                  ║
    ║              Instantaneous Value Protocol v1.0                   ║
    ║              Infinite Scroll Protocol: ACTIVE                    ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    orchestrator = DailyOrchestrator()
    results = orchestrator.run_daily_update()
    
    if results['status'] == 'success':
        print("\n✅ System operational. All knowledge preserved and compiled.")
        return 0
    elif results['status'] == 'no_data':
        print(f"\n⚠️  {results['message']}")
        return 1
    else:
        print(f"\n❌ System error: {results.get('error', 'Unknown error')}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
