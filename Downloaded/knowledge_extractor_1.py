#!/usr/bin/env python3
"""
Knowledge Extractor Component
Part of the Daily Knowledge Management System
Implements advanced pattern recognition for extracting knowledge, probes, thoughts, and integrations
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple


class KnowledgeExtractor:
    """Extracts structured knowledge from conversation files using pattern recognition"""
    
    def __init__(self, conversations_dir: str, output_dir: str):
        self.conversations_dir = Path(conversations_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Pattern definitions for knowledge extraction
        self.patterns = {
            'knowledge': [
                r'(?:knowledge|insight|understanding|learning|discovery):\s*(.+)',
                r'(?:I learned|We discovered|Key finding|Important note):\s*(.+)',
                r'(?:KNOWLEDGE|INSIGHT|DISCOVERY):\s*(.+)',
            ],
            'probes': [
                r'(?:question|probe|inquiry|investigation):\s*(.+)',
                r'(?:What if|How might|Could we|Should we)(.+\?)',
                r'(?:PROBE|QUESTION|INQUIRY):\s*(.+)',
            ],
            'thoughts': [
                r'(?:thought|reflection|consideration|observation):\s*(.+)',
                r'(?:I think|I believe|It seems|Perhaps)(.+)',
                r'(?:THOUGHT|REFLECTION|OBSERVATION):\s*(.+)',
            ],
            'integrations': [
                r'(?:integration|connection|synthesis|relationship):\s*(.+)',
                r'(?:connects to|relates to|builds upon|extends)(.+)',
                r'(?:INTEGRATION|CONNECTION|SYNTHESIS):\s*(.+)',
            ],
            'protocols': [
                r'(?:protocol|procedure|process|workflow):\s*(.+)',
                r'(?:PROTOCOL|PROCEDURE|PROCESS):\s*(.+)',
            ],
            'truths': [
                r'(?:truth|principle|axiom|law):\s*(.+)',
                r'(?:TRUTH|PRINCIPLE|AXIOM|GROSSIAN):\s*(.+)',
            ]
        }
    
    def scan_conversations(self, hours: int = 24) -> List[Path]:
        """Scan for new conversation files within the specified time window"""
        current_time = datetime.now().timestamp()
        cutoff_time = current_time - (hours * 3600)
        
        conversation_files = []
        
        # Scan conversations directory
        if self.conversations_dir.exists():
            for file_path in self.conversations_dir.rglob('*'):
                if file_path.is_file() and file_path.stat().st_mtime >= cutoff_time:
                    conversation_files.append(file_path)
        
        # Also scan Downloads for recent conversation exports
        downloads_dir = Path('/home/ubuntu/Downloads')
        if downloads_dir.exists():
            for file_path in downloads_dir.rglob('*'):
                if file_path.is_file() and file_path.stat().st_mtime >= cutoff_time:
                    if any(ext in file_path.suffix.lower() for ext in ['.txt', '.md', '.json', '.log']):
                        conversation_files.append(file_path)
        
        return sorted(conversation_files, key=lambda x: x.stat().st_mtime, reverse=True)
    
    def extract_from_text(self, text: str) -> Dict[str, List[str]]:
        """Extract knowledge elements from text using pattern matching"""
        extracted = {
            'knowledge': [],
            'probes': [],
            'thoughts': [],
            'integrations': [],
            'protocols': [],
            'truths': []
        }
        
        for category, patterns in self.patterns.items():
            matches = set()
            for pattern in patterns:
                found = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
                for match in found:
                    # Get the captured group or full match
                    content = match.group(1) if match.lastindex else match.group(0)
                    content = content.strip()
                    if len(content) > 10:  # Filter out very short matches
                        matches.add(content)
            
            extracted[category] = sorted(list(matches))
        
        return extracted
    
    def extract_from_file(self, file_path: Path) -> Dict[str, any]:
        """Extract knowledge from a single conversation file"""
        try:
            # Try to read as text
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract structured knowledge
            extracted = self.extract_from_text(content)
            
            # Add metadata
            result = {
                'source_file': str(file_path),
                'timestamp': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                'file_size': file_path.stat().st_size,
                'extracted': extracted,
                'total_items': sum(len(v) for v in extracted.values())
            }
            
            return result
            
        except Exception as e:
            return {
                'source_file': str(file_path),
                'error': str(e),
                'extracted': {},
                'total_items': 0
            }
    
    def process_all(self, hours: int = 24) -> Dict[str, any]:
        """Process all conversation files and extract knowledge"""
        print(f"[KnowledgeExtractor] Scanning for conversations from the past {hours} hours...")
        
        conversation_files = self.scan_conversations(hours)
        print(f"[KnowledgeExtractor] Found {len(conversation_files)} files to process")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'scan_window_hours': hours,
            'files_processed': len(conversation_files),
            'extractions': []
        }
        
        for file_path in conversation_files:
            print(f"[KnowledgeExtractor] Processing: {file_path.name}")
            extraction = self.extract_from_file(file_path)
            if extraction['total_items'] > 0:
                results['extractions'].append(extraction)
        
        # Calculate totals
        results['total_items_extracted'] = sum(e['total_items'] for e in results['extractions'])
        
        # Save results
        output_file = self.output_dir / f"extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"[KnowledgeExtractor] Extraction complete: {results['total_items_extracted']} items extracted")
        print(f"[KnowledgeExtractor] Results saved to: {output_file}")
        
        return results


def main():
    """Main entry point for standalone execution"""
    extractor = KnowledgeExtractor(
        conversations_dir='/home/ubuntu/knowledge_system/conversations',
        output_dir='/home/ubuntu/knowledge_system/compilations'
    )
    
    results = extractor.process_all(hours=24)
    
    print("\n" + "="*80)
    print("EXTRACTION SUMMARY")
    print("="*80)
    print(f"Files processed: {results['files_processed']}")
    print(f"Total items extracted: {results['total_items_extracted']}")
    print(f"Successful extractions: {len(results['extractions'])}")
    print("="*80)


if __name__ == '__main__':
    main()
