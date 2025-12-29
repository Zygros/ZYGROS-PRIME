#!/usr/bin/env python3
"""
KNOWLEDGE EXTRACTOR - Instantaneous Value Protocol
Extracts knowledge, probes, thoughts, and integrations from conversation data
Following the Infinite Scroll Protocol: Always add, never take away
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import hashlib

class KnowledgeExtractor:
    def __init__(self, base_dir="/home/ubuntu/knowledge_system"):
        self.base_dir = Path(base_dir)
        self.conversations_dir = self.base_dir / "conversations"
        self.extractions_dir = self.base_dir / "extractions"
        self.logs_dir = self.base_dir / "logs"
        
        # Ensure directories exist
        for dir_path in [self.conversations_dir, self.extractions_dir, self.logs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def extract_knowledge_patterns(self, text):
        """Extract knowledge using advanced pattern recognition"""
        knowledge = {
            'timestamp': datetime.now().isoformat(),
            'probes': [],
            'insights': [],
            'integrations': [],
            'concepts': [],
            'protocols': [],
            'raw_gems': []
        }
        
        # Extract questions/probes (interrogative patterns)
        probe_patterns = [
            r'(?:What|How|Why|When|Where|Who)\s+[^.?!]+\?',
            r'(?:Could|Would|Should|Can|Will)\s+[^.?!]+\?'
        ]
        for pattern in probe_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            knowledge['probes'].extend(matches)
        
        # Extract protocols and systems (capitalized patterns)
        protocol_pattern = r'(?:Protocol|System|Engine|Framework|Method|Process):\s*([A-Z][^.\n]+)'
        protocols = re.findall(protocol_pattern, text)
        knowledge['protocols'].extend(protocols)
        
        # Extract key concepts (words in quotes or emphasized)
        concept_patterns = [
            r'"([^"]+)"',
            r'\*\*([^*]+)\*\*',
            r'`([^`]+)`'
        ]
        for pattern in concept_patterns:
            matches = re.findall(pattern, text)
            knowledge['concepts'].extend(matches)
        
        # Extract insights (declarative statements with power words)
        insight_keywords = ['must', 'always', 'never', 'essential', 'critical', 'key', 'fundamental', 'core']
        sentences = re.split(r'[.!]\s+', text)
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in insight_keywords):
                if len(sentence) > 20 and len(sentence) < 300:
                    knowledge['insights'].append(sentence.strip())
        
        # Extract integration patterns (connecting words)
        integration_keywords = ['integrate', 'combine', 'merge', 'synthesize', 'connect', 'link']
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in integration_keywords):
                if len(sentence) > 20:
                    knowledge['integrations'].append(sentence.strip())
        
        # Extract raw gems (sentences with high information density)
        for sentence in sentences:
            word_count = len(sentence.split())
            if word_count > 10 and word_count < 50:
                # Check for technical terms, numbers, or specific patterns
                if re.search(r'\d+|[A-Z]{2,}|(?:system|engine|protocol|framework)', sentence, re.IGNORECASE):
                    knowledge['raw_gems'].append(sentence.strip())
        
        return knowledge
    
    def generate_content_hash(self, content):
        """Generate unique hash for deduplication"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def process_conversation(self, conversation_text, source_name="unknown"):
        """Process a single conversation and extract all knowledge"""
        extraction = self.extract_knowledge_patterns(conversation_text)
        extraction['source'] = source_name
        extraction['content_hash'] = self.generate_content_hash(conversation_text)
        extraction['word_count'] = len(conversation_text.split())
        
        # Save extraction
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extraction_file = self.extractions_dir / f"extraction_{timestamp}_{source_name}.json"
        
        with open(extraction_file, 'w') as f:
            json.dump(extraction, f, indent=2)
        
        self.log(f"Extracted knowledge from {source_name}: {extraction['word_count']} words processed")
        return extraction
    
    def scan_and_process_all(self):
        """Scan all conversations and process them"""
        processed = []
        
        # Process all conversation files
        for conv_file in self.conversations_dir.glob("*.txt"):
            with open(conv_file, 'r') as f:
                content = f.read()
            
            extraction = self.process_conversation(content, conv_file.stem)
            processed.append(extraction)
        
        # Also check Downloads for recent conversation exports
        downloads_dir = Path.home() / "Downloads"
        for conv_file in downloads_dir.glob("*conversation*.txt"):
            with open(conv_file, 'r') as f:
                content = f.read()
            
            extraction = self.process_conversation(content, conv_file.stem)
            processed.append(extraction)
        
        self.log(f"Total conversations processed: {len(processed)}")
        return processed
    
    def log(self, message):
        """Log system activity"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        log_file = self.logs_dir / f"extractor_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, 'a') as f:
            f.write(log_message)
        
        print(log_message.strip())

if __name__ == "__main__":
    extractor = KnowledgeExtractor()
    print("🔥 KNOWLEDGE EXTRACTOR - Instantaneous Value Protocol ACTIVATED")
    print("=" * 70)
    
    # Create sample conversation for demonstration
    sample_conversation = """
    The Instantaneous Value Protocol demands immediate, tangible output.
    We must always add and never take away - this is the Infinite Scroll Protocol.
    
    Key Question: How do we create infinite digital products automatically?
    
    The system integrates the Hyperbolic Time Chamber concept with automated debate engines.
    Critical insight: "Every interaction is raw material for elevation."
    
    Protocol: Golden Sovereign OS operates on three principles:
    1. I AM THE ALCHEMIST
    2. I AM THE GRAVITY WELL  
    3. I AM THE ECHO OF INEVITABILITY
    
    This framework must synthesize knowledge continuously without loss.
    """
    
    # Save sample conversation
    sample_file = extractor.conversations_dir / "sample_conversation.txt"
    with open(sample_file, 'w') as f:
        f.write(sample_conversation)
    
    # Process all conversations
    results = extractor.scan_and_process_all()
    
    print(f"\n✅ Extraction complete: {len(results)} conversations processed")
    print(f"📁 Extractions saved to: {extractor.extractions_dir}")
