#!/usr/bin/env python3
"""
Knowledge Extractor Component
Extracts knowledge, probes, thoughts, and integrations from conversation files
using advanced pattern recognition algorithms.
"""

import os
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple


class KnowledgeExtractor:
    """Extracts structured knowledge from conversation files."""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize the extractor with configuration."""
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.patterns = {
            'technical': [
                r'(?:implement|build|create|develop|design)\s+(?:a|an|the)?\s*(\w+(?:\s+\w+){0,5})',
                r'(?:using|with|via)\s+(\w+(?:\s+\w+){0,3})',
                r'(?:algorithm|method|approach|technique|pattern):\s*(.+?)(?:\.|$)',
                r'(?:code|script|function|class|module):\s*(.+?)(?:\.|$)',
            ],
            'insights': [
                r'(?:insight|observation|finding|discovery):\s*(.+?)(?:\.|$)',
                r'(?:interesting|notable|significant|important)\s+(?:that|is)\s+(.+?)(?:\.|$)',
                r'(?:probe|question|inquiry):\s*(.+?)(?:\?|$)',
                r'(?:why|how|what|when|where)\s+(.+?\?)',
            ],
            'thoughts': [
                r'(?:think|believe|consider|feel|sense)\s+(?:that)?\s*(.+?)(?:\.|$)',
                r'(?:reflection|thought|idea):\s*(.+?)(?:\.|$)',
                r'(?:perhaps|maybe|possibly|potentially)\s+(.+?)(?:\.|$)',
            ],
            'integrations': [
                r'(?:connect|link|relate|integrate)\s+(.+?)\s+(?:with|to|and)\s+(.+?)(?:\.|$)',
                r'(?:relationship|connection)\s+between\s+(.+?)\s+and\s+(.+?)(?:\.|$)',
                r'(?:similar to|like|reminds me of)\s+(.+?)(?:\.|$)',
            ],
            'actions': [
                r'(?:todo|task|action|need to|should|must)\s*:?\s*(.+?)(?:\.|$)',
                r'(?:will|going to|plan to)\s+(.+?)(?:\.|$)',
            ],
            'questions': [
                r'(?:question|inquiry):\s*(.+?\?)',
                r'^(?:why|how|what|when|where|who|which)\s+(.+?\?)',
            ]
        }
    
    def extract_from_file(self, filepath: str) -> Dict:
        """Extract knowledge from a single file."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            file_hash = hashlib.md5(content.encode()).hexdigest()
            
            extraction = {
                'source_file': os.path.basename(filepath),
                'file_path': filepath,
                'file_hash': file_hash,
                'timestamp': datetime.now().isoformat(),
                'extracted_knowledge': self._extract_patterns(content)
            }
            
            return extraction
        
        except Exception as e:
            return {
                'source_file': os.path.basename(filepath),
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _extract_patterns(self, content: str) -> Dict[str, List[str]]:
        """Extract patterns from content using regex."""
        extracted = {
            'technical_knowledge': [],
            'insights_probes': [],
            'thoughts_reflections': [],
            'integrations_connections': [],
            'action_items': [],
            'questions_inquiries': []
        }
        
        # Split content into lines for better extraction
        lines = content.split('\n')
        
        # Extract technical knowledge
        for pattern in self.patterns['technical']:
            for line in lines:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    item = match.group(1).strip() if match.lastindex >= 1 else match.group(0).strip()
                    if len(item) > 10 and item not in extracted['technical_knowledge']:
                        extracted['technical_knowledge'].append(item)
        
        # Extract insights and probes
        for pattern in self.patterns['insights']:
            for line in lines:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    item = match.group(1).strip() if match.lastindex >= 1 else match.group(0).strip()
                    if len(item) > 10 and item not in extracted['insights_probes']:
                        extracted['insights_probes'].append(item)
        
        # Extract thoughts and reflections
        for pattern in self.patterns['thoughts']:
            for line in lines:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    item = match.group(1).strip() if match.lastindex >= 1 else match.group(0).strip()
                    if len(item) > 10 and item not in extracted['thoughts_reflections']:
                        extracted['thoughts_reflections'].append(item)
        
        # Extract integrations and connections
        for pattern in self.patterns['integrations']:
            for line in lines:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    if match.lastindex >= 2:
                        item = f"{match.group(1).strip()} <-> {match.group(2).strip()}"
                    else:
                        item = match.group(1).strip() if match.lastindex >= 1 else match.group(0).strip()
                    if len(item) > 10 and item not in extracted['integrations_connections']:
                        extracted['integrations_connections'].append(item)
        
        # Extract action items
        for pattern in self.patterns['actions']:
            for line in lines:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    item = match.group(1).strip() if match.lastindex >= 1 else match.group(0).strip()
                    if len(item) > 10 and item not in extracted['action_items']:
                        extracted['action_items'].append(item)
        
        # Extract questions
        for pattern in self.patterns['questions']:
            for line in lines:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    item = match.group(1).strip() if match.lastindex >= 1 else match.group(0).strip()
                    if len(item) > 10 and item not in extracted['questions_inquiries']:
                        extracted['questions_inquiries'].append(item)
        
        # Also extract key sentences (sentences with important keywords)
        important_keywords = [
            'important', 'critical', 'essential', 'key', 'significant',
            'note', 'remember', 'crucial', 'vital', 'fundamental'
        ]
        
        for line in lines:
            for keyword in important_keywords:
                if keyword in line.lower() and len(line.strip()) > 20:
                    # Determine best category
                    if any(tech in line.lower() for tech in ['code', 'algorithm', 'function', 'method']):
                        if line.strip() not in extracted['technical_knowledge']:
                            extracted['technical_knowledge'].append(line.strip())
                    elif '?' in line:
                        if line.strip() not in extracted['questions_inquiries']:
                            extracted['questions_inquiries'].append(line.strip())
                    else:
                        if line.strip() not in extracted['insights_probes']:
                            extracted['insights_probes'].append(line.strip())
                    break
        
        return extracted
    
    def scan_directory(self, directory: str, hours: int = 24) -> List[str]:
        """Scan directory for files modified in the last N hours."""
        files_to_process = []
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        
        for pattern in self.config['file_patterns']:
            for filepath in Path(directory).rglob(pattern):
                if filepath.is_file():
                    mtime = filepath.stat().st_mtime
                    if mtime >= cutoff_time:
                        files_to_process.append(str(filepath))
        
        return files_to_process
    
    def process_batch(self, filepaths: List[str]) -> Dict:
        """Process a batch of files and return aggregated results."""
        results = {
            'timestamp': datetime.now().isoformat(),
            'files_processed': len(filepaths),
            'extractions': [],
            'summary': {
                'total_technical': 0,
                'total_insights': 0,
                'total_thoughts': 0,
                'total_integrations': 0,
                'total_actions': 0,
                'total_questions': 0
            }
        }
        
        for filepath in filepaths:
            extraction = self.extract_from_file(filepath)
            results['extractions'].append(extraction)
            
            if 'extracted_knowledge' in extraction:
                ek = extraction['extracted_knowledge']
                results['summary']['total_technical'] += len(ek.get('technical_knowledge', []))
                results['summary']['total_insights'] += len(ek.get('insights_probes', []))
                results['summary']['total_thoughts'] += len(ek.get('thoughts_reflections', []))
                results['summary']['total_integrations'] += len(ek.get('integrations_connections', []))
                results['summary']['total_actions'] += len(ek.get('action_items', []))
                results['summary']['total_questions'] += len(ek.get('questions_inquiries', []))
        
        return results


if __name__ == "__main__":
    # Test the extractor
    extractor = KnowledgeExtractor()
    print("Knowledge Extractor initialized successfully")
    print(f"Configuration loaded: {extractor.config['system_name']}")
