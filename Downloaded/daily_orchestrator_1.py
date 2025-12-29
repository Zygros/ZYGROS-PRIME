#!/usr/bin/env python3
"""
Daily Orchestrator - Infinite Scroll Protocol Command Center
Part of the Infinite Scroll Protocol Knowledge Management System

Orchestrates the daily knowledge management workflow:
1. Scan for new conversation files
2. Extract knowledge using advanced pattern recognition
3. Compile into daily compilations with deduplication
4. Update mega thread master document
5. Generate comprehensive reports
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import subprocess


class DailyOrchestrator:
    """Orchestrates the daily knowledge management system execution."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_dir = Path(config.get('base_dir', '/home/ubuntu/knowledge_system'))
        self.scripts_dir = self.base_dir / 'scripts'
        self.logs_dir = self.base_dir / 'data' / 'logs'
        
        self.execution_log = []
        self.start_time = datetime.now()
    
    def log(self, level: str, message: str):
        """Log a message with timestamp."""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'level': level,
            'message': message
        }
        self.execution_log.append(log_entry)
        
        # Console output
        print(f"[{timestamp}] {level}: {message}")
        
        # File output
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = self.logs_dir / f'orchestrator_{datetime.now().strftime("%Y%m%d")}.log'
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {level}: {message}\n")
    
    def run_component(self, component_name: str, script_path: Path) -> Dict[str, Any]:
        """Run a component script and capture results."""
        self.log('INFO', f"Starting component: {component_name}")
        
        try:
            # Run the script
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            component_result = {
                'component': component_name,
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'execution_time': (datetime.now() - self.start_time).total_seconds()
            }
            
            if result.returncode == 0:
                self.log('SUCCESS', f"Component {component_name} completed successfully")
            else:
                self.log('ERROR', f"Component {component_name} failed with code {result.returncode}")
                self.log('ERROR', f"Error output: {result.stderr}")
            
            return component_result
            
        except subprocess.TimeoutExpired:
            self.log('ERROR', f"Component {component_name} timed out")
            return {
                'component': component_name,
                'success': False,
                'error': 'Timeout',
                'execution_time': (datetime.now() - self.start_time).total_seconds()
            }
        except Exception as e:
            self.log('ERROR', f"Component {component_name} error: {str(e)}")
            return {
                'component': component_name,
                'success': False,
                'error': str(e),
                'execution_time': (datetime.now() - self.start_time).total_seconds()
            }
    
    def execute_workflow(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Execute the complete knowledge management workflow."""
        self.log('INFO', '=' * 80)
        self.log('INFO', 'DAILY KNOWLEDGE MANAGEMENT SYSTEM - Infinite Scroll Protocol')
        self.log('INFO', '=' * 80)
        self.log('INFO', f'Time window: {time_window_hours} hours')
        self.log('INFO', f'Base directory: {self.base_dir}')
        
        workflow_results = {
            'start_time': self.start_time.isoformat(),
            'time_window_hours': time_window_hours,
            'components': [],
            'overall_success': True
        }
        
        # Phase 1: Knowledge Extraction
        self.log('INFO', '\n--- PHASE 1: KNOWLEDGE EXTRACTION ---')
        extractor_script = self.scripts_dir / 'knowledge_extractor.py'
        
        if extractor_script.exists():
            extraction_result = self.run_component('Knowledge Extractor', extractor_script)
            workflow_results['components'].append(extraction_result)
            
            if not extraction_result['success']:
                workflow_results['overall_success'] = False
                self.log('ERROR', 'Extraction failed, aborting workflow')
                return workflow_results
        else:
            self.log('ERROR', f'Extractor script not found: {extractor_script}')
            workflow_results['overall_success'] = False
            return workflow_results
        
        # Phase 2: Mega Thread Compilation
        self.log('INFO', '\n--- PHASE 2: MEGA THREAD COMPILATION ---')
        compiler_script = self.scripts_dir / 'mega_thread_compiler.py'
        
        if compiler_script.exists():
            compilation_result = self.run_component('Mega Thread Compiler', compiler_script)
            workflow_results['components'].append(compilation_result)
            
            if not compilation_result['success']:
                workflow_results['overall_success'] = False
                self.log('WARNING', 'Compilation failed, but extraction was successful')
        else:
            self.log('ERROR', f'Compiler script not found: {compiler_script}')
            workflow_results['overall_success'] = False
        
        # Phase 3: Generate Execution Summary
        self.log('INFO', '\n--- PHASE 3: EXECUTION SUMMARY ---')
        workflow_results['end_time'] = datetime.now().isoformat()
        workflow_results['total_execution_time'] = (datetime.now() - self.start_time).total_seconds()
        workflow_results['execution_log'] = self.execution_log
        
        # Save execution summary
        summary_file = self.save_execution_summary(workflow_results)
        workflow_results['summary_file'] = str(summary_file)
        
        self.log('INFO', f'\nTotal execution time: {workflow_results["total_execution_time"]:.2f} seconds')
        self.log('INFO', f'Overall success: {workflow_results["overall_success"]}')
        self.log('INFO', f'Execution summary saved to: {summary_file}')
        
        self.log('INFO', '\n' + '=' * 80)
        self.log('INFO', 'WORKFLOW COMPLETE')
        self.log('INFO', '=' * 80)
        
        return workflow_results
    
    def save_execution_summary(self, workflow_results: Dict[str, Any]) -> Path:
        """Save the execution summary to a file."""
        summary_dir = self.base_dir / 'data' / 'logs' / 'summaries'
        summary_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        summary_file = summary_dir / f'execution_summary_{timestamp}.json'
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(workflow_results, f, indent=2, ensure_ascii=False)
        
        # Also create a markdown summary
        md_summary_file = summary_dir / f'execution_summary_{timestamp}.md'
        md_content = self.generate_markdown_summary(workflow_results)
        
        with open(md_summary_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return summary_file
    
    def generate_markdown_summary(self, workflow_results: Dict[str, Any]) -> str:
        """Generate a markdown summary of the execution."""
        md = f"""# Daily Knowledge Management System - Execution Summary

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Time Window**: {workflow_results['time_window_hours']} hours  
**Overall Success**: {'✓ YES' if workflow_results['overall_success'] else '✗ NO'}  
**Total Execution Time**: {workflow_results['total_execution_time']:.2f} seconds

---

## Component Results

"""
        
        for component in workflow_results['components']:
            status = '✓ SUCCESS' if component['success'] else '✗ FAILED'
            md += f"### {component['component']}\n\n"
            md += f"- **Status**: {status}\n"
            md += f"- **Return Code**: {component.get('returncode', 'N/A')}\n"
            md += f"- **Execution Time**: {component.get('execution_time', 0):.2f}s\n\n"
            
            if component.get('stdout'):
                md += f"**Output**:\n```\n{component['stdout'][:500]}\n```\n\n"
            
            if component.get('stderr'):
                md += f"**Errors**:\n```\n{component['stderr'][:500]}\n```\n\n"
        
        md += f"---\n\n## Execution Log\n\n"
        
        for log_entry in workflow_results['execution_log'][-20:]:  # Last 20 entries
            md += f"- **[{log_entry['timestamp']}]** {log_entry['level']}: {log_entry['message']}\n"
        
        md += f"\n---\n\n*Generated by Daily Orchestrator - Infinite Scroll Protocol*\n"
        
        return md
    
    def create_sample_conversation(self):
        """Create a sample conversation file for testing."""
        conversations_dir = self.base_dir / 'data' / 'conversations'
        conversations_dir.mkdir(parents=True, exist_ok=True)
        
        sample_file = conversations_dir / f'sample_conversation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        
        sample_content = f"""# Sample Conversation - Knowledge Management System

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Knowledge Items

Knowledge: The Infinite Scroll Protocol mandates that all knowledge is preserved and accumulated without loss.

Insight: Advanced pattern recognition algorithms can extract structured knowledge from unstructured conversation data.

Grossian Truth: The principle of perpetual accumulation is fundamental to the knowledge management system.

## Probes and Questions

Question: How can we improve the relationship mapping between knowledge entries?

Probe: What patterns emerge when analyzing knowledge accumulation over extended time periods?

Investigation: Explore methods for automatic categorization of knowledge based on semantic content.

## Thoughts and Reflections

Thought: The system architecture mirrors the Zythrognosis protocol with distinct layers of processing.

Reflection: Deduplication is essential to maintain the integrity of the knowledge repository.

Hypothesis: Knowledge relationships can be mapped using graph-based algorithms.

## Integrations

Integration: The extractor, compiler, and orchestrator components work in harmony to create a unified system.

Synthesis: Combining temporal analysis with categorical organization provides powerful navigation capabilities.

Connection: This system relates to the broader Golden Sovereign OS architecture.

## Protocols

Protocol: Daily execution at scheduled intervals ensures continuous knowledge accumulation.

Procedure: Scan conversations → Extract knowledge → Compile insights → Update mega thread → Generate reports

Workflow: The orchestrator coordinates all components in a sequential, error-resilient manner.

---

*This is a sample conversation file generated for testing the knowledge management system.*
"""
        
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        
        self.log('INFO', f'Sample conversation created: {sample_file}')
        return sample_file


def main():
    """Main execution function."""
    config = {
        'base_dir': '/home/ubuntu/knowledge_system',
        'time_window_hours': 24
    }
    
    orchestrator = DailyOrchestrator(config)
    
    # Create sample conversation for testing
    orchestrator.log('INFO', 'Creating sample conversation for testing...')
    orchestrator.create_sample_conversation()
    
    # Execute workflow
    results = orchestrator.execute_workflow(time_window_hours=config['time_window_hours'])
    
    # Exit with appropriate code
    sys.exit(0 if results['overall_success'] else 1)


if __name__ == '__main__':
    main()
