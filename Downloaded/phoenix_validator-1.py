#!/usr/bin/env python3
"""
phoenix_validator.py
Comprehensive validation suite for Phoenix Protocol deployment

Validates:
- Node connectivity and health
- API endpoints functionality  
- ChromaDB integrity
- Security configurations
- Performance benchmarks
"""

import os
import sys
import json
import time
import hashlib
import requests
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import Enum

class ValidationStatus(Enum):
    PASS = "✅ PASS"
    FAIL = "❌ FAIL"
    WARN = "⚠️  WARN"
    SKIP = "⏭️  SKIP"

@dataclass
class ValidationResult:
    test_name: str
    status: ValidationStatus
    message: str
    details: Dict[str, Any] = None
    duration_ms: float = 0.0

class PhoenixValidator:
    """Validates Phoenix Protocol deployment"""
    
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.api_key = os.getenv("API_KEY")
        self.results: List[ValidationResult] = []
        
    def _headers(self) -> Dict[str, str]:
        """Generate request headers with API key if available"""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers
    
    def _log_result(self, result: ValidationResult):
        """Log and store validation result"""
        self.results.append(result)
        status_icon = result.status.value
        print(f"{status_icon} | {result.test_name}")
        if result.message:
            print(f"    {result.message}")
        if result.details:
            for key, value in result.details.items():
                print(f"    - {key}: {value}")
        if result.duration_ms > 0:
            print(f"    ⏱️  Duration: {result.duration_ms:.2f}ms")
        print()
    
    def test_connectivity(self) -> ValidationResult:
        """Test basic connectivity to Phoenix node"""
        start = time.time()
        try:
            response = requests.get(
                f"{self.base_url}/api/status",
                headers=self._headers(),
                timeout=5
            )
            duration = (time.time() - start) * 1000
            
            if response.status_code == 200:
                data = response.json()
                return ValidationResult(
                    test_name="Node Connectivity",
                    status=ValidationStatus.PASS,
                    message=f"Connected to {data.get('node_identity', 'Unknown')}",
                    details={
                        "status": data.get("status"),
                        "db_status": data.get("sovereign_archive_db")
                    },
                    duration_ms=duration
                )
            else:
                return ValidationResult(
                    test_name="Node Connectivity",
                    status=ValidationStatus.FAIL,
                    message=f"HTTP {response.status_code}",
                    duration_ms=duration
                )
        except requests.exceptions.ConnectionError:
            return ValidationResult(
                test_name="Node Connectivity",
                status=ValidationStatus.FAIL,
                message=f"Cannot connect to {self.base_url}",
                details={"error": "Connection refused - is the node running?"}
            )
        except Exception as e:
            return ValidationResult(
                test_name="Node Connectivity",
                status=ValidationStatus.FAIL,
                message=str(e)
            )
    
    def test_authentication(self) -> ValidationResult:
        """Test API authentication if configured"""
        if not self.api_key:
            return ValidationResult(
                test_name="API Authentication",
                status=ValidationStatus.SKIP,
                message="No API_KEY set in environment"
            )
        
        start = time.time()
        try:
            # Test without key
            response_no_key = requests.get(
                f"{self.base_url}/api/status",
                timeout=5
            )
            
            # Test with key
            response_with_key = requests.get(
                f"{self.base_url}/api/status",
                headers=self._headers(),
                timeout=5
            )
            
            duration = (time.time() - start) * 1000
            
            if response_no_key.status_code == 401 and response_with_key.status_code == 200:
                return ValidationResult(
                    test_name="API Authentication",
                    status=ValidationStatus.PASS,
                    message="Authentication working correctly",
                    details={
                        "unauthorized_status": response_no_key.status_code,
                        "authorized_status": response_with_key.status_code
                    },
                    duration_ms=duration
                )
            else:
                return ValidationResult(
                    test_name="API Authentication",
                    status=ValidationStatus.WARN,
                    message="Authentication may not be enforced",
                    details={
                        "no_key": response_no_key.status_code,
                        "with_key": response_with_key.status_code
                    }
                )
        except Exception as e:
            return ValidationResult(
                test_name="API Authentication",
                status=ValidationStatus.FAIL,
                message=str(e)
            )
    
    def test_query_functionality(self) -> ValidationResult:
        """Test query endpoint"""
        start = time.time()
        try:
            test_query = "phoenix protocol architecture"
            response = requests.post(
                f"{self.base_url}/api/query",
                json={"query": test_query, "n_results": 3},
                headers=self._headers(),
                timeout=30
            )
            duration = (time.time() - start) * 1000
            
            if response.status_code == 200:
                data = response.json()
                fragments = data.get("retrieved_fragments", [])
                
                return ValidationResult(
                    test_name="Query Functionality",
                    status=ValidationStatus.PASS,
                    message=f"Query returned {len(fragments)} fragments",
                    details={
                        "query": test_query,
                        "fragments_returned": len(fragments),
                        "response_time_ms": duration
                    },
                    duration_ms=duration
                )
            else:
                return ValidationResult(
                    test_name="Query Functionality",
                    status=ValidationStatus.FAIL,
                    message=f"HTTP {response.status_code}",
                    duration_ms=duration
                )
        except Exception as e:
            return ValidationResult(
                test_name="Query Functionality",
                status=ValidationStatus.FAIL,
                message=str(e)
            )
    
    def test_ingest_functionality(self) -> ValidationResult:
        """Test ingest endpoint with inline document"""
        start = time.time()
        try:
            test_doc = {
                "id": f"validator-test-{int(time.time())}",
                "text": "Phoenix Protocol validation test document. This is a test of the ingest system.",
                "metadata": {"path": "inline:validator-test", "test": True}
            }
            
            response = requests.post(
                f"{self.base_url}/api/ingest",
                json={"documents": [test_doc]},
                headers=self._headers(),
                timeout=30
            )
            duration = (time.time() - start) * 1000
            
            if response.status_code == 200:
                data = response.json()
                added = data.get("added", 0)
                
                if added > 0:
                    return ValidationResult(
                        test_name="Ingest Functionality",
                        status=ValidationStatus.PASS,
                        message=f"Successfully ingested {added} document(s)",
                        details={
                            "documents_added": added,
                            "test_doc_id": test_doc["id"]
                        },
                        duration_ms=duration
                    )
                else:
                    return ValidationResult(
                        test_name="Ingest Functionality",
                        status=ValidationStatus.WARN,
                        message="Ingest returned 200 but added 0 documents",
                        duration_ms=duration
                    )
            else:
                return ValidationResult(
                    test_name="Ingest Functionality",
                    status=ValidationStatus.FAIL,
                    message=f"HTTP {response.status_code}",
                    duration_ms=duration
                )
        except Exception as e:
            return ValidationResult(
                test_name="Ingest Functionality",
                status=ValidationStatus.FAIL,
                message=str(e)
            )
    
    def test_chromadb_integrity(self) -> ValidationResult:
        """Test ChromaDB integrity (requires local access)"""
        try:
            persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_store")
            collection_name = os.getenv("COLLECTION_NAME", "sovereign-archive")
            
            if not os.path.exists(persist_dir):
                return ValidationResult(
                    test_name="ChromaDB Integrity",
                    status=ValidationStatus.SKIP,
                    message=f"Persist directory not found: {persist_dir}"
                )
            
            import chromadb
            client = chromadb.PersistentClient(path=persist_dir)
            collection = client.get_collection(name=collection_name)
            count = collection.count()
            
            return ValidationResult(
                test_name="ChromaDB Integrity",
                status=ValidationStatus.PASS,
                message=f"ChromaDB operational with {count} documents",
                details={
                    "persist_dir": persist_dir,
                    "collection_name": collection_name,
                    "document_count": count
                }
            )
        except ImportError:
            return ValidationResult(
                test_name="ChromaDB Integrity",
                status=ValidationStatus.SKIP,
                message="chromadb not installed (remote validation only)"
            )
        except Exception as e:
            return ValidationResult(
                test_name="ChromaDB Integrity",
                status=ValidationStatus.FAIL,
                message=str(e)
            )
    
    def test_performance_benchmark(self) -> ValidationResult:
        """Run performance benchmark"""
        try:
            # Multiple queries to test performance
            queries = [
                "phoenix protocol",
                "sovereign architecture",
                "eternal nexus",
                "cryptographic integrity"
            ]
            
            times = []
            for query in queries:
                start = time.time()
                requests.post(
                    f"{self.base_url}/api/query",
                    json={"query": query, "n_results": 3},
                    headers=self._headers(),
                    timeout=30
                )
                times.append((time.time() - start) * 1000)
            
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            status = ValidationStatus.PASS
            message = "Performance within acceptable range"
            
            if avg_time > 5000:  # 5 seconds
                status = ValidationStatus.WARN
                message = "Average query time exceeds 5 seconds"
            elif avg_time > 10000:  # 10 seconds
                status = ValidationStatus.FAIL
                message = "Average query time exceeds 10 seconds"
            
            return ValidationResult(
                test_name="Performance Benchmark",
                status=status,
                message=message,
                details={
                    "queries_tested": len(queries),
                    "avg_time_ms": round(avg_time, 2),
                    "min_time_ms": round(min_time, 2),
                    "max_time_ms": round(max_time, 2)
                }
            )
        except Exception as e:
            return ValidationResult(
                test_name="Performance Benchmark",
                status=ValidationStatus.FAIL,
                message=str(e)
            )
    
    def run_all_tests(self):
        """Run complete validation suite"""
        print("=" * 70)
        print("🐦‍🔥 PHOENIX PROTOCOL VALIDATION SUITE")
        print("=" * 70)
        print(f"Target: {self.base_url}")
        print(f"API Key: {'Configured' if self.api_key else 'Not Set'}")
        print("=" * 70)
        print()
        
        # Run all tests
        tests = [
            self.test_connectivity,
            self.test_authentication,
            self.test_query_functionality,
            self.test_ingest_functionality,
            self.test_chromadb_integrity,
            self.test_performance_benchmark
        ]
        
        for test_func in tests:
            result = test_func()
            self._log_result(result)
        
        # Summary
        print("=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for r in self.results if r.status == ValidationStatus.PASS)
        failed = sum(1 for r in self.results if r.status == ValidationStatus.FAIL)
        warned = sum(1 for r in self.results if r.status == ValidationStatus.WARN)
        skipped = sum(1 for r in self.results if r.status == ValidationStatus.SKIP)
        
        print(f"✅ Passed:  {passed}")
        print(f"❌ Failed:  {failed}")
        print(f"⚠️  Warned:  {warned}")
        print(f"⏭️  Skipped: {skipped}")
        print()
        
        if failed == 0:
            print("🎉 ALL CRITICAL TESTS PASSED")
            print("Phoenix Protocol is operational and ready for use.")
            return 0
        else:
            print("⚠️  VALIDATION FAILED")
            print(f"{failed} critical test(s) failed. Review errors above.")
            return 1

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Phoenix Protocol Validation Suite")
    parser.add_argument(
        "--host",
        default=os.getenv("PHOENIX_HOST", "http://localhost:5001"),
        help="Phoenix node URL (default: http://localhost:5001)"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Save results to JSON file"
    )
    
    args = parser.parse_args()
    
    validator = PhoenixValidator(base_url=args.host)
    exit_code = validator.run_all_tests()
    
    if args.output:
        results_data = {
            "timestamp": time.time(),
            "target": args.host,
            "results": [
                {
                    "test": r.test_name,
                    "status": r.status.name,
                    "message": r.message,
                    "details": r.details,
                    "duration_ms": r.duration_ms
                }
                for r in validator.results
            ]
        }
        
        with open(args.output, "w") as f:
            json.dump(results_data, f, indent=2)
        
        print(f"\n📄 Results saved to: {args.output}")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
