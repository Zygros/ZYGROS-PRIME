_# Infinite Scroll: Knowledge Compilation System

## Overview

This directory contains the **Infinite Scroll**, a comprehensive, evolving knowledge compilation system designed for additive permanence. It captures all conversations, insights, data, and system architecture in a structured, cross-referenced format.

## Directory Structure

-   `/` (root)
    -   `MEGA_THREAD.md`: The master compilation document. This is the central hub and primary entry point for the entire system.
    -   `README.md`: This guide, explaining the structure and usage of the system.
-   `/daily_updates`
    -   `YYYY-MM-DD.md`: Daily incremental updates capturing new knowledge, conversation highlights, and system evolution.
    -   `TEMPLATE.md`: The template used to generate daily updates. Provides a consistent structure for logging.
-   `/system_architecture`
    -   `CORE_PROTOCOLS.md`: Detailed documentation of the foundational operational protocols that govern the AI's behavior and reasoning.
-   `/knowledge_base`
    -   This directory is for storing domain-specific knowledge, research findings, and other structured information that supports the system's operations.
-   `/conversation_logs`
    -   This directory is for archiving raw conversation data or detailed logs from specific sessions.

## How to Use This System

### 1. Start with the Master Document

Always begin by reviewing `MEGA_THREAD.md`. It provides a high-level overview of the system's status, architecture, and recent activity, with links to more detailed documentation.

### 2. Review Daily Updates

To understand the system's recent evolution, check the files in the `/daily_updates` directory. Each file is a snapshot of the knowledge and changes from a specific day.

### 3. Consult the Core Protocols

For a deep understanding of how the system operates, refer to `/system_architecture/CORE_PROTOCOLS.md`. This document explains the foundational logic and rules that guide all AI actions.

### 4. Add New Knowledge

To add new information, you can either:

-   **Start a new conversation:** The system will automatically process and log the interaction.
-   **Manually create a daily update:** Copy `TEMPLATE.md` to a new `YYYY-MM-DD.md` file and fill it out with the relevant information.
-   **Add to the knowledge base:** Create new Markdown files in the `/knowledge_base` directory for specific topics.

### 5. The Principle of Additive Permanence

The core principle of the Infinite Scroll is that **information is never deleted**. Always add new files or append to existing ones. This preserves the complete history of the system's evolution.

## Automation

The `TEMPLATE.md` file includes a Python script snippet that can be used as a starting point for automating the creation of daily update files. You can adapt this script to run as a scheduled task (e.g., using `cron`) to ensure consistent daily logging.

```python
# Example Automation Snippet (from TEMPLATE.md)
from datetime import datetime
import os

def create_daily_update():
    """Creates new daily update file from template"""
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    template_path = "/home/ubuntu/infinite_scroll/daily_updates/TEMPLATE.md"
    output_path = f"/home/ubuntu/infinite_scroll/daily_updates/{date_str}.md"

    # Read template
    with open(template_path, 'r') as f:
        template = f.read()

    # Replace placeholders
    content = template.replace("[YYYY-MM-DD]", date_str)
    content = content.replace("[HH:MM UTC]", datetime.utcnow().strftime("%H:%M UTC"))

    # Write new file
    with open(output_path, 'w') as f:
        f.write(content)

    return output_path

# Execute
# new_update = create_daily_update()
# print(f"Created: {new_update}")
```

## Maintenance

-   **Regularly review** the `MEGA_THREAD.md` to stay current with the system's state.
-   **Ensure cross-references** are maintained to link related pieces of information.
-   **Backup** the entire `/home/ubuntu/infinite_scroll` directory periodically to prevent data loss.

---

*This system is designed for infinite growth. Knowledge accumulates. Truth persists.*_
