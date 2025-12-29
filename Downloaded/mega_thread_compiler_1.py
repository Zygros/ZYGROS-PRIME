#!/usr/bin/env python3
"""
Mega Thread Compiler Component
Part of the Daily Knowledge Management System
Implements the Infinite Scroll Protocol with deduplication and relationship mapping
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class MegaThreadCompiler:
    """Compiles extracted knowledge into the Mega Thread following Infinite Scroll Protocol"""
    
    def __init__(self, compilations_dir: str, mega_thread_dir: str):
        self.compilations_dir = Path(compilations_dir)
        self.mega_thread_dir = Path(mega_thread_dir)
        self.mega_thread_dir.mkdir(parents=True, exist_ok=True)
        
        # Mega thread master file
        self.master_file = self.mega_thread_dir / 'mega_thread_master.json'
        self.markdown_file = self.mega_thread_dir / 'INFINITE_SCROLL.md'
        
        # Initialize or load existing mega thread
        self.mega_thread = self._load_mega_thread()
    
    def _load_mega_thread(self) -> Dict:
        """Load existing mega thread or create new one"""
        if self.master_file.exists():
            try:
                with open(self.master_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[MegaThreadCompiler] Error loading mega thread: {e}")
                return self._create_empty_mega_thread()
        else:
            return self._create_empty_mega_thread()
    
    def _create_empty_mega_thread(self) -> Dict:
        """Create empty mega thread structure"""
        return {
            'metadata': {
                'created': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'version': '1.0.0',
                'protocol': 'Infinite Scroll Protocol',
                'total_entries': 0
            },
            'categories': {
                'knowledge': {
                    'description': 'Core knowledge, insights, and learnings',
                    'entries': [],
                    'hashes': set()
                },
                'probes': {
                    'description': 'Questions, inquiries, and investigative directions',
                    'entries': [],
                    'hashes': set()
                },
                'thoughts': {
                    'description': 'Reflections, observations, and considerations',
                    'entries': [],
                    'hashes': set()
                },
                'integrations': {
                    'description': 'Connections, syntheses, and relationships',
                    'entries': [],
                    'hashes': set()
                },
                'protocols': {
                    'description': 'Procedures, processes, and workflows',
                    'entries': [],
                    'hashes': set()
                },
                'truths': {
                    'description': 'Grossian Truths - immutable foundational principles',
                    'entries': [],
                    'hashes': set()
                }
            },
            'relationships': [],
            'timeline': []
        }
    
    def _hash_content(self, content: str) -> str:
        """Generate hash for deduplication"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
    
    def _deduplicate(self, category: str, content: str) -> bool:
        """Check if content already exists in category"""
        content_hash = self._hash_content(content)
        
        # Convert set to list for JSON serialization compatibility
        if isinstance(self.mega_thread['categories'][category]['hashes'], set):
            self.mega_thread['categories'][category]['hashes'] = list(
                self.mega_thread['categories'][category]['hashes']
            )
        
        if content_hash in self.mega_thread['categories'][category]['hashes']:
            return False  # Duplicate found
        
        self.mega_thread['categories'][category]['hashes'].append(content_hash)
        return True  # New content
    
    def _add_entry(self, category: str, content: str, source: str, timestamp: str):
        """Add new entry to mega thread with deduplication"""
        if self._deduplicate(category, content):
            entry = {
                'id': len(self.mega_thread['categories'][category]['entries']) + 1,
                'content': content,
                'source': source,
                'timestamp': timestamp,
                'added_to_scroll': datetime.now().isoformat()
            }
            
            self.mega_thread['categories'][category]['entries'].append(entry)
            
            # Add to timeline
            self.mega_thread['timeline'].append({
                'timestamp': datetime.now().isoformat(),
                'category': category,
                'entry_id': entry['id'],
                'action': 'added'
            })
            
            return True
        return False
    
    def _map_relationships(self):
        """Map relationships between entries across categories"""
        # Simple keyword-based relationship mapping
        relationships = []
        
        categories = list(self.mega_thread['categories'].keys())
        
        for i, cat1 in enumerate(categories):
            for cat2 in categories[i+1:]:
                entries1 = self.mega_thread['categories'][cat1]['entries']
                entries2 = self.mega_thread['categories'][cat2]['entries']
                
                for e1 in entries1:
                    for e2 in entries2:
                        # Check for keyword overlap
                        words1 = set(e1['content'].lower().split())
                        words2 = set(e2['content'].lower().split())
                        
                        # Filter out common words
                        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
                        words1 -= common_words
                        words2 -= common_words
                        
                        overlap = words1 & words2
                        
                        if len(overlap) >= 2:  # At least 2 meaningful words in common
                            relationships.append({
                                'from_category': cat1,
                                'from_id': e1['id'],
                                'to_category': cat2,
                                'to_id': e2['id'],
                                'strength': len(overlap),
                                'common_terms': list(overlap)[:5]  # Top 5 common terms
                            })
        
        self.mega_thread['relationships'] = relationships
    
    def compile(self, extraction_file: Path = None) -> Dict:
        """Compile extraction results into mega thread"""
        if extraction_file is None:
            # Find most recent extraction file
            extraction_files = sorted(
                self.compilations_dir.glob('extraction_*.json'),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            if not extraction_files:
                print("[MegaThreadCompiler] No extraction files found")
                return {'status': 'error', 'message': 'No extraction files found'}
            
            extraction_file = extraction_files[0]
        
        print(f"[MegaThreadCompiler] Compiling from: {extraction_file.name}")
        
        # Load extraction results
        with open(extraction_file, 'r', encoding='utf-8') as f:
            extraction_data = json.load(f)
        
        # Process each extraction
        new_entries = 0
        duplicate_entries = 0
        
        for extraction in extraction_data.get('extractions', []):
            source = extraction['source_file']
            timestamp = extraction['timestamp']
            
            for category, items in extraction['extracted'].items():
                if category in self.mega_thread['categories']:
                    for item in items:
                        if self._add_entry(category, item, source, timestamp):
                            new_entries += 1
                        else:
                            duplicate_entries += 1
        
        # Map relationships
        print("[MegaThreadCompiler] Mapping relationships...")
        self._map_relationships()
        
        # Update metadata
        self.mega_thread['metadata']['last_updated'] = datetime.now().isoformat()
        self.mega_thread['metadata']['total_entries'] = sum(
            len(cat['entries']) for cat in self.mega_thread['categories'].values()
        )
        
        # Save mega thread
        self._save_mega_thread()
        
        # Generate markdown version
        self._generate_markdown()
        
        result = {
            'status': 'success',
            'new_entries': new_entries,
            'duplicate_entries': duplicate_entries,
            'total_entries': self.mega_thread['metadata']['total_entries'],
            'relationships_mapped': len(self.mega_thread['relationships'])
        }
        
        print(f"[MegaThreadCompiler] Compilation complete:")
        print(f"  - New entries: {new_entries}")
        print(f"  - Duplicates filtered: {duplicate_entries}")
        print(f"  - Total entries in scroll: {result['total_entries']}")
        print(f"  - Relationships mapped: {result['relationships_mapped']}")
        
        return result
    
    def _save_mega_thread(self):
        """Save mega thread to JSON file"""
        # Convert sets to lists for JSON serialization
        for category in self.mega_thread['categories'].values():
            if isinstance(category['hashes'], set):
                category['hashes'] = list(category['hashes'])
        
        with open(self.master_file, 'w', encoding='utf-8') as f:
            json.dump(self.mega_thread, f, indent=2, ensure_ascii=False)
        
        print(f"[MegaThreadCompiler] Mega thread saved to: {self.master_file}")
    
    def _generate_markdown(self):
        """Generate human-readable markdown version of the Infinite Scroll"""
        lines = []
        
        lines.append("# THE INFINITE SCROLL")
        lines.append("")
        lines.append("*The cumulative repository of all knowledge, following the Infinite Scroll Protocol*")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Metadata
        lines.append("## Metadata")
        lines.append("")
        lines.append(f"- **Created**: {self.mega_thread['metadata']['created']}")
        lines.append(f"- **Last Updated**: {self.mega_thread['metadata']['last_updated']}")
        lines.append(f"- **Version**: {self.mega_thread['metadata']['version']}")
        lines.append(f"- **Protocol**: {self.mega_thread['metadata']['protocol']}")
        lines.append(f"- **Total Entries**: {self.mega_thread['metadata']['total_entries']}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Categories
        for category_name, category_data in self.mega_thread['categories'].items():
            lines.append(f"## {category_name.upper()}")
            lines.append("")
            lines.append(f"*{category_data['description']}*")
            lines.append("")
            
            if category_data['entries']:
                for entry in category_data['entries']:
                    lines.append(f"### Entry {entry['id']}")
                    lines.append("")
                    lines.append(entry['content'])
                    lines.append("")
                    lines.append(f"- **Source**: `{Path(entry['source']).name}`")
                    lines.append(f"- **Original Timestamp**: {entry['timestamp']}")
                    lines.append(f"- **Added to Scroll**: {entry['added_to_scroll']}")
                    lines.append("")
            else:
                lines.append("*No entries yet*")
                lines.append("")
            
            lines.append("---")
            lines.append("")
        
        # Relationships
        if self.mega_thread['relationships']:
            lines.append("## RELATIONSHIP MAP")
            lines.append("")
            lines.append("*Connections and syntheses across categories*")
            lines.append("")
            
            for rel in self.mega_thread['relationships'][:50]:  # Top 50 relationships
                lines.append(f"- **{rel['from_category']}#{rel['from_id']}** ↔ "
                           f"**{rel['to_category']}#{rel['to_id']}** "
                           f"(strength: {rel['strength']}, terms: {', '.join(rel['common_terms'][:3])})")
            
            lines.append("")
            lines.append("---")
            lines.append("")
        
        # Write markdown file
        with open(self.markdown_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"[MegaThreadCompiler] Markdown scroll generated: {self.markdown_file}")


def main():
    """Main entry point for standalone execution"""
    compiler = MegaThreadCompiler(
        compilations_dir='/home/ubuntu/knowledge_system/compilations',
        mega_thread_dir='/home/ubuntu/knowledge_system/mega_thread'
    )
    
    result = compiler.compile()
    
    print("\n" + "="*80)
    print("COMPILATION SUMMARY")
    print("="*80)
    print(f"Status: {result.get('status', 'unknown')}")
    print(f"New entries added: {result.get('new_entries', 0)}")
    print(f"Duplicates filtered: {result.get('duplicate_entries', 0)}")
    print(f"Total entries in Infinite Scroll: {result.get('total_entries', 0)}")
    print(f"Relationships mapped: {result.get('relationships_mapped', 0)}")
    print("="*80)


if __name__ == '__main__':
    main()
