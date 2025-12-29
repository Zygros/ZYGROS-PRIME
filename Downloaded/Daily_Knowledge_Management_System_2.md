# Daily Knowledge Management System

**An automated system for extracting, compiling, and preserving knowledge following the Infinite Scroll Protocol**

---

## Quick Start

### Run Daily Update

```bash
cd /home/ubuntu/knowledge_system
python3 scripts/daily_orchestrator.py --hours 24
```

This will:
1. Scan for new conversation files from the past 24 hours
2. Extract knowledge using pattern recognition
3. Compile into the Mega Thread with deduplication
4. Update the Infinite Scroll
5. Generate a daily report

---

## System Components

### Core Scripts

- **`daily_orchestrator.py`** - Main orchestration script
- **`knowledge_extractor.py`** - Pattern-based knowledge extraction
- **`mega_thread_compiler.py`** - Compilation and deduplication

### Directories

- **`conversations/`** - Place conversation files here for processing
- **`compilations/`** - Intermediate extraction results (JSON)
- **`mega_thread/`** - The Infinite Scroll and master data
- **`logs/`** - System logs and daily reports

---

## Key Outputs

### Infinite Scroll
**Location**: `mega_thread/INFINITE_SCROLL.md`

Human-readable Markdown document containing all accumulated knowledge organized by category:
- Knowledge
- Probes
- Thoughts
- Integrations
- Protocols
- Truths

### Mega Thread Master
**Location**: `mega_thread/mega_thread_master.json`

Complete system state in JSON format with full metadata and relationships.

### Daily Reports
**Location**: `logs/daily_report_YYYYMMDD.md`

Summary of each execution with statistics and system health.

---

## Adding Conversation Data

1. Place conversation files in the `conversations/` directory
2. Supported formats: `.txt`, `.md`, `.json`, `.log`
3. Run the orchestrator to process new files
4. Knowledge will be automatically extracted and compiled

---

## Pattern Recognition

The system recognizes these patterns in conversations:

### Knowledge
- `KNOWLEDGE:`, `INSIGHT:`, `DISCOVERY:`
- `I learned`, `We discovered`, `Key finding`

### Probes
- `PROBE:`, `QUESTION:`, `INQUIRY:`
- `What if`, `How might`, `Could we`

### Thoughts
- `THOUGHT:`, `REFLECTION:`, `OBSERVATION:`
- `I think`, `I believe`, `It seems`

### Integrations
- `INTEGRATION:`, `CONNECTION:`, `SYNTHESIS:`
- `connects to`, `relates to`, `builds upon`

### Protocols
- `PROTOCOL:`, `PROCEDURE:`, `PROCESS:`

### Truths
- `TRUTH:`, `PRINCIPLE:`, `AXIOM:`, `GROSSIAN:`

---

## Command Line Options

```bash
# Process past 24 hours (default)
python3 scripts/daily_orchestrator.py

# Process past 7 days
python3 scripts/daily_orchestrator.py --hours 168

# Custom base directory
python3 scripts/daily_orchestrator.py --base-dir /path/to/system
```

---

## Features

✓ Automated conversation scanning  
✓ Advanced pattern recognition  
✓ Multi-category classification  
✓ Intelligent deduplication  
✓ Relationship mapping  
✓ Infinite Scroll Protocol compliance  
✓ JSON and Markdown output  
✓ Comprehensive logging  
✓ Daily reporting  

---

## Infinite Scroll Protocol

The system follows the Infinite Scroll Protocol:

1. **Add-Only**: Knowledge is never deleted, only added
2. **Cumulative**: All knowledge accumulates over time
3. **Attributed**: Full source tracking and timestamps
4. **Connected**: Relationships mapped between entries
5. **Accessible**: Multiple formats for different needs

---

## System Status

Check the latest daily report in `logs/` for current system status and statistics.

---

## Support

For detailed information, see `EXECUTION_SUMMARY.md`

---

*Protocol: Infinite Scroll Protocol v1.0.0*  
*Status: Operational*
