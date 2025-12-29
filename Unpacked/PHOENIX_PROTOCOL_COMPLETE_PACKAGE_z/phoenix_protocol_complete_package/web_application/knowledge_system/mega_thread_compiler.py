#!/usr/bin/env python3
"""
Mega Thread Compiler Component
Compiles extracted data into daily compilations with deduplication and relationship mapping.
Updates the mega thread master document following the Infinite Scroll Protocol.
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict


class MegaThreadCompiler:
    """Compiles knowledge extractions into the mega thread repository."""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize the compiler with configuration."""
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.mega_thread_path = Path(self.config['directories']['mega_thread'])
        self.master_file = self.mega_thread_path / self.config.get('master_thread_file', 'MASTER_THREAD.md')
        self.index_file = self.mega_thread_path / self.config.get('index_file', 'knowledge_index.json')
        
        # Initialize master file if it doesn't exist
        if not self.master_file.exists():
            self._initialize_master_file()
        
        # Load or initialize index
        self.index = self._load_index()
    
    def _initialize_master_file(self):
        """Initialize the mega thread master document."""
        initial_content = f"""# MEGA THREAD MASTER DOCUMENT
## Knowledge Management System - Infinite Scroll Protocol

**System**: {self.config['system_name']}
**Version**: {self.config['version']}
**Protocol**: {self.config['protocol']}
**Initialized**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Overview

This document serves as the central repository for all accumulated knowledge, insights, thoughts, and integrations extracted from daily conversations and interactions. Following the Infinite Scroll Protocol, all knowledge is preserved and accumulated without loss, organized by category and timestamped for traceability.

---

## Categories

"""
        for category in self.config['categories']:
            initial_content += f"- {category}\n"
        
        initial_content += """
---

## Knowledge Entries

*Entries are organized chronologically with the most recent at the top, following the Infinite Scroll Protocol.*

---

"""
        
        self.mega_thread_path.mkdir(parents=True, exist_ok=True)
        with open(self.master_file, 'w', encoding='utf-8') as f:
            f.write(initial_content)
    
    def _load_index(self) -> Dict:
        """Load the knowledge index for deduplication."""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'entries': {},
            'hashes': set(),
            'relationships': [],
            'statistics': {
                'total_entries': 0,
                'by_category': defaultdict(int)
            }
        }
    
    def _save_index(self):
        """Save the knowledge index."""
        # Convert set to list for JSON serialization
        index_copy = self.index.copy()
        if isinstance(index_copy.get('hashes'), set):
            index_copy['hashes'] = list(index_copy['hashes'])
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index_copy, f, indent=2)
    
    def _compute_hash(self, content: str) -> str:
        """Compute hash for deduplication."""
        # Normalize content for better deduplication
        normalized = content.lower().strip()
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def _is_duplicate(self, content: str) -> bool:
        """Check if content is a duplicate."""
        content_hash = self._compute_hash(content)
        if isinstance(self.index.get('hashes'), set):
            return content_hash in self.index['hashes']
        else:
            return content_hash in set(self.index.get('hashes', []))
    
    def _add_to_index(self, content: str, category: str, entry_id: str):
        """Add content to the deduplication index."""
        content_hash = self._compute_hash(content)
        
        if not isinstance(self.index.get('hashes'), set):
            self.index['hashes'] = set(self.index.get('hashes', []))
        
        self.index['hashes'].add(content_hash)
        self.index['entries'][entry_id] = {
            'hash': content_hash,
            'category': category,
            'timestamp': datetime.now().isoformat()
        }
        self.index['statistics']['total_entries'] += 1
        
        if 'by_category' not in self.index['statistics']:
            self.index['statistics']['by_category'] = {}
        
        if category not in self.index['statistics']['by_category']:
            self.index['statistics']['by_category'][category] = 0
        
        self.index['statistics']['by_category'][category] += 1
    
    def compile_daily_report(self, extraction_results: Dict) -> str:
        """Compile daily extraction results into a structured report."""
        timestamp = datetime.now()
        date_str = timestamp.strftime('%Y-%m-%d')
        time_str = timestamp.strftime('%H:%M:%S')
        
        report_path = Path(self.config['directories']['compilations']) / f"daily_compilation_{date_str}.md"
        
        report_content = f"""# Daily Knowledge Compilation
## {date_str} at {time_str}

**Files Processed**: {extraction_results['files_processed']}
**Protocol**: {self.config['protocol']}

---

## Summary Statistics

"""
        
        summary = extraction_results['summary']
        report_content += f"- **Technical Knowledge**: {summary['total_technical']} items\n"
        report_content += f"- **Insights & Probes**: {summary['total_insights']} items\n"
        report_content += f"- **Thoughts & Reflections**: {summary['total_thoughts']} items\n"
        report_content += f"- **Integrations & Connections**: {summary['total_integrations']} items\n"
        report_content += f"- **Action Items**: {summary['total_actions']} items\n"
        report_content += f"- **Questions & Inquiries**: {summary['total_questions']} items\n"
        
        report_content += "\n---\n\n## Extracted Knowledge by Category\n\n"
        
        # Process each extraction
        for extraction in extraction_results['extractions']:
            if 'error' in extraction:
                continue
            
            source = extraction['source_file']
            ek = extraction.get('extracted_knowledge', {})
            
            report_content += f"### Source: {source}\n\n"
            
            # Technical Knowledge
            if ek.get('technical_knowledge'):
                report_content += "#### Technical Knowledge\n\n"
                for item in ek['technical_knowledge']:
                    report_content += f"- {item}\n"
                report_content += "\n"
            
            # Insights & Probes
            if ek.get('insights_probes'):
                report_content += "#### Insights & Probes\n\n"
                for item in ek['insights_probes']:
                    report_content += f"- {item}\n"
                report_content += "\n"
            
            # Thoughts & Reflections
            if ek.get('thoughts_reflections'):
                report_content += "#### Thoughts & Reflections\n\n"
                for item in ek['thoughts_reflections']:
                    report_content += f"- {item}\n"
                report_content += "\n"
            
            # Integrations & Connections
            if ek.get('integrations_connections'):
                report_content += "#### Integrations & Connections\n\n"
                for item in ek['integrations_connections']:
                    report_content += f"- {item}\n"
                report_content += "\n"
            
            # Action Items
            if ek.get('action_items'):
                report_content += "#### Action Items\n\n"
                for item in ek['action_items']:
                    report_content += f"- [ ] {item}\n"
                report_content += "\n"
            
            # Questions & Inquiries
            if ek.get('questions_inquiries'):
                report_content += "#### Questions & Inquiries\n\n"
                for item in ek['questions_inquiries']:
                    report_content += f"- {item}\n"
                report_content += "\n"
            
            report_content += "---\n\n"
        
        # Write report
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return str(report_path)
    
    def update_mega_thread(self, extraction_results: Dict) -> Dict:
        """Update the mega thread master document with new entries."""
        timestamp = datetime.now()
        date_str = timestamp.strftime('%Y-%m-%d')
        time_str = timestamp.strftime('%H:%M:%S')
        
        new_entries = []
        duplicates_skipped = 0
        
        # Prepare new entries with deduplication
        for extraction in extraction_results['extractions']:
            if 'error' in extraction:
                continue
            
            source = extraction['source_file']
            ek = extraction.get('extracted_knowledge', {})
            
            for category_key, category_name in [
                ('technical_knowledge', 'Technical Knowledge'),
                ('insights_probes', 'Insights & Probes'),
                ('thoughts_reflections', 'Thoughts & Reflections'),
                ('integrations_connections', 'Integrations & Connections'),
                ('action_items', 'Action Items'),
                ('questions_inquiries', 'Questions & Inquiries')
            ]:
                items = ek.get(category_key, [])
                for item in items:
                    if not self._is_duplicate(item):
                        entry_id = f"{date_str}_{len(new_entries)}"
                        new_entries.append({
                            'id': entry_id,
                            'category': category_name,
                            'content': item,
                            'source': source,
                            'timestamp': timestamp.isoformat()
                        })
                        self._add_to_index(item, category_name, entry_id)
                    else:
                        duplicates_skipped += 1
        
        # Read current master file
        with open(self.master_file, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        # Find insertion point (after "## Knowledge Entries" section)
        insertion_marker = "## Knowledge Entries\n\n*Entries are organized chronologically with the most recent at the top, following the Infinite Scroll Protocol.*\n\n---\n\n"
        
        if insertion_marker in current_content:
            parts = current_content.split(insertion_marker, 1)
            header = parts[0] + insertion_marker
            existing_entries = parts[1] if len(parts) > 1 else ""
        else:
            header = current_content + "\n\n" + insertion_marker
            existing_entries = ""
        
        # Build new entries section
        new_entries_content = f"### Daily Update: {date_str} at {time_str}\n\n"
        new_entries_content += f"**New Entries**: {len(new_entries)} | **Duplicates Skipped**: {duplicates_skipped}\n\n"
        
        # Group by category
        by_category = defaultdict(list)
        for entry in new_entries:
            by_category[entry['category']].append(entry)
        
        for category in self.config['categories']:
            if category in by_category:
                new_entries_content += f"#### {category}\n\n"
                for entry in by_category[category]:
                    new_entries_content += f"- **[{entry['id']}]** {entry['content']}\n"
                    new_entries_content += f"  - *Source: {entry['source']}*\n"
                new_entries_content += "\n"
        
        new_entries_content += "---\n\n"
        
        # Combine and write
        updated_content = header + new_entries_content + existing_entries
        
        with open(self.master_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        # Save index
        self._save_index()
        
        return {
            'new_entries': len(new_entries),
            'duplicates_skipped': duplicates_skipped,
            'total_entries': self.index['statistics']['total_entries'],
            'master_file': str(self.master_file)
        }


if __name__ == "__main__":
    # Test the compiler
    compiler = MegaThreadCompiler()
    print("Mega Thread Compiler initialized successfully")
    print(f"Master file: {compiler.master_file}")
