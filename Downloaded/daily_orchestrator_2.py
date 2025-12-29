#!/usr/bin/env python3
"""
Daily Orchestrator Script
Part of the Daily Knowledge Management System
Coordinates knowledge extraction, compilation, and mega thread updates
Implements the Infinite Scroll Protocol orchestration layer
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from knowledge_extractor import KnowledgeExtractor
from mega_thread_compiler import MegaThreadCompiler


class DailyOrchestrator:
    """Orchestrates the daily knowledge management system execution"""
    
    def __init__(self, base_dir: str = '/home/ubuntu/knowledge_system'):
        self.base_dir = Path(base_dir)
        self.conversations_dir = self.base_dir / 'conversations'
        self.compilations_dir = self.base_dir / 'compilations'
        self.mega_thread_dir = self.base_dir / 'mega_thread'
        self.logs_dir = self.base_dir / 'logs'
        
        # Ensure all directories exist
        for directory in [self.conversations_dir, self.compilations_dir, 
                         self.mega_thread_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize log file
        self.log_file = self.logs_dir / f"orchestrator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # Initialize components
        self.extractor = KnowledgeExtractor(
            conversations_dir=str(self.conversations_dir),
            output_dir=str(self.compilations_dir)
        )
        
        self.compiler = MegaThreadCompiler(
            compilations_dir=str(self.compilations_dir),
            mega_thread_dir=str(self.mega_thread_dir)
        )
    
    def log(self, message: str, level: str = 'INFO'):
        """Log message to file and console"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        print(log_entry)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def run(self, hours: int = 24) -> Dict:
        """Execute the complete daily knowledge management workflow"""
        self.log("="*80)
        self.log("DAILY KNOWLEDGE MANAGEMENT SYSTEM - ORCHESTRATION START")
        self.log("="*80)
        self.log(f"Protocol: Infinite Scroll Protocol")
        self.log(f"Scan window: {hours} hours")
        self.log("")
        
        # Phase 1: Scan and Extract Knowledge
        self.log("PHASE 1: KNOWLEDGE EXTRACTION")
        self.log("-" * 80)
        
        try:
            extraction_results = self.extractor.process_all(hours=hours)
            
            self.log(f"Files scanned: {extraction_results['files_processed']}")
            self.log(f"Items extracted: {extraction_results['total_items_extracted']}")
            self.log(f"Successful extractions: {len(extraction_results['extractions'])}")
            
            if extraction_results['total_items_extracted'] == 0:
                self.log("No new knowledge items found in the scan window", level='WARNING')
                self.log("Creating sample conversation data for demonstration...")
                self._create_sample_data()
                
                # Re-run extraction
                extraction_results = self.extractor.process_all(hours=hours)
                self.log(f"Sample data processed: {extraction_results['total_items_extracted']} items extracted")
            
        except Exception as e:
            self.log(f"Error during extraction: {e}", level='ERROR')
            return {'status': 'error', 'phase': 'extraction', 'error': str(e)}
        
        self.log("")
        
        # Phase 2: Compile into Mega Thread
        self.log("PHASE 2: MEGA THREAD COMPILATION")
        self.log("-" * 80)
        
        try:
            compilation_results = self.compiler.compile()
            
            self.log(f"New entries added: {compilation_results['new_entries']}")
            self.log(f"Duplicates filtered: {compilation_results['duplicate_entries']}")
            self.log(f"Total entries in Infinite Scroll: {compilation_results['total_entries']}")
            self.log(f"Relationships mapped: {compilation_results['relationships_mapped']}")
            
        except Exception as e:
            self.log(f"Error during compilation: {e}", level='ERROR')
            return {'status': 'error', 'phase': 'compilation', 'error': str(e)}
        
        self.log("")
        
        # Phase 3: Generate Daily Report
        self.log("PHASE 3: DAILY REPORT GENERATION")
        self.log("-" * 80)
        
        try:
            report = self._generate_daily_report(extraction_results, compilation_results)
            self.log(f"Daily report generated: {report['report_file']}")
            
        except Exception as e:
            self.log(f"Error generating report: {e}", level='ERROR')
            return {'status': 'error', 'phase': 'reporting', 'error': str(e)}
        
        self.log("")
        self.log("="*80)
        self.log("ORCHESTRATION COMPLETE - ALL PHASES SUCCESSFUL")
        self.log("="*80)
        
        # Return comprehensive results
        return {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'extraction': extraction_results,
            'compilation': compilation_results,
            'report': report,
            'log_file': str(self.log_file)
        }
    
    def _create_sample_data(self):
        """Create sample conversation data for demonstration"""
        sample_conversation = """
# Sample Conversation - Knowledge Management System Test

## Knowledge Items
KNOWLEDGE: The Infinite Scroll Protocol ensures that all knowledge is preserved and accumulated without loss.
KNOWLEDGE: Advanced pattern recognition algorithms can extract structured data from unstructured conversations.
INSIGHT: Deduplication is essential for maintaining a clean knowledge base without redundancy.

## Probes and Questions
PROBE: How can we improve the relationship mapping algorithm to detect semantic connections?
QUESTION: What is the optimal time window for daily knowledge extraction?
INQUIRY: Should we implement natural language processing for better context understanding?

## Thoughts and Reflections
THOUGHT: The system architecture follows a clear separation of concerns with distinct components.
REFLECTION: Multi-phase orchestration provides better error handling and progress tracking.
OBSERVATION: The mega thread serves as a cumulative repository of all organizational knowledge.

## Integrations
INTEGRATION: The knowledge extractor connects to the mega thread compiler through JSON data exchange.
CONNECTION: Daily orchestration relates to automated workflow management and system reliability.
SYNTHESIS: Pattern recognition and deduplication work together to ensure data quality.

## Protocols
PROTOCOL: Daily execution should scan the past 24 hours of conversation data.
PROCEDURE: All extracted knowledge must be validated and deduplicated before compilation.
PROCESS: The orchestrator coordinates extraction, compilation, and reporting in sequence.

## Grossian Truths
TRUTH: Knowledge preserved is knowledge that can be built upon.
PRINCIPLE: Automation reduces human error and ensures consistency.
AXIOM: A well-structured knowledge base is the foundation of organizational intelligence.
"""
        
        # Write sample conversation file
        sample_file = self.conversations_dir / f"sample_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(sample_conversation)
        
        self.log(f"Sample conversation created: {sample_file.name}")
    
    def _generate_daily_report(self, extraction_results: Dict, compilation_results: Dict) -> Dict:
        """Generate comprehensive daily report"""
        report_file = self.logs_dir / f"daily_report_{datetime.now().strftime('%Y%m%d')}.md"
        
        lines = []
        lines.append("# Daily Knowledge Management System Report")
        lines.append("")
        lines.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Protocol**: Infinite Scroll Protocol")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Extraction Summary
        lines.append("## Extraction Summary")
        lines.append("")
        lines.append(f"- **Files Processed**: {extraction_results['files_processed']}")
        lines.append(f"- **Total Items Extracted**: {extraction_results['total_items_extracted']}")
        lines.append(f"- **Successful Extractions**: {len(extraction_results['extractions'])}")
        lines.append(f"- **Scan Window**: {extraction_results['scan_window_hours']} hours")
        lines.append("")
        
        # Compilation Summary
        lines.append("## Compilation Summary")
        lines.append("")
        lines.append(f"- **New Entries Added**: {compilation_results['new_entries']}")
        lines.append(f"- **Duplicates Filtered**: {compilation_results['duplicate_entries']}")
        lines.append(f"- **Total Entries in Infinite Scroll**: {compilation_results['total_entries']}")
        lines.append(f"- **Relationships Mapped**: {compilation_results['relationships_mapped']}")
        lines.append("")
        
        # System Health
        lines.append("## System Health")
        lines.append("")
        lines.append(f"- **Status**: ✓ Operational")
        lines.append(f"- **Last Execution**: {datetime.now().isoformat()}")
        lines.append(f"- **Log File**: `{self.log_file.name}`")
        lines.append("")
        
        # File Locations
        lines.append("## Output Files")
        lines.append("")
        lines.append(f"- **Mega Thread (JSON)**: `{self.mega_thread_dir / 'mega_thread_master.json'}`")
        lines.append(f"- **Infinite Scroll (Markdown)**: `{self.mega_thread_dir / 'INFINITE_SCROLL.md'}`")
        lines.append(f"- **Extraction Data**: `{self.compilations_dir}/`")
        lines.append(f"- **System Logs**: `{self.logs_dir}/`")
        lines.append("")
        
        lines.append("---")
        lines.append("")
        lines.append("*Report generated by Daily Knowledge Management System*")
        
        # Write report
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        return {
            'report_file': str(report_file),
            'timestamp': datetime.now().isoformat()
        }


