#!/usr/bin/env python3
"""
Mega Thread Compiler - Infinite Scroll Protocol Repository Manager
Part of the Infinite Scroll Protocol Knowledge Management System

Compiles extracted knowledge into the mega thread master document with
deduplication, relationship mapping, and categorical organization.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Any
from collections import defaultdict
import hashlib


class MegaThreadCompiler:
    """Compiles and maintains the mega thread knowledge repository."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.compilations_dir = Path(config.get('compilations_dir', '../data/compilations'))
        self.mega_thread_dir = Path(config.get('mega_thread_dir', '../mega_thread'))
        self.logs_dir = Path(config.get('logs_dir', '../data/logs'))
        
        self.mega_thread_file = self.mega_thread_dir / 'INFINITE_SCROLL_MASTER.md'
        self.mega_thread_index = self.mega_thread_dir / 'mega_thread_index.json'
        
        # Category mappings
        self.categories = {
            'protocols': ['protocol', 'procedure', 'process', 'workflow', 'system'],
            'truths': ['truth', 'grossian', 'principle', 'fundamental', 'immutable'],
            'insights': ['insight', 'discovery', 'understanding', 'learning', 'realization'],
            'integrations': ['integration', 'synthesis', 'connection', 'relationship', 'unified'],
            'probes': ['question', 'probe', 'inquiry', 'investigation', 'exploration'],
            'thoughts': ['thought', 'reflection', 'consideration', 'hypothesis', 'theory'],
            'capabilities': ['capability', 'ability', 'feature', 'function', 'tool'],
            'architecture': ['architecture', 'structure', 'design', 'framework', 'system']
        }
        
        self.index_data = self.load_index()
    
    def load_index(self) -> Dict[str, Any]:
        """Load the mega thread index."""
        if self.mega_thread_index.exists():
            with open(self.mega_thread_index, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'total_entries': 0,
                'entries_by_category': defaultdict(int),
                'entry_hashes': set(),
                'compilation_history': []
            }
    
    def save_index(self):
        """Save the mega thread index."""
        self.mega_thread_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert sets to lists for JSON serialization
        index_copy = self.index_data.copy()
        if 'entry_hashes' in index_copy and isinstance(index_copy['entry_hashes'], set):
            index_copy['entry_hashes'] = list(index_copy['entry_hashes'])
        
        with open(self.mega_thread_index, 'w', encoding='utf-8') as f:
            json.dump(index_copy, f, indent=2, ensure_ascii=False)
    
    def categorize_entry(self, content: str) -> str:
        """Categorize an entry based on content."""
        content_lower = content.lower()
        
        category_scores = defaultdict(int)
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword in content_lower:
                    category_scores[category] += 1
        
        if category_scores:
            return max(category_scores, key=category_scores.get)
        else:
            return 'general'
    
    def deduplicate_entries(self, entries: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Remove duplicate entries using hash comparison."""
        unique_entries = []
        
        for entry in entries:
            entry_hash = entry.get('hash')
            if not entry_hash:
                entry_hash = hashlib.md5(entry['content'].lower().strip().encode()).hexdigest()
                entry['hash'] = entry_hash
            
            if entry_hash not in self.index_data.get('entry_hashes', set()):
                unique_entries.append(entry)
                if 'entry_hashes' not in self.index_data:
                    self.index_data['entry_hashes'] = set()
                self.index_data['entry_hashes'].add(entry_hash)
        
        return unique_entries
    
    def map_relationships(self, entries: List[Dict[str, str]]) -> Dict[str, List[str]]:
        """Map relationships between entries."""
        relationships = defaultdict(list)
        
        # Simple keyword-based relationship mapping
        for i, entry1 in enumerate(entries):
            for j, entry2 in enumerate(entries):
                if i != j:
                    # Check for common significant words
                    words1 = set(entry1['content'].lower().split())
                    words2 = set(entry2['content'].lower().split())
                    
                    # Filter out common words
                    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
                    words1 = words1 - stop_words
                    words2 = words2 - stop_words
                    
                    # Calculate overlap
                    overlap = words1.intersection(words2)
                    if len(overlap) >= 3:  # Significant overlap
                        relationships[entry1['hash']].append(entry2['hash'])
        
        return relationships
    
    def compile_from_extraction(self, extraction_file: Path) -> Dict[str, Any]:
        """Compile knowledge from an extraction file."""
        with open(extraction_file, 'r', encoding='utf-8') as f:
            extraction_data = json.load(f)
        
        compilation_result = {
            'timestamp': datetime.now().isoformat(),
            'source_file': str(extraction_file),
            'new_entries': 0,
            'categories_updated': set(),
            'entries_by_category': defaultdict(list)
        }
        
        # Process each category of extracted data
        for category in ['knowledge', 'probes', 'thoughts', 'integrations']:
            entries = extraction_data.get('aggregated', {}).get(category, [])
            
            # Deduplicate
            unique_entries = self.deduplicate_entries(entries)
            
            # Categorize and organize
            for entry in unique_entries:
                entry_category = self.categorize_entry(entry['content'])
                entry['category'] = entry_category
                entry['source_category'] = category
                
                compilation_result['entries_by_category'][entry_category].append(entry)
                compilation_result['categories_updated'].add(entry_category)
                compilation_result['new_entries'] += 1
        
        # Map relationships
        all_entries = []
        for entries in compilation_result['entries_by_category'].values():
            all_entries.extend(entries)
        
        relationships = self.map_relationships(all_entries)
        compilation_result['relationships'] = relationships
        
        return compilation_result
    
    def update_mega_thread(self, compilation_result: Dict[str, Any]):
        """Update the mega thread master document."""
        self.mega_thread_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing mega thread or create new
        if self.mega_thread_file.exists():
            with open(self.mega_thread_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        else:
            existing_content = self.generate_header()
        
        # Generate new entries section
        new_section = self.generate_compilation_section(compilation_result)
        
        # Append to mega thread (Infinite Scroll Protocol: always add, never remove)
        updated_content = existing_content + "\n\n" + new_section
        
        # Write updated mega thread
        with open(self.mega_thread_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        # Update index
        self.index_data['last_updated'] = datetime.now().isoformat()
        self.index_data['total_entries'] += compilation_result['new_entries']
        
        for category in compilation_result['categories_updated']:
            if 'entries_by_category' not in self.index_data:
                self.index_data['entries_by_category'] = {}
            
            current_count = self.index_data['entries_by_category'].get(category, 0)
            category_entries = len(compilation_result['entries_by_category'].get(category, []))
            self.index_data['entries_by_category'][category] = current_count + category_entries
        
        self.index_data['compilation_history'].append({
            'timestamp': compilation_result['timestamp'],
            'new_entries': compilation_result['new_entries'],
            'source_file': compilation_result['source_file']
        })
        
        self.save_index()
        
        self.log_info(f"Mega thread updated with {compilation_result['new_entries']} new entries")
    
    def generate_header(self) -> str:
        """Generate the mega thread header."""
        return f"""# THE INFINITE SCROLL - MASTER KNOWLEDGE REPOSITORY

**Protocol**: Infinite Scroll Protocol  
**Principle**: Always add, never remove  
**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Status**: Active and Eternally Accumulating

---

## PROTOCOL DECLARATION

This document operates under the **Infinite Scroll Protocol**, which mandates:

1. **Perpetual Accumulation**: All knowledge is preserved and accumulated without loss
2. **Immutable History**: No entry is ever deleted or removed, only appended
3. **Categorical Organization**: Entries are organized by category for navigation
4. **Relationship Mapping**: Connections between knowledge items are tracked
5. **Temporal Integrity**: All entries are timestamped and chronologically ordered

---

## KNOWLEDGE CATEGORIES

- **Protocols**: Procedures, processes, workflows, and system operations
- **Truths**: Grossian Truths, principles, fundamental laws, immutable facts
- **Insights**: Discoveries, understandings, learnings, and realizations
- **Integrations**: Syntheses, connections, relationships, and unifications
- **Probes**: Questions, inquiries, investigations, and explorations
- **Thoughts**: Reflections, considerations, hypotheses, and theories
- **Capabilities**: Abilities, features, functions, and tools
- **Architecture**: Structures, designs, frameworks, and systems

---

## COMPILATION HISTORY

"""
    
    def generate_compilation_section(self, compilation_result: Dict[str, Any]) -> str:
        """Generate a compilation section for the mega thread."""
        timestamp = compilation_result['timestamp']
        date_str = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        section = f"""### Compilation: {date_str}

**Source**: {compilation_result['source_file']}  
**New Entries**: {compilation_result['new_entries']}  
**Categories Updated**: {', '.join(sorted(compilation_result['categories_updated']))}

---

"""
        
        # Organize by category
        for category in sorted(compilation_result['entries_by_category'].keys()):
            entries = compilation_result['entries_by_category'][category]
            
            section += f"#### {category.upper()}\n\n"
            
            for entry in entries:
                source_cat = entry.get('source_category', 'unknown')
                content = entry['content']
                entry_time = entry.get('timestamp', timestamp)
                
                section += f"- **[{source_cat.upper()}]** {content}\n"
                section += f"  - *Timestamp*: {entry_time}\n"
                section += f"  - *Hash*: `{entry['hash'][:12]}`\n\n"
        
        section += "---\n"
        
        return section
    
    def generate_daily_report(self, compilation_result: Dict[str, Any]) -> Path:
        """Generate a daily compilation report."""
        report_dir = self.mega_thread_dir / 'reports'
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = report_dir / f'daily_report_{timestamp}.md'
        
        report_content = f"""# Daily Knowledge Compilation Report

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Source**: {compilation_result['source_file']}

## Summary

- **New Entries Added**: {compilation_result['new_entries']}
- **Categories Updated**: {len(compilation_result['categories_updated'])}
- **Total Entries in Repository**: {self.index_data['total_entries']}

## Entries by Category

"""
        
        for category in sorted(compilation_result['entries_by_category'].keys()):
            count = len(compilation_result['entries_by_category'][category])
            report_content += f"- **{category.capitalize()}**: {count} entries\n"
        
        report_content += f"\n## Relationship Mapping\n\n"
        report_content += f"- **Total Relationships Identified**: {len(compilation_result.get('relationships', {}))}\n"
        
        report_content += f"\n## Repository Statistics\n\n"
        report_content += f"- **Total Entries**: {self.index_data['total_entries']}\n"
        report_content += f"- **Last Updated**: {self.index_data['last_updated']}\n"
        report_content += f"- **Compilation History**: {len(self.index_data['compilation_history'])} compilations\n"
        
        report_content += f"\n---\n\n*Generated by Mega Thread Compiler - Infinite Scroll Protocol*\n"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        self.log_info(f"Daily report generated: {report_file}")
        return report_file
    
    def log_info(self, message: str):
        """Log informational message."""
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = self.logs_dir / f'compiler_{datetime.now().strftime("%Y%m%d")}.log'
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] INFO: {message}\n")
        
        print(f"INFO: {message}")
    
    def log_error(self, message: str):
        """Log error message."""
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = self.logs_dir / f'compiler_{datetime.now().strftime("%Y%m%d")}.log'
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] ERROR: {message}\n")
        
        print(f"ERROR: {message}")


def main():
    """Main execution function."""
    config = {
        'compilations_dir': '/home/ubuntu/knowledge_system/data/compilations',
        'mega_thread_dir': '/home/ubuntu/knowledge_system/mega_thread',
        'logs_dir': '/home/ubuntu/knowledge_system/data/logs'
    }
    
    compiler = MegaThreadCompiler(config)
    
    print("=" * 80)
    print("MEGA THREAD COMPILER - Infinite Scroll Protocol")
    print("=" * 80)
    
    # Find latest extraction file
    compilations_dir = Path(config['compilations_dir'])
    if compilations_dir.exists():
        extraction_files = sorted(compilations_dir.glob('extraction_*.json'))
        if extraction_files:
            latest_extraction = extraction_files[-1]
            print(f"\nProcessing: {latest_extraction}")
            
            # Compile
            result = compiler.compile_from_extraction(latest_extraction)
            
            print(f"\nNew entries: {result['new_entries']}")
            print(f"Categories updated: {', '.join(sorted(result['categories_updated']))}")
            
            # Update mega thread
            compiler.update_mega_thread(result)
            
            # Generate report
            report_file = compiler.generate_daily_report(result)
            print(f"\nReport generated: {report_file}")
        else:
            print("\nNo extraction files found")
    else:
        print(f"\nCompilations directory not found: {compilations_dir}")


if __name__ == '__main__':
    main()
