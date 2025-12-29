#!/usr/bin/env python3
"""
Praxion - Infinite Scroll Log Engine
Manages conversation history, context, and mythic template integration
"""

import logging
import os
import json
import time
import uuid
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("praxion.infinite_scroll")

class InfiniteScrollEngine:
    """
    The InfiniteScrollEngine manages conversation history, context persistence,
    and mythic template integration for Praxion.
    """
    
    def __init__(self, storage_path: str = None):
        """
        Initialize the InfiniteScrollEngine
        
        Args:
            storage_path: Path to log storage directory
        """
        self.storage_path = storage_path or os.path.join(os.path.dirname(__file__), "../../resources/memory")
        os.makedirs(self.storage_path, exist_ok=True)
        
        # Initialize mythic template
        self.mythic_template = self._load_mythic_template()
        
        # Initialize active sessions
        self.active_sessions = {}
        
        # Load existing sessions
        self._load_sessions()
        
        logger.info(f"InfiniteScrollEngine initialized with mythic template")
    
    def _load_mythic_template(self) -> Dict[str, Any]:
        """
        Load the mythic template for the Infinite Scroll
        
        Returns:
            Mythic template dictionary
        """
        template_path = os.path.join(self.storage_path, "mythic_template.json")
        
        # Create default template if it doesn't exist
        if not os.path.exists(template_path):
            default_template = {
                "version": "1.0",
                "name": "Praxion Mythic Template",
                "author": "Justin Conzet",
                "created_at": datetime.now().isoformat(),
                "description": "Mythic template for Praxion Infinite Scroll",
                "sigil": "PRAX:INFINITE_SCROLL",
                "system_dna": {
                    "core_principles": [
                        "Knowledge preservation across sessions",
                        "Context-aware responses",
                        "Persona-specific memory",
                        "Temporal awareness"
                    ],
                    "memory_structure": {
                        "short_term": {"max_entries": 100, "retention": "session"},
                        "long_term": {"max_entries": 1000, "retention": "permanent"},
                        "episodic": {"max_entries": 50, "retention": "permanent"}
                    }
                },
                "context_layers": [
                    {"name": "immediate", "weight": 1.0, "window_size": 10},
                    {"name": "recent", "weight": 0.7, "window_size": 50},
                    {"name": "historical", "weight": 0.3, "window_size": 100}
                ],
                "metadata_schema": {
                    "timestamp": {"type": "datetime", "required": true},
                    "persona_id": {"type": "string", "required": true},
                    "session_id": {"type": "string", "required": true},
                    "message_type": {"type": "string", "required": true},
                    "importance": {"type": "float", "required": false, "default": 0.5},
                    "tags": {"type": "array", "required": false, "default": []}
                }
            }
            
            with open(template_path, 'w') as f:
                json.dump(default_template, f, indent=2)
            
            logger.info("Created default mythic template")
            return default_template
        
        # Load existing template
        try:
            with open(template_path, 'r') as f:
                template = json.load(f)
            logger.info("Loaded mythic template from storage")
            return template
        except Exception as e:
            logger.error(f"Error loading mythic template: {str(e)}")
            # Create and return a minimal template as fallback
            minimal_template = {
                "version": "1.0",
                "name": "Minimal Fallback Template",
                "sigil": "PRAX:FALLBACK",
                "system_dna": {"core_principles": ["Fallback operation"]}
            }
            return minimal_template
    
    def _load_sessions(self):
        """Load existing session data"""
        try:
            sessions_dir = os.path.join(self.storage_path, "sessions")
            os.makedirs(sessions_dir, exist_ok=True)
            
            # Load the session index if it exists
            index_path = os.path.join(sessions_dir, "index.json")
            if os.path.exists(index_path):
                with open(index_path, 'r') as f:
                    session_index = json.load(f)
                logger.info(f"Loaded session index with {len(session_index)} sessions")
            else:
                # Create empty index
                session_index = {}
                with open(index_path, 'w') as f:
                    json.dump(session_index, f, indent=2)
                logger.info("Created empty session index")
        except Exception as e:
            logger.error(f"Error loading sessions: {str(e)}")
    
    def _get_session_path(self, session_id: str) -> str:
        """
        Get the file path for a session
        
        Args:
            session_id: Session ID
            
        Returns:
            Path to the session file
        """
        return os.path.join(self.storage_path, "sessions", f"{session_id}.json")
    
    def _save_session_index(self, session_id: str, persona_id: str, metadata: Dict[str, Any]):
        """
        Save a session to the index
        
        Args:
            session_id: Session ID
            persona_id: Persona ID
            metadata: Session metadata
        """
        index_path = os.path.join(self.storage_path, "sessions", "index.json")
        
        try:
            # Load existing index
            if os.path.exists(index_path):
                with open(index_path, 'r') as f:
                    session_index = json.load(f)
            else:
                session_index = {}
            
            # Add or update session in index
            session_index[session_id] = {
                "persona_id": persona_id,
                "created_at": metadata.get("created_at", datetime.now().isoformat()),
                "last_updated": datetime.now().isoformat(),
                "message_count": metadata.get("message_count", 0),
                "title": metadata.get("title", f"Session {session_id}")
            }
            
            # Save updated index
            with open(index_path, 'w') as f:
                json.dump(session_index, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving session index: {str(e)}")
    
    def create_session(self, persona_id: str, title: Optional[str] = None) -> str:
        """
        Create a new conversation session
        
        Args:
            persona_id: ID of the persona
            title: Optional title for the session
            
        Returns:
            Session ID
        """
        # Generate a unique session ID
        session_id = f"session_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        
        # Create session metadata
        created_at = datetime.now().isoformat()
        session_data = {
            "id": session_id,
            "persona_id": persona_id,
            "created_at": created_at,
            "last_updated": created_at,
            "title": title or f"Session {created_at}",
            "message_count": 0,
            "messages": [],
            "metadata": {
                "mythic_sigil": self.mythic_template["sigil"],
                "template_version": self.mythic_template["version"]
            }
        }
        
        # Save session data
        session_path = self._get_session_path(session_id)
        with open(session_path, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        # Update session index
        self._save_session_index(session_id, persona_id, session_data)
        
        # Add to active sessions
        self.active_sessions[session_id] = session_data
        
        logger.info(f"Created new session {session_id} for persona {persona_id}")
        return session_id
    
    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a session
        
        Args:
            session_id: Session ID
            
        Returns:
            Session data if found, None otherwise
        """
        # Check if session is already active
        if session_id in self.active_sessions:
            return self.active_sessions[session_id]
        
        # Load session from file
        session_path = self._get_session_path(session_id)
        if not os.path.exists(session_path):
            logger.warning(f"Session {session_id} not found")
            return None
        
        try:
            with open(session_path, 'r') as f:
                session_data = json.load(f)
            
            # Add to active sessions
            self.active_sessions[session_id] = session_data
            
            logger.info(f"Loaded session {session_id}")
            return session_data
        except Exception as e:
            logger.error(f"Error loading session {session_id}: {str(e)}")
            return None
    
    def list_sessions(self, persona_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List available sessions
        
        Args:
            persona_id: Optional persona ID to filter by
            
        Returns:
            List of session metadata
        """
        index_path = os.path.join(self.storage_path, "sessions", "index.json")
        
        if not os.path.exists(index_path):
            return []
        
        try:
            with open(index_path, 'r') as f:
                session_index = json.load(f)
            
            # Filter by persona if specified
            if persona_id:
                filtered_sessions = {
                    session_id: data
                    for session_id, data in session_index.items()
                    if data["persona_id"] == persona_id
                }
                
                # Convert to list and sort by last_updated (newest first)
                sessions = [
                    {"id": session_id, **data}
                    for session_id, data in filtered_sessions.items()
                ]
            else:
                # Convert to list and sort by last_updated (newest first)
                sessions = [
                    {"id": session_id, **data}
                    for session_id, data in session_index.items()
                ]
            
            # Sort by last_updated (newest first)
            sessions.sort(key=lambda x: x.get("last_updated", ""), reverse=True)
            
            return sessions
        except Exception as e:
            logger.error(f"Error listing sessions: {str(e)}")
            return []
    
    def add_message(self, session_id: str, message: Dict[str, Any]) -> bool:
        """
        Add a message to a session
        
        Args:
            session_id: Session ID
            message: Message data
            
        Returns:
            True if successful, False otherwise
        """
        # Load session if not active
        if session_id not in self.active_sessions:
            session_data = self.load_session(session_id)
            if not session_data:
                logger.warning(f"Cannot add message: Session {session_id} not found")
                return False
        else:
            session_data = self.active_sessions[session_id]
        
        # Ensure message has required fields
        if "content" not in message:
            logger.warning("Cannot add message: Missing content")
            return False
        
        if "role" not in message:
            logger.warning("Cannot add message: Missing role")
            return False
        
        # Add timestamp if not present
        if "timestamp" not in message:
            message["timestamp"] = datetime.now().isoformat()
        
        # Add message ID if not present
        if "id" not in message:
            message["id"] = f"msg_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        
        # Add message to session
        session_data["messages"].append(message)
        session_data["message_count"] += 1
        session_data["last_updated"] = datetime.now().isoformat()
        
        # Update session file
        session_path = self._get_session_path(session_id)
        with open(session_path, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        # Update session index
        self._save_session_index(
            session_id,
            session_data["persona_id"],
            {
                "created_at": session_data["created_at"],
                "message_count": session_data["message_count"],
                "title": session_data["title"]
            }
        )
        
        logger.info(f"Added message to session {session_id}")
        return True
    
    def get_messages(self, session_id: str, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get messages from a session
        
        Args:
            session_id: Session ID
            limit: Optional maximum number of messages to return
            offset: Optional offset to start from
            
        Returns:
            List of messages
        """
        # Load session if not active
        if session_id not in self.active_sessions:
            session_data = self.load_session(session_id)
            if not session_data:
                logger.warning(f"Cannot get messages: Session {session_id} not found")
                return []
        else:
            session_data = self.active_sessions[session_id]
        
        # Get messages with limit and offset
        messages = session_data["messages"]
        
        if offset > 0:
            messages = messages[offset:]
        
        if limit is not None:
            messages = messages[:limit]
        
        return messages
    
    def get_context(self, session_id: str, window_size: int = 10) -> List[Dict[str, Any]]:
        """
        Get conversation context from a session
        
        Args:
            session_id: Session ID
            window_size: Number of recent messages to include
            
        Returns:
            List of context messages
        """
        # Get recent messages
        messages = self.get_messages(session_id, limit=window_size)
        
        # Format for LLM context
        context = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            # Map roles to standard format
            if role == "user":
                context_role = "user"
            elif role == "assistant":
                context_role = "assistant"
            elif role == "system":
                context_role = "system"
            else:
                # Skip unknown roles
                continue
            
            context.append({
                "role": context_role,
                "content": content
            })
        
        return context
    
    def search_messages(self, query: str, persona_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for messages across sessions
        
        Args:
            query: Search query
            persona_id: Optional persona ID to filter by
            
        Returns:
            List of matching messages with session context
        """
        results = []
        query_lower = query.lower()
        
        # Get list of sessions to search
        sessions = self.l
(Content truncated due to size limit. Use line ranges to read in chunks)