#!/usr/bin/env python3
"""
Knowledge Extractor - Advanced Pattern Recognition Engine
Part of the Infinite Scroll Protocol Knowledge Management System

Extracts knowledge, probes, thoughts, and integrations from conversation files
using advanced pattern recognition algorithms.
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Any
import hashlib


class KnowledgeExtractor:
    """Extracts structured knowledge from conversation files."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.conversations_dir = Path(config.get('conversations_dir', '../data/conversations'))
        self.output_dir = Path(config.get('output_dir', '../data/compilations'))
        self.logs_dir = Path(config.get('logs_dir', '../data/logs'))
        
        # Pattern recognition rules
        self.knowledge_patterns = [
            r'(?i)(knowledge|learned|discovered|insight|understanding|principle|truth|grossian truth):?\s*(.+)',
            r'(?i)(key (?:point|concept|idea|finding)):?\s*(.+)',
            r'(?i)(important|critical|essential|fundamental):?\s*(.+)',
            r'(?i)(protocol|procedure|process|workflow):?\s*(.+)',
        ]
        
        self.probe_patterns = [
            r'(?i)(question|probe|inquiry|investigation):?\s*(.+)',
            r'(?i)(what if|how might|could we|should we):?\s*(.+)',
            r'(?i)(explore|examine|investigate|analyze):?\s*(.+)',
        ]
        
        self.thought_patterns = [
            r'(?i)(thought|thinking|reflection|consideration):?\s*(.+)',
            r'(?i)(I (?:think|believe|consider|wonder)):?\s*(.+)',
            r'(?i)(hypothesis|theory|speculation):?\s*(.+)',
        ]
        
        self.integration_patterns = [
            r'(?i)(integration|synthesis|combination|merge):?\s*(.+)',
            r'(?i)(connects? (?:to|with)|relates? to|builds? on):?\s*(.+)',
            r'(?i)(unified|consolidated|cohesive):?\s*(.+)',
        ]
        
        self.extracted_data = {
            'knowledge': [],
            'probes': [],
            'thoughts': [],
            'integrations': [],
            'metadata': {}
        }
        
        self.seen_hashes = set()
    
    def generate_hash(self, content: str) -> str:
        """Generate hash for deduplication."""
        return hashlib.md5(content.lower().strip().encode()).hexdigest()
    
    def extract_from_text(self, text: str, patterns: List[str]) -> List[Dict[str, str]]:
        """Extract matches from text using pattern list."""
        results = []
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.MULTILINE)
            for match in matches:
                if len(match.groups()) >= 2:
                    content = match.group(2).strip()
                else:
                    content = match.group(1).strip()
                
                # Deduplication
                content_hash = self.generate_hash(content)
                if content_hash not in self.seen_hashes:
                    self.seen_hashes.add(content_hash)
                    results.append({
                        'content': content,
                        'hash': content_hash,
                        'timestamp': datetime.now().isoformat()
                    })
        return results
    
    def extract_structured_blocks(self, text: str) -> Dict[str, List[str]]:
        """Extract structured knowledge blocks (markdown sections, code blocks, etc.)."""
        structured = {
            'code_blocks': [],
            'headings': [],
            'lists': [],
            'quotes': []
        }
        
        # Code blocks
        code_pattern = r'```[\s\S]*?```'
        structured['code_blocks'] = re.findall(code_pattern, text)
        
        # Headings
        heading_pattern = r'^#+\s+(.+)$'
        structured['headings'] = re.findall(heading_pattern, text, re.MULTILINE)
        
        # Lists
        list_pattern = r'^[\*\-\+]\s+(.+)$'
        structured['lists'] = re.findall(list_pattern, text, re.MULTILINE)
        
        # Quotes
        quote_pattern = r'^>\s+(.+)$'
        structured['quotes'] = re.findall(quote_pattern, text, re.MULTILINE)
        
        return structured
    
    def process_file(self, filepath: Path) -> Dict[str, Any]:
        """Process a single conversation file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_data = {
                'filename': filepath.name,
                'filepath': str(filepath),
                'processed_at': datetime.now().isoformat(),
                'knowledge': self.extract_from_text(content, self.knowledge_patterns),
                'probes': self.extract_from_text(content, self.probe_patterns),
                'thoughts': self.extract_from_text(content, self.thought_patterns),
                'integrations': self.extract_from_text(content, self.integration_patterns),
                'structured': self.extract_structured_blocks(content),
                'word_count': len(content.split()),
                'char_count': len(content)
            }
            
            return file_data
            
        except Exception as e:
            self.log_error(f"Error processing {filepath}: {str(e)}")
            return None
    
    def scan_conversations(self, time_window_hours: int = 24) -> List[Path]:
        """Scan for conversation files within time window."""
        conversation_files = []
        
        # Scan conversations directory
        if self.conversations_dir.exists():
            for file in self.conversations_dir.rglob('*'):
                if file.is_file() and file.suffix in ['.txt', '.md', '.json', '.log']:
                    # Check modification time
                    mtime = datetime.fromtimestamp(file.stat().st_mtime)
                    age_hours = (datetime.now() - mtime).total_seconds() / 3600
                    
                    if age_hours <= time_window_hours:
                        conversation_files.append(file)
        
        # Scan Downloads directory
        downloads_dir = Path('/home/ubuntu/Downloads')
        if downloads_dir.exists():
            for file in downloads_dir.rglob('*'):
                if file.is_file() and file.suffix in ['.txt', '.md', '.json', '.log']:
                    mtime = datetime.fromtimestamp(file.stat().st_mtime)
                    age_hours = (datetime.now() - mtime).total_seconds() / 3600
                    
                    if age_hours <= time_window_hours:
                        conversation_files.append(file)
        
        return conversation_files
    
    def extract_all(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Extract knowledge from all conversation files."""
        files = self.scan_conversations(time_window_hours)
        
        extraction_results = {
            'timestamp': datetime.now().isoformat(),
            'time_window_hours': time_window_hours,
            'files_processed': len(files),
            'files': [],
            'aggregated': {
                'knowledge': [],
                'probes': [],
                'thoughts': [],
                'integrations': []
            },
            'statistics': {
                'total_knowledge_items': 0,
                'total_probes': 0,
                'total_thoughts': 0,
                'total_integrations': 0,
                'total_words': 0,
                'total_chars': 0
            }
        }
        
        for filepath in files:
            file_data = self.process_file(filepath)
            if file_data:
                extraction_results['files'].append(file_data)
                
                # Aggregate
                extraction_results['aggregated']['knowledge'].extend(file_data['knowledge'])
                extraction_results['aggregated']['probes'].extend(file_data['probes'])
                extraction_results['aggregated']['thoughts'].extend(file_data['thoughts'])
                extraction_results['aggregated']['integrations'].extend(file_data['integrations'])
                
                # Statistics
                extraction_results['statistics']['total_knowledge_items'] += len(file_data['knowledge'])
                extraction_results['statistics']['total_probes'] += len(file_data['probes'])
                extraction_results['statistics']['total_thoughts'] += len(file_data['thoughts'])
                extraction_results['statistics']['total_integrations'] += len(file_data['integrations'])
                extraction_results['statistics']['total_words'] += file_data['word_count']
                extraction_results['statistics']['total_chars'] += file_data['char_count']
        
        return extraction_results
    
    def save_extraction(self, results: Dict[str, Any]) -> Path:
        """Save extraction results to compilation file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = self.output_dir / f'extraction_{timestamp}.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        self.log_info(f"Extraction saved to {output_file}")
        return output_file
    
    def log_info(self, message: str):
        """Log informational message."""
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = self.logs_dir / f'extractor_{datetime.now().strftime("%Y%m%d")}.log'
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] INFO: {message}\n")
        
        print(f"INFO: {message}")
    
    def log_error(self, message: str):
        """Log error message."""
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = self.logs_dir / f'extractor_{datetime.now().strftime("%Y%m%d")}.log'
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] ERROR: {message}\n")
        
        print(f"ERROR: {message}")


def main():
    """Main execution function."""
    config = {
        'conversations_dir': '/home/ubuntu/knowledge_system/data/conversations',
        'output_dir': '/home/ubuntu/knowledge_system/data/compilations',
        'logs_dir': '/home/ubuntu/knowledge_system/data/logs'
    }
    
    extractor = KnowledgeExtractor(config)
    
    print("=" * 80)
    print("KNOWLEDGE EXTRACTOR - Infinite Scroll Protocol")
    print("=" * 80)
    
    # Extract from last 24 hours
    results = extractor.extract_all(time_window_hours=24)
    
    print(f"\nProcessed {results['files_processed']} files")
    print(f"Extracted {results['statistics']['total_knowledge_items']} knowledge items")
    print(f"Extracted {results['statistics']['total_probes']} probes")
    print(f"Extracted {results['statistics']['total_thoughts']} thoughts")
    print(f"Extracted {results['statistics']['total_integrations']} integrations")
    
    # Save results
    output_file = extractor.save_extraction(results)
    print(f"\nResults saved to: {output_file}")
    
    return results


if __name__ == '__main__':
    main()