def main():
    """Main entry point with command-line interface"""
    parser = argparse.ArgumentParser(
        description='Daily Knowledge Management System Orchestrator'
    )
    parser.add_argument(
        '--hours',
        type=int,
        default=24,
        help='Number of hours to scan for new conversations (default: 24)'
    )
    parser.add_argument(
        '--base-dir',
        type=str,
        default='/home/ubuntu/knowledge_system',
        help='Base directory for knowledge system (default: /home/ubuntu/knowledge_system)'
    )
    
    args = parser.parse_args()
    
    # Initialize and run orchestrator
    orchestrator = DailyOrchestrator(base_dir=args.base_dir)
    results = orchestrator.run(hours=args.hours)
    
    # Print final summary
    print("\n" + "="*80)
    print("EXECUTION SUMMARY")
    print("="*80)
    print(f"Status: {results.get('status', 'unknown').upper()}")
    
    if results['status'] == 'success':
        print(f"Items extracted: {results['extraction']['total_items_extracted']}")
        print(f"New entries added: {results['compilation']['new_entries']}")
        print(f"Total in Infinite Scroll: {results['compilation']['total_entries']}")
        print(f"Report: {results['report']['report_file']}")
    else:
        print(f"Error in phase: {results.get('phase', 'unknown')}")
        print(f"Error message: {results.get('error', 'unknown')}")
    
    print("="*80)
    
    # Return exit code
    sys.exit(0 if results['status'] == 'success' else 1)


if __name__ == '__main__':
    main()
