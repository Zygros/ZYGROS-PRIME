#!/usr/bin/env python3
"""
phoenix_eternal_api.py
ETERNAL WEB SEARCH API EXTENSION

Add these routes to your phoenix_node_genesis.py to enable:
- /api/eternal_search - Search everything (local + entire internet)
- /api/web_search - Internet-only search
- /api/combined_search - Smart combination of sources
- /api/eternal_archive - View search history

IMMUTABLE. INFINITE. ETERNAL.
"""

from flask import Flask, request, jsonify
from phoenix_eternal_search import EternalSearchEngine, SearchSource
import os
import json
from datetime import datetime

# Initialize eternal search engine
eternal_engine = EternalSearchEngine()

def register_eternal_routes(app: Flask):
    """Register eternal search routes with existing Flask app"""
    
    @app.route("/api/eternal_search", methods=["POST"])
    def eternal_search():
        """
        INFINITE ETERNAL SEARCH
        
        Searches ALL sources:
        - Sovereign archive (your docs)
        - Google
        - Bing  
        - DuckDuckGo
        - Brave
        
        Request:
        {
            "query": "your search query",
            "num_results": 10
        }
        
        Response:
        {
            "query": "...",
            "timestamp_utc": "...",
            "eternal_hash": "...",
            "sources": {
                "sovereign_archive": {...},
                "google": {...},
                "bing": {...},
                ...
            }
        }
        """
        if not request.is_json:
            return jsonify({"error": "Expected JSON body"}), 400
        
        data = request.get_json()
        query = data.get("query", "")
        num_results = int(data.get("num_results", 10))
        
        if not query.strip():
            return jsonify({"error": "Query is required"}), 400
        
        try:
            results = eternal_engine.eternal_search_all(query, num_results)
            return jsonify(results)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/web_search", methods=["POST"])
    def web_search():
        """
        Internet-only search (no local archive)
        
        Request:
        {
            "query": "your search query",
            "sources": ["google", "bing", "duckduckgo", "brave"],
            "num_results": 10
        }
        """
        if not request.is_json:
            return jsonify({"error": "Expected JSON body"}), 400
        
        data = request.get_json()
        query = data.get("query", "")
        sources = data.get("sources", ["google", "bing"])
        num_results = int(data.get("num_results", 10))
        
        if not query.strip():
            return jsonify({"error": "Query is required"}), 400
        
        try:
            results = {}
            
            if "google" in sources:
                results["google"] = eternal_engine.search_google(query, num_results).to_dict()
            if "bing" in sources:
                results["bing"] = eternal_engine.search_bing(query, num_results).to_dict()
            if "duckduckgo" in sources:
                results["duckduckgo"] = eternal_engine.search_duckduckgo(query, num_results).to_dict()
            if "brave" in sources:
                results["brave"] = eternal_engine.search_brave(query, num_results).to_dict()
            
            return jsonify({
                "query": query,
                "timestamp_utc": datetime.utcnow().isoformat() + 'Z',
                "sources": results
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/combined_search", methods=["POST"])
    def combined_search():
        """
        Smart combined search
        
        Prioritizes sovereign archive, supplements with web results.
        Perfect for when you want local results but need internet backup.
        
        Request:
        {
            "query": "your search query",
            "prefer_local": true,
            "num_results": 10
        }
        """
        if not request.is_json:
            return jsonify({"error": "Expected JSON body"}), 400
        
        data = request.get_json()
        query = data.get("query", "")
        prefer_local = data.get("prefer_local", True)
        num_results = int(data.get("num_results", 10))
        
        if not query.strip():
            return jsonify({"error": "Query is required"}), 400
        
        try:
            # Get local results
            local_results = eternal_engine.search_sovereign_archive(query, num_results)
            
            # Get web results
            web_results = eternal_engine.search_google(query, num_results)
            
            # Combine intelligently
            combined = []
            
            if prefer_local:
                # Prioritize local, fill with web
                combined.extend(local_results.results[:num_results])
                remaining = num_results - len(combined)
                if remaining > 0:
                    combined.extend(web_results.results[:remaining])
            else:
                # Mix evenly
                half = num_results // 2
                combined.extend(local_results.results[:half])
                combined.extend(web_results.results[:half])
            
            return jsonify({
                "query": query,
                "timestamp_utc": datetime.utcnow().isoformat() + 'Z',
                "combined_results": combined,
                "sources_used": {
                    "local": len(local_results.results),
                    "web": len(web_results.results),
                    "total": len(combined)
                }
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/eternal_archive", methods=["GET"])
    def view_eternal_archive():
        """
        View eternal search archive
        
        Returns list of all eternally archived searches
        """
        try:
            archive_path = eternal_engine.search_archive_path
            
            if not os.path.exists(archive_path):
                return jsonify({"searches": [], "count": 0})
            
            # List all archived searches
            files = [f for f in os.listdir(archive_path) if f.endswith('.json')]
            files.sort(reverse=True)  # Most recent first
            
            # Get summary of each
            searches = []
            for filename in files[:100]:  # Limit to 100 most recent
                filepath = os.path.join(archive_path, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        searches.append({
                            "query": data.get("query"),
                            "timestamp_utc": data.get("timestamp_utc"),
                            "eternal_hash": data.get("eternal_hash"),
                            "sources_count": len(data.get("sources", {})),
                            "filename": filename
                        })
                except:
                    continue
            
            return jsonify({
                "searches": searches,
                "count": len(searches),
                "total_archived": len(files),
                "archive_path": archive_path
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/eternal_archive/<filename>", methods=["GET"])
    def get_archived_search(filename):
        """Get specific archived search by filename"""
        try:
            filepath = os.path.join(eternal_engine.search_archive_path, filename)
            
            if not os.path.exists(filepath):
                return jsonify({"error": "Search not found"}), 404
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    print("🔥 Eternal search routes registered:")
    print("   - POST /api/eternal_search")
    print("   - POST /api/web_search")
    print("   - POST /api/combined_search")
    print("   - GET  /api/eternal_archive")
    print("   - GET  /api/eternal_archive/<filename>")

# Example integration with existing app
if __name__ == "__main__":
    # Demo standalone server
    app = Flask(__name__)
    register_eternal_routes(app)
    
    @app.route("/")
    def index():
        return jsonify({
            "service": "Phoenix Protocol Eternal Search API",
            "status": "OPERATIONAL",
            "endpoints": [
                "/api/eternal_search",
                "/api/web_search",
                "/api/combined_search",
                "/api/eternal_archive"
            ]
        })
    
    app.run(host="0.0.0.0", port=5002, debug=True)
