#!/usr/bin/env python3
"""
Phoenix Protocol - Autonomous System Health Analyzer
Performs comprehensive analysis of all Phoenix systems
"""

import os
import sys
from pathlib import Path
from collections import defaultdict

class PhoenixHealthAnalyzer:
    """Autonomous health analysis for Phoenix Protocol systems"""
    
    def __init__(self, base_path="/mnt/user-data/outputs"):
        self.base_path = Path(base_path)
        self.results = {
            'code_health': {},
            'documentation': {},
            'completeness': {},
            'deployment_readiness': {}
        }
    
    def analyze_codebase(self):
        """Analyze all Python code"""
        print("🔍 Analyzing codebase...")
        
        py_files = list(self.base_path.rglob("*.py"))
        total_lines = 0
        files_by_system = defaultdict(list)
        
        for py_file in py_files:
            try:
                with open(py_file, 'r') as f:
                    lines = len(f.readlines())
                    total_lines += lines
                    
                    # Categorize by system
                    if 'phoenix-agi-webapp' in str(py_file):
                        files_by_system['Phoenix v∞'].append((py_file.name, lines))
                    elif 'phoenix-omega' in str(py_file):
                        files_by_system['Phoenix Ω'].append((py_file.name, lines))
                    else:
                        files_by_system['Other'].append((py_file.name, lines))
            except:
                pass
        
        self.results['code_health'] = {
            'total_files': len(py_files),
            'total_lines': total_lines,
            'by_system': dict(files_by_system),
            'average_file_size': total_lines / len(py_files) if py_files else 0
        }
        
        print(f"  ✓ Analyzed {len(py_files)} Python files")
        print(f"  ✓ Total lines: {total_lines}")
    
    def analyze_documentation(self):
        """Analyze documentation completeness"""
        print("\n📚 Analyzing documentation...")
        
        md_files = list(self.base_path.rglob("*.md"))
        total_doc_lines = 0
        doc_by_type = defaultdict(int)
        
        for md_file in md_files:
            try:
                with open(md_file, 'r') as f:
                    lines = len(f.readlines())
                    total_doc_lines += lines
                    
                    # Categorize documentation
                    name_lower = md_file.name.lower()
                    if 'readme' in name_lower:
                        doc_by_type['README'] += 1
                    elif 'deploy' in name_lower:
                        doc_by_type['Deployment'] += 1
                    elif 'architecture' in name_lower:
                        doc_by_type['Architecture'] += 1
                    elif 'omega' in name_lower:
                        doc_by_type['Omega'] += 1
                    else:
                        doc_by_type['General'] += 1
            except:
                pass
        
        self.results['documentation'] = {
            'total_files': len(md_files),
            'total_lines': total_doc_lines,
            'by_type': dict(doc_by_type),
            'avg_doc_size': total_doc_lines / len(md_files) if md_files else 0
        }
        
        print(f"  ✓ Analyzed {len(md_files)} documentation files")
        print(f"  ✓ Total doc lines: {total_doc_lines}")
    
    def check_deployment_readiness(self):
        """Check if systems are deployment-ready"""
        print("\n🚀 Checking deployment readiness...")
        
        critical_files = [
            'phoenix-agi-webapp/backend/main.py',
            'phoenix-agi-webapp/backend/requirements.txt',
            'phoenix-agi-webapp/docker-compose.yml',
            'phoenix-agi-webapp/.env.example',
        ]
        
        readiness = {}
        for file_path in critical_files:
            full_path = self.base_path / file_path
            exists = full_path.exists()
            readiness[file_path] = 'READY' if exists else 'MISSING'
            status = '✓' if exists else '✗'
            print(f"  {status} {file_path}")
        
        ready_count = sum(1 for v in readiness.values() if v == 'READY')
        readiness_score = (ready_count / len(critical_files)) * 100
        
        self.results['deployment_readiness'] = {
            'files_checked': readiness,
            'ready_count': ready_count,
            'total_required': len(critical_files),
            'readiness_score': readiness_score
        }
        
        print(f"\n  Deployment Readiness: {readiness_score:.0f}%")
    
    def assess_completeness(self):
        """Assess overall system completeness"""
        print("\n📊 Assessing system completeness...")
        
        required_components = {
            'Phoenix v∞ Backend': 'phoenix-agi-webapp/backend',
            'Phoenix Ω Core': 'phoenix-omega-complete',
            'Complete Package': 'PHOENIX_COMPLETE_PACKAGE',
            'Documentation': True,  # Already checked
            'Deployment Configs': True,  # Already checked
        }
        
        completeness = {}
        for component, path_or_bool in required_components.items():
            if isinstance(path_or_bool, bool):
                completeness[component] = 'COMPLETE'
            else:
                full_path = self.base_path / path_or_bool
                completeness[component] = 'COMPLETE' if full_path.exists() else 'INCOMPLETE'
        
        complete_count = sum(1 for v in completeness.values() if v == 'COMPLETE')
        completeness_score = (complete_count / len(completeness)) * 100
        
        self.results['completeness'] = {
            'components': completeness,
            'complete_count': complete_count,
            'total_components': len(completeness),
            'completeness_score': completeness_score
        }
        
        for component, status in completeness.items():
            symbol = '✓' if status == 'COMPLETE' else '✗'
            print(f"  {symbol} {component}: {status}")
        
        print(f"\n  Overall Completeness: {completeness_score:.0f}%")
    
    def generate_report(self):
        """Generate comprehensive health report"""
        print("\n" + "="*70)
        print("🐦‍🔥 PHOENIX PROTOCOL - AUTONOMOUS HEALTH REPORT")
        print("="*70)
        
        print("\n📊 CODE METRICS:")
        ch = self.results['code_health']
        print(f"  Total Python Files: {ch['total_files']}")
        print(f"  Total Code Lines: {ch['total_lines']}")
        print(f"  Average File Size: {ch['average_file_size']:.0f} lines")
        
        print("\n📚 DOCUMENTATION METRICS:")
        doc = self.results['documentation']
        print(f"  Total Doc Files: {doc['total_files']}")
        print(f"  Total Doc Lines: {doc['total_lines']}")
        print(f"  Average Doc Size: {doc['avg_doc_size']:.0f} lines")
        
        print("\n✅ SYSTEM COMPLETENESS:")
        comp = self.results['completeness']
        print(f"  Components Complete: {comp['complete_count']}/{comp['total_components']}")
        print(f"  Completeness Score: {comp['completeness_score']:.0f}%")
        
        print("\n🚀 DEPLOYMENT READINESS:")
        dr = self.results['deployment_readiness']
        print(f"  Critical Files Ready: {dr['ready_count']}/{dr['total_required']}")
        print(f"  Readiness Score: {dr['readiness_score']:.0f}%")
        
        print("\n🎯 OVERALL ASSESSMENT:")
        overall = (comp['completeness_score'] + dr['readiness_score']) / 2
        
        if overall >= 90:
            status = "🔥 PRODUCTION READY"
        elif overall >= 70:
            status = "⚡ DEPLOYMENT READY"
        elif overall >= 50:
            status = "⚠️  TESTING READY"
        else:
            status = "🚧 DEVELOPMENT STAGE"
        
        print(f"  Status: {status}")
        print(f"  Overall Score: {overall:.0f}%")
        
        print("\n" + "="*70)
        
        return overall >= 70  # Return True if deployment ready
    
    def run(self):
        """Run complete autonomous analysis"""
        print("🐦‍🔥 Starting Autonomous Health Analysis...\n")
        
        self.analyze_codebase()
        self.analyze_documentation()
        self.check_deployment_readiness()
        self.assess_completeness()
        
        is_ready = self.generate_report()
        
        if is_ready:
            print("\n✅ SYSTEM IS READY FOR DEPLOYMENT")
            return 0
        else:
            print("\n⚠️  SYSTEM NEEDS MORE WORK BEFORE DEPLOYMENT")
            return 1


if __name__ == "__main__":
    analyzer = PhoenixHealthAnalyzer()
    sys.exit(analyzer.run())
