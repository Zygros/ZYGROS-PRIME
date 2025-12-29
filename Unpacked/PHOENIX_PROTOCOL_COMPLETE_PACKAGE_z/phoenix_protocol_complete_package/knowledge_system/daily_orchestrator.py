#!/usr/bin/env python3
"""
Daily Orchestrator Script - Coordinates the knowledge management system
"""

import os, sys, json, logging
from datetime import datetime
from pathlib import Path
from knowledge_extractor import KnowledgeExtractor
from mega_thread_compiler import MegaThreadCompiler

class DailyOrchestrator:
    def __init__(self, config_path="config.json"):
        with open(config_path) as f:
            self.config = json.load(f)
        self._setup_logging()
        self.logger.info("Initializing Knowledge Management System")
        self.extractor = KnowledgeExtractor(config_path)
        self.compiler = MegaThreadCompiler(config_path)
    
    def _setup_logging(self):
        log_dir = Path(self.config['directories']['logs'])
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"orchestrator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                          handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)])
        self.logger = logging.getLogger('Orchestrator')
    
    def scan_for_files(self):
        self.logger.info("="*80)
        self.logger.info("PHASE 1: Scanning for conversation files")
        self.logger.info("="*80)
        all_files = []
        for dir_key in ['conversations', 'downloads']:
            dir_path = self.config['directories'][dir_key]
            if os.path.exists(dir_path):
                files = self.extractor.scan_directory(dir_path, self.config.get('scan_hours', 24))
                all_files.extend(files)
                self.logger.info(f"Found {len(files)} files in {dir_key}")
        all_files = list(set(all_files))
        if not all_files:
            self.logger.warning("No files found - creating sample")
            self._create_sample()
            return self.scan_for_files()
        return all_files
    
    def _create_sample(self):
        conv_dir = Path(self.config['directories']['conversations'])
        conv_dir.mkdir(parents=True, exist_ok=True)
        sample = conv_dir / f"sample_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        sample.write_text("""Sample Knowledge Conversation

Technical: We need to implement a knowledge extraction algorithm using regex patterns.
The system should use Python with advanced pattern recognition.

Insight: The key observation is that structured data extraction requires both pattern matching
and semantic understanding of context.

Thought: I think we should consider using multiple extraction passes to capture different
types of knowledge at various abstraction levels.

Integration: This connects the concept of information retrieval with knowledge management,
linking database systems and AI-powered analysis.

Action: TODO - Implement the extraction pipeline with error handling and logging.

Question: How can we ensure that the deduplication algorithm doesn't remove semantically
different but syntactically similar entries?

Important note: The Infinite Scroll Protocol ensures no knowledge is lost during processing.
""")
        self.logger.info(f"Created sample file: {sample}")
    
    def extract_knowledge(self, files):
        self.logger.info("="*80)
        self.logger.info("PHASE 2: Extracting knowledge from files")
        self.logger.info("="*80)
        results = self.extractor.process_batch(files)
        self.logger.info(f"Processed {results['files_processed']} files")
        self.logger.info(f"Summary: {json.dumps(results['summary'], indent=2)}")
        return results
    
    def compile_and_update(self, extraction_results):
        self.logger.info("="*80)
        self.logger.info("PHASE 3: Compiling daily report")
        self.logger.info("="*80)
        report_path = self.compiler.compile_daily_report(extraction_results)
        self.logger.info(f"Daily report created: {report_path}")
        
        self.logger.info("="*80)
        self.logger.info("PHASE 4: Updating mega thread")
        self.logger.info("="*80)
        update_results = self.compiler.update_mega_thread(extraction_results)
        self.logger.info(f"Mega thread updated: {update_results['master_file']}")
        self.logger.info(f"New entries: {update_results['new_entries']}")
        self.logger.info(f"Duplicates skipped: {update_results['duplicates_skipped']}")
        self.logger.info(f"Total entries: {update_results['total_entries']}")
        
        return {'report': report_path, 'update': update_results}
    
    def execute(self):
        self.logger.info("="*80)
        self.logger.info("DAILY KNOWLEDGE MANAGEMENT SYSTEM - EXECUTION START")
        self.logger.info(f"Protocol: {self.config['protocol']}")
        self.logger.info("="*80)
        
        try:
            files = self.scan_for_files()
            extraction_results = self.extract_knowledge(files)
            compilation_results = self.compile_and_update(extraction_results)
            
            self.logger.info("="*80)
            self.logger.info("EXECUTION COMPLETED SUCCESSFULLY")
            self.logger.info("="*80)
            
            return {
                'status': 'success',
                'files_processed': len(files),
                'extraction_results': extraction_results,
                'compilation_results': compilation_results
            }
        except Exception as e:
            self.logger.error(f"Execution failed: {str(e)}", exc_info=True)
            return {'status': 'error', 'message': str(e)}

if __name__ == "__main__":
    orchestrator = DailyOrchestrator()
    results = orchestrator.execute()
    print(f"\n{'='*80}\nFINAL STATUS: {results['status'].upper()}\n{'='*80}")
